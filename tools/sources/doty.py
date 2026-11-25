"""Doty, Numbers (Bible Study Textbook Series, College Press, 1973) OCR text -> sources/marked/doty.txt

Usage:  python -I tools/sources/doty.py

Reads sources/downloads/doty/Numbers.txt (copy of Downloads/Numbers.txt; the PDF beside it is the
scan it came from). The book is built in units, each: a heading ("A. SETTING OF THE EVENT v.1"),
TEXT (KJV), PARAPHRASE (his own), COMMENTARY, QUESTIONS AND RESEARCH ITEMS. One section per unit, indexed
by the verses its TEXT block covers (the "Chapter C:V." opener and the verse numbers inside the text, with
OCR slips such as "1:l" tolerated). English verse numbering (KJV). Page numbers: the scan prints the number
at the FOOT of each page, so `[p. N]` is written at the head of page N (one more than the number just passed);
running heads ("v. 1", "vv. 21-28", "NUMBERS") are dropped. The front matter and outline go in as `intro`.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "sources" / "downloads" / "doty"
OUT = ROOT / "sources" / "marked"
DIG = {"l": "1", "I": "1", "O": "0", "|": "1", "s": "5", "S": "5"}
CHREF = re.compile(r"Ch\w{2,6}r\s*((?:\d\s?){1,2})\s*[:~;]\s*((?:[0-9lIOsS|]\s?){1,3})")


def num(tok):
    return int("".join(DIG.get(c, c) for c in tok if not c.isspace()))


HEADLINE = re.compile(r"^(NUMBERS|[Vv][Vv]?\.?\s*[\d\-–, ]*|[Ww]\.?|\d{1,3}\s*[-–]\s*\d{1,3}|[Cc]h(?:apters?|s?\.)\s*[\d\-–, ]+)$")


def clean_pages(lines, first_page):
    """Drop running heads, turn the page-foot numbers into [p. N] at the head of the next page."""
    out, n = [], len(lines)
    page = first_page
    out.append(f"[p. {page}]")
    i = 0
    while i < n:
        s = lines[i].strip()
        if (re.fullmatch(r"\d{1,3}", s) and page <= int(s) <= page + 12
                and any(re.fullmatch(r"NUMBERS", x.strip()) for x in lines[i + 1:i + 9])):
            page = int(s) + 1
            out.append("")
            out.append(f"[p. {page}]")
            j = i + 1
            seen = 0
            while j < n and seen < 5 and (not lines[j].strip() or HEADLINE.match(lines[j].strip())):
                if lines[j].strip():
                    seen += 1
                j += 1
            i = j
            continue
        out.append(lines[i].rstrip())
        i += 1
    return out


def cap_line(s):
    letters = re.findall(r"[A-Za-z]", s)
    return len(letters) >= 4 and sum(c.isupper() for c in letters) / len(letters) > 0.7 and len(s) < 110


def text_range(block):
    """(start, end) verses from a TEXT block: 'Chapter C:V.' opener and the verse numbers inside."""
    txt = " ".join(block)
    m = CHREF.search(txt)
    if not m:
        return None
    c, v = num(m[1]), num(m[2])
    start = (c, v)
    pos = m.end()
    while True:
        nxt_ch = CHREF.search(txt, pos)
        nxt_v = re.compile(rf"(?<![\d:,])\b{v + 1}\s?\.\s").search(txt, pos)
        cand = [(x.start(), x, k) for x, k in ((nxt_ch, "c"), (nxt_v, "v")) if x]
        if not cand:
            break
        _, x, k = min(cand, key=lambda t: t[0])
        if k == "c":
            c2, v2 = num(x[1]), num(x[2])
            if c2 >= c and (c2, v2) > (c, v):
                c, v = c2, v2
            pos = x.end()
        else:
            v += 1
            pos = x.end()
    return start, (c, v)


def rng(a, b):
    if a == b:
        return f"{a[0]}:{a[1]}"
    return f"{a[0]}:{a[1]}-{b[1]}" if a[0] == b[0] else f"{a[0]}:{a[1]}-{b[0]}:{b[1]}"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    f = next(SRC.glob("*.txt"))
    L = f.read_text(encoding="utf-8", errors="replace").split("\n")
    texts = [i for i, l in enumerate(L) if l.strip() == "TEXT"]
    body0 = texts[0]
    # front matter: from the dedication to the first unit heading
    front_end = body0
    k = body0 - 1
    while k > 0 and (cap_line(L[k].strip()) or re.match(r"^(\(|Part |[IVX]+\.)", L[k].strip()) or not L[k].strip()):
        front_end = k
        k -= 1
    # unit starts: heading lines above each TEXT
    starts = []
    for t in texts:
        k = t - 1
        while k >= 0 and not L[k].strip():
            k -= 1
        s = t
        heads = 0
        while k >= 0 and heads < 5 and (cap_line(L[k].strip()) or re.match(r"^(\(\d|Part (One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten)|[IVX]+\.\s)", L[k].strip())):
            s = k
            heads += 1
            k -= 1
            while k >= 0 and not L[k].strip():
                k -= 1
        starts.append(s)
    # the page number that closes the page the first unit begins on
    first_page = 15
    for j in range(body0, min(body0 + 90, len(L))):
        if re.fullmatch(r"\d{1,3}", L[j].strip()) and not L[j - 1].strip():
            first_page = int(L[j].strip())
            break
    back = next((i for i, l in enumerate(L) if l.strip().startswith("ABBREVIATIONS FOR REFERENCES")), len(L))
    ends = starts[1:] + [back]
    parts = []
    nsec = 0
    intro = [x for x in L[:front_end]]
    secs = [("intro", "Front matter, introduction, outline of the book", "\n".join(intro))]
    for k_, (s, e, t) in enumerate(zip(starts, ends, texts)):
        # text block = TEXT .. PARAPHRASE
        p = next((i for i in range(t + 1, e)
                  if re.fullmatch(r"PA[A-Z]{3,9}|COMMENTARY", L[i].strip())), min(t + 40, e))
        block = [x.strip() for x in L[t + 1:p]]
        r = text_range(block)
        title0 = " ".join(x.strip() for x in L[s:t] if x.strip())
        if r is None:                              # fall back on the heading: "(10:11-12:16) ... W. 11-28"
            mv = re.search(r"[VvWw]{1,2}\s?[.,]\s?(\d{1,2})\s?[-–]\s?(\d{1,2})\s*$", title0)
            mc = re.findall(r"\(\s*([0-9lIO ]{1,3})\s*[:;]", title0)
            if mv and mc:
                r = ((num(mc[-1]), int(mv[1])), (num(mc[-1]), int(mv[2])))
        if r is None:
            mh = re.search(r"\(\s*([0-9lIO ]{1,3})\s*[:;]\s*([0-9lIO ]{1,3})\s*[-–]\s*(?:([0-9lIO ]{1,3})\s*[:;]\s*)?([0-9lIO ]{1,3})\s*\)", title0)
            if mh:
                c1 = num(mh[1])
                r = ((c1, num(mh[2])), (num(mh[3]) if mh[3] else c1, num(mh[4])))
        title = re.sub(r"\s+", " ", " ".join(x.strip() for x in L[s:t] if x.strip()))
        body = L[s:e]
        secs.append((r, title, body))
    # page cleaning must run over the whole body in one pass so the page counter carries on
    SENT = "@@UNIT@@"
    whole = []
    sset = set(starts)
    for i in range(starts[0], back):
        if i in sset:
            whole.append(SENT)
        whole.append(L[i])
    cleaned = clean_pages(whole, first_page)
    idxs = [i for i, l in enumerate(cleaned) if l == SENT]
    idxs.append(len(cleaned))
    # tile: each unit runs up to the verse before the next unit's start (same chapter or the next one)
    tiled = []
    for k2, (r, title, body) in enumerate(secs[1:]):
        nxt = next((x[0][0] for x in secs[k2 + 2:] if x[0]), None)
        if r and nxt and nxt > r[1] and (nxt[0] - r[1][0] <= 1) and nxt > r[0]:
            end = (nxt[0], nxt[1] - 1) if nxt[1] > 1 else (nxt[0] - 1, 999)
            if end > r[1]:
                r = (r[0], end)
        tiled.append((r, title, body))
    if tiled and tiled[-1][0]:
        tiled[-1] = ((tiled[-1][0][0], (36, 13)), tiled[-1][1], tiled[-1][2])   # last unit: to the end of the book
    secs = [secs[0]] + tiled
    final = [secs[0]]
    for (r, title, _), a, b in zip(secs[1:], idxs, idxs[1:]):
        body = "\n".join(cleaned[a + 1:b]).strip("\n")
        body = re.sub(r"\n{3,}", "\n\n", body)
        body = re.sub(r"(?m)^@@ ", " @@ ", body)
        final.append((r, title, body))
    final.append(("intro", "Abbreviations and glossary (end matter)", "\n".join(L[back:]).strip()))
    head = ["#source: doty",
            "#label: Brant Lee Doty, Numbers (Bible Study Textbook Series, College Press, 1973), scanned text. "
            "Churches-of-Christ teaching commentary: KJV text, his paraphrase, commentary, study questions. "
            "English (KJV) verse numbering. Private copy: paraphrase. Page numbers are printed pages."]
    lines = ["\n".join(head)]
    bad = 0
    for r, title, body in final:
        if r == "intro":
            rr = "intro"
        elif r is None:
            rr, bad = "intro", bad + 1
        else:
            rr = rng(*r)
        lines.append(f"@@ {rr} | {title[:140]}\n{body}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "doty.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"doty: {len(final)} sections ({bad} without a verse range)")


if __name__ == "__main__":
    main()
