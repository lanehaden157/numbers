"""Dr. Thomas Constable's Notes -> sources/marked/constable.txt

Usage:  python -I tools/sources/constable.py Leviticus

Downloads the PDF once into sources/downloads/constable/ (untrusted: read only with
pymupdf under -I), converts to text, indexes by his outline headings
("The burnt offering ch. 1", "... 1:3-9") and by his bare verse lines ("15:5-9").
Introduction, outline, appendix, bibliography -> intro. English verse numbering.
"""
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DL = ROOT / "sources" / "downloads" / "constable"
OUT = ROOT / "sources" / "marked"
URLS = ["https://soniclight.com/tcon/notes/pdf/{f}.pdf",
        "https://planobiblechapel.org/tcon/notes/pdf/{f}.pdf"]
FIXES = {"23:33-444": "23:33-44"}  # typos in the PDF headings
DASH = r"[–—-]"
REF = rf"\d+(?::\d+)?(?:\s*{DASH}\s*\d+(?::\d+)?)?"
HEAD = re.compile(rf"^(?P<title>[A-Z'\"].{{2,120}}?)\s+(?P<chs>(?:CHS?\.)\s*)?(?P<ref>{REF})\s*$", re.I)
VERSE = re.compile(rf"^(?P<ref>\d+:\d+(?:\s*{DASH}\s*\d+(?::\d+)?)?)\s*$")
BOOKREF = re.compile(r"^(?:[123] ?)?(?:Gen|Exod|Lev|Num|Deut|Josh|Judg|Ruth|Sam|Kgs|Kings|Chron|Ps|Prov|Isa|Jer|Ezek|Dan|Hos|Matt|Mark|Luke|John|Acts|Rom|Cor|Gal|Eph|Heb|Pet|Rev)\.?\s*\d")
NOISE = re.compile(r"^(Dr\. Constable's Notes on \w+|\d{4} Edition)$")


def norm(ref):
    ref = FIXES.get(ref.strip(), ref.strip())
    return re.sub(rf"\s*{DASH}\s*", "-", ref)


def fetch(book):
    f = DL / f"{book.lower()}.pdf"
    if f.exists():
        return f
    local = sorted(DL.glob("*.pdf"))   # a PDF copied here by hand (e.g. from Downloads)
    if local:
        return local[0]
    DL.mkdir(parents=True, exist_ok=True)
    for u in URLS:
        time.sleep(1)
        req = urllib.request.Request(u.format(f=book.lower()), headers={"User-Agent": "bible-study-fetch"})
        data = urllib.request.urlopen(req, timeout=120).read()
        if data[:4] == b"%PDF":
            f.write_bytes(data)
            return f
    raise SystemExit("no PDF found")


def lines_of(pdf):
    import pymupdf
    out, expect = [], 1
    for page in pymupdf.open(pdf):
        for l in page.get_text().split("\n"):
            s = l.strip()
            if not s or NOISE.match(s):
                continue
            if s.isdigit() and 1 <= int(s) <= 999 and int(s) in (expect, expect + 1):
                expect = int(s) + 1
                out.append(f"[p. {s}]")
                continue
            out.append(s)
    return out


def reflow(lines):
    """Join wrapped lines; a short line ending a sentence closes the paragraph."""
    paras, cur = [], []
    for s in lines:
        if s.startswith("[p. "):
            if cur:
                paras.append(" ".join(cur)); cur = []
            paras.append(s)
            continue
        if re.match(r"^\d{1,2}[A-Z]", s) and not cur:   # footnote line
            paras.append(s)
            continue
        cur.append(s)
        if len(s) < 70 and re.search(r"[.?!:”\"')\]]\d*$", s):
            paras.append(" ".join(cur)); cur = []
    if cur:
        paras.append(" ".join(cur))
    return "\n\n".join(p for p in paras if p)


def _span(ref):
    m = re.fullmatch(r"(\d+)(?::(\d+))?(?:-(?:(\d+):)?(\d+))?", ref)
    if not m:
        return None
    c1, v1, c2, x = m.groups()
    if v1 is None:                                  # whole chapter(s)
        return (int(c1), 1), (int(x or c1), 999)
    if x is None:
        return (int(c1), int(v1)), (int(c1), int(v1))
    return (int(c1), int(v1)), (int(c2 or c1), int(x))


def fill_gaps(secs):
    """Constable gives no verse line for some stretches (e.g. 23:27-24:14), so the text sits under the
    previous heading. Extend a section's end to the verse before the next section's start when the
    next one starts later than the end (one level only; parents that span their children are left)."""
    out = [list(s) for s in secs]
    prev = None
    for s in out:
        sp = _span(s[0]) if s[0] != "intro" else None
        if sp is None:
            continue
        if prev is not None:
            ps, pe = _span(prev[0])
            nxt = sp[0]
            if (pe[1] != 999 and nxt > ps and nxt > pe and (nxt[0] - pe[0] <= 1)
                    and not (nxt[1] == 1 and nxt[0] == pe[0] + 1)):
                end = (nxt[0], nxt[1] - 1) if nxt[1] > 1 else (nxt[0] - 1, 999)
                if end > pe:
                    prev[0] = f"{ps[0]}:{ps[1]}-{end[0]}:{end[1]}"
        prev = s
    return [tuple(s) for s in out]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    book = sys.argv[1]
    L = lines_of(fetch(book))
    body = next(i for i, l in enumerate(L) if l == "Exposition")
    end = next((i for i, l in enumerate(L) if i > body and l in ("Appendix", "Bibliography")), len(L))
    marks = []  # (index, kind, ref, title)
    for i in range(body + 1, end):
        s = L[i]
        m = VERSE.match(s)
        if m and not L[i - 1].endswith(("cf.", "vv.", "v.")):
            marks.append((i, "v", norm(m["ref"]), s))
            continue
        m = HEAD.match(s)
        if m and len(s) < 160 and not re.search(r"\bvv?\.", s) and not BOOKREF.match(s):
            ref = m["ref"]
            if ":" not in ref and not m["chs"]:
                continue
            if s.count("(") != s.count(")"):
                continue
            marks.append((i, "h", norm(ref), s))
    secs = [("intro", "Introduction, outline, message", reflow(L[:body]))]
    if end < len(L):
        secs.append(("intro", "Appendix and bibliography", reflow(L[end:])))
    parent = ""
    for k, (i, kind, ref, title) in enumerate(marks):
        j = marks[k + 1][0] if k + 1 < len(marks) else end
        text = reflow(L[i + 1:j])
        if kind == "h":
            parent = title
            secs.append((ref, title, text))
        else:
            secs.append((ref, f"{ref} (under: {parent})" if parent else ref, text))
    secs = fill_gaps(secs)
    lines = [f"#source: constable", f"#label: Dr. Thomas L. Constable, Notes on {book} (2015 Edition, local PDF copy of the "
             "soniclight.com notes). English verse numbering. Bible-teacher notes: weigh "
             "as popular evangelical commentary; paraphrase."]
    secs = [x for x in secs if x[2].strip()]
    for ref, title, text in secs:
        lines += [f"@@ {ref} | {title}", text]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "constable.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    chs = set()
    for ref, _, _ in secs:
        if ref == "intro":
            continue
        a = re.findall(r"(\d+)(?::\d+)?", ref)
        chs.update(range(int(a[0]), int(a[-1]) + 1) if "-" in ref and ":" not in ref.split("-")[1] and ":" not in ref
                   else {int(a[0]), int(a[-1])} if ":" in ref.split("-")[-1] and "-" in ref else {int(a[0])})
    print(f"constable: {len(secs)} sections; chapters touched {sorted(chs)}")


if __name__ == "__main__":
    main()
