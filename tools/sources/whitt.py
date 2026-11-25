"""William Whitt, Numbers: A new translation with commentary (Cutting Horse Press, 2022) -> sources/marked/whitt.txt

Usage:  python -I tools/sources/whitt.py

Reads sources/downloads/whitt/William Whitt.txt (copy of Bible/William Whitt.txt: an archive.org OCR of the
PDF; free on the Internet Archive and academia.edu, so the licence is the author's). Indexed in ENGLISH
(familiar) chapter numbers, because Whitt prints no verse numbers: the translation is set in paragraphs
(parashot) numbered P1, P2 ... with the Christian chapter in the margin ([Ch. N]).

  - translator's note and the composition-history essay: `intro` (with [p. N] printed pages)
  - the translation: one section per chapter (`N`), text flattened into sentences-as-lines
  - the notes and comments: one section per note, keyed by his label (P-number, optional setumah
    subunit, margin letter: "15,4c"), indexed to the chapter its paragraph sits in

Masoretic paragraph marks, as Whitt prints them and as kept here:
  petuhah (open parashah): he prints a triple line break and a double asterisk (**). The OCR turned most
      of those marks into noise ("Ey", "Cy", "+" ...), so every short noise line standing alone between
      blank lines is rewritten here as a line `**` : treat it as "a petuhah break near here", not a count.
  setumah (closed parashah): a single break and an em-dash; kept as lines starting with an em-dash.
The margin labels (P-numbers, [Ch. N], note letters a, b, c) were read into the text by the OCR; the P and
chapter labels are stripped from the line ends, the note letters stay.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "sources" / "downloads" / "whitt"
OUT = ROOT / "sources" / "marked"

NOISE = {"+", "Ey", "Cy", "Cry", "cy", "*%*", "*%", "4%", "Cr", "ee", "Ee", "Č", "ae", "ey", "**", "*", "cy ", "Cr y"}
LABEL_ONLY = re.compile(r"^(?:P\d+(?:,\d+)?\s*[a-z]{0,2}\s*)+$")
CH = re.compile(r"\[Ch\.?\s*(\d+)\]")
TRAIL = re.compile(r"\s*\bP\d+(?:,\d+)?\b(?:\s*\[Ch\.?\s*\d+\])?\s*(?:[a-z]\b\s*)*$")
NOTE_KEY = re.compile(r"^(\d{1,3})(?:,(\d{1,2}))?([a-z]{1,2})\s+(\S.*)$")
HEAD_NOTES = re.compile(r"^(?:NOTES AND COMMENTS (\d+)|(\d+) NOTES AND COMMENTS)\s*$")
HEAD_COMP = re.compile(r"^(?:THE COMPOSITION HISTORY OF NUMBERS (\d+)|(\d+) THE COMPOSITION HISTORY OF NUMBERS)\s*$")


def find(lines, pred, start=0):
    return next(i for i in range(start, len(lines)) if pred(lines[i].strip()))


def with_pages(lines, head_rx):
    """Running heads sit after their page's text: write [p. N+1] there, [p. first] at the top."""
    out, first = [], None
    for l in lines:
        m = head_rx.match(l.strip())
        if m:
            n = int(m[1] or m[2])
            if first is None:
                first = n
                out.insert(0, f"[p. {n}]")
            out += ["", f"[p. {n + 1}]"]
            continue
        out.append(l.rstrip())
    return out


def tidy(lines):
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip("\n")
    return re.sub(r"(?m)^@@ ", " @@ ", text)


def sentences(lines):
    """Flatten a chapter's OCR lines: a line starts a new row after sentence-final punctuation + capital."""
    rows, cur = [], ""
    for l in lines:
        s = l.strip()
        if not s:
            continue
        if s == "**" or s.startswith(("—", "“—")):
            if cur:
                rows.append(cur)
                cur = ""
            if s == "**":
                rows.append("**")
                continue
        if cur and re.search(r"[.?!:”’\"]$", cur) and re.match(r"^[“\"‘A-Z—]", s):
            rows.append(cur)
            cur = s
        else:
            cur = (cur + " " + s).strip() if cur else s
    if cur:
        rows.append(cur)
    return rows


# last verse of each chapter, Hebrew numbering (as in levine.py)
CHMAX = {1: 54, 2: 34, 3: 51, 4: 49, 5: 31, 6: 27, 7: 89, 8: 26, 9: 23, 10: 36, 11: 35, 12: 16, 13: 33,
         14: 45, 15: 41, 16: 35, 17: 28, 18: 32, 19: 22, 20: 29, 21: 35, 22: 41, 23: 30, 24: 25, 25: 18,
         26: 65, 27: 23, 28: 31, 29: 40, 30: 17, 31: 54, 32: 42, 33: 56, 34: 29, 35: 34, 36: 13}


def next_verse(c, v):
    return (c, v + 1) if v < CHMAX[c] else (c + 1, 1)


def paragraph_bounds():
    """Whitt's paragraphs are the Masoretic ones: P<n> starts after the (n-1)th petuhah and runs to the
    nth; the closed parashot (setumot) inside it are P<n>,1  P<n>,2 ... . Reads candidate-boundaries.md
    (OSHB/morphhb markers, Hebrew numbering). Whitt follows the Aleppo Codex, which has two fewer petuhot
    than morphhb, so the numbering can drift by a paragraph or two late in the book."""
    f = ROOT / "candidate-boundaries.md"
    if not f.exists():
        return None
    rows = [(int(m[1]), int(m[2]), m[3]) for m in
            re.finditer(r"^\|\s*\d+\s*\|\s*Num (\d+):(\d+)\s*\|\s*(petuhah|setumah)", f.read_text("utf-8"), re.M)
            for m in [re.match(r"(\d+)\|(\d+)\|(\w+)", f"{m[1]}|{m[2]}|{m[3]}")]]
    paras, start, segs = [], (1, 1), []
    seg_start = start
    for c, v, kind in rows:
        segs.append((seg_start, (c, v)))
        seg_start = next_verse(c, v) if (c, v) != (36, 13) else (36, 13)
        if kind == "petuhah":
            paras.append(segs)
            segs = []
    if segs:
        paras.append(segs)
    return paras


def note_range(paras, n, sub):
    """English-numbered range string for Whitt's paragraph n, subunit sub (0 = the paragraph's first part)."""
    if not paras or not (1 <= n <= len(paras)):
        return None
    segs = paras[n - 1]
    if sub >= len(segs):
        a, b = segs[0][0], segs[-1][1]
    else:
        a, b = segs[sub]
    sys.path.insert(0, str(ROOT / "tools"))
    import split_sources as ss
    table = ss.heb_to_eng()
    ra, rb = ss.to_english((a[0] * 1000 + a[1], b[0] * 1000 + b[1]), table)
    ca, va, cb, vb = ra // 1000, ra % 1000, rb // 1000, rb % 1000
    if (ca, va) == (cb, vb):
        return f"{ca}:{va}"
    return f"{ca}:{va}-{vb}" if ca == cb else f"{ca}:{va}-{cb}:{vb}"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    f = next(SRC.glob("*.txt"))
    L = f.read_text(encoding="utf-8", errors="replace").split("\n")
    i_tn = find(L, lambda s: s.lower().startswith("translator’s note to the reader") or s.lower().startswith("translator's note to the reader"), 100)
    i_tr = find(L, lambda s: s.startswith("Numbers 37732"), i_tn) + 1
    i_notes = find(L, lambda s: s == "Notes and comments", i_tr + 3000)
    i_comp = find(L, lambda s: s == "The composition history of Numbers", i_notes)
    i_schema = next((i for i in range(i_comp + 500, len(L)) if L[i].strip().startswith("SCHEMA FOR THE COMPOSITION")), len(L))
    # the upside-down schema chart near the end is OCR garbage; stop at its first line of noise
    i_noise = next((i for i in range(i_comp + 1500, len(L)) if re.match(r"^\d+\s+\d+\s*$|^[^\x00-\x7f\w\s]{3,}", L[i].strip())), i_schema)
    secs = []

    # ---- intro: translator's note
    secs.append(("intro", "Translator's note to the reader (OCR, roman page numbers dropped)", tidy(L[i_tn:i_tr - 1])))

    # ---- translation by chapter
    # Whitt prints no verse numbers, and the OCR scattered his margin labels (P-numbers, [Ch. N]) through the
    # text, so chapter breaks cannot be read off the page. They are placed by proportion instead: the
    # translation's length is mapped onto the JPS text of the same book (chapter by chapter), corrected at
    # landmarks (first appearance of a name whose verse is known). Boundaries are good to a few verses; each
    # chapter section is padded by PAD lines on both sides, so a verse near an edge still finds its text.
    body = L[i_tr:i_notes]
    rows = []                      # cleaned lines: (text) without margin noise
    for l in body:
        s = l.strip()
        if not s:
            rows.append("")
            continue
        if LABEL_ONLY.match(s) or re.fullmatch(r"\[Ch\.?\s*\d+\](?:\s*[a-z])?", s) or re.fullmatch(r"\d+ P\d+.*", s):
            continue
        s = CH.sub("", s)
        s = TRAIL.sub("", s).strip()
        rows.append(s)
    out = []
    nbreak = 0
    for k, s in enumerate(rows):
        alone = (k == 0 or not rows[k - 1]) and (k + 1 >= len(rows) or not rows[k + 1])
        if s in NOISE and alone:
            out.append("**")
            nbreak += 1
        elif re.fullmatch(r"[a-z]{1,2}( [a-z]{1,2})?", s) and alone:
            continue                      # a lone margin letter
        else:
            out.append(s)
    sent = sentences(out)                 # list of rows (sentence-ish lines), "**" kept
    cum, tot = [], 0
    for s in sent:
        cum.append(tot)
        tot += len(s) + 1

    sys.path.insert(0, str(ROOT / "tools"))
    import split_sources as ss
    e2h = ss.eng_to_heb()
    jps = ROOT / "sources" / "marked" / "jps.txt"
    vlen = {}                             # (hebrew chapter, verse) -> length
    if jps.exists():
        for m in re.finditer(r"^@@ (\d+):(\d+) \|[^\n]*\n(.*?)(?=^@@ |\Z)", jps.read_text("utf-8"), re.M | re.S):
            vlen[(int(m[1]), int(m[2]))] = len(m[3])
    else:
        vlen = {(c, v): 150 for c, n in CHMAX.items() for v in range(1, n + 1)}
    order = sorted(vlen)
    cumv, tv = {}, 0
    for k in order:
        cumv[k] = tv
        tv += vlen[k]

    def heb_key(c, v):                    # English chapter:verse -> JPS (Hebrew) verse key
        h = e2h.get(c * 1000 + v, c * 1000 + v)
        return (h // 1000, h % 1000)

    # landmarks: (Whitt spelling, English chapter, verse of its first appearance in Numbers)
    LAND = [("naziyr", 6, 2), ("Hovav", 10, 29), ("Yehoshua", 11, 28), ("Eldad", 11, 26), ("Miryam", 12, 1),
            ("Hoshea", 13, 8), ("Qadesh", 13, 26), ("Qorah", 16, 1), ("Edom", 20, 14), ("Siyhon", 21, 21),
            ("Bil‘am", 22, 5), ("Piynehas", 25, 7), ("Zimriy", 25, 14), ("Tzelophhad", 26, 33)]
    anchors = [(0.0, 0.0), (1.0, 1.0)]    # (fraction of JPS, fraction of Whitt)
    used = []
    for term, c, v in LAND:
        hit = next((k for k, s in enumerate(sent) if term in s), None)
        key = heb_key(c, v)
        if hit is None or key not in cumv:
            continue
        fj, fw = cumv[key] / tv, cum[hit] / tot
        if abs(fj - fw) < 0.04:
            anchors.append((fj, fw))
            used.append(term)
    anchors = sorted(set(anchors))
    mono = [anchors[0]]
    for a in anchors[1:]:
        if a[1] > mono[-1][1] and a[0] > mono[-1][0]:
            mono.append(a)
    anchors = mono

    def to_whitt(fj):
        for (a0, w0), (a1, w1) in zip(anchors, anchors[1:]):
            if a0 <= fj <= a1:
                return w0 + (w1 - w0) * (fj - a0) / (a1 - a0 or 1)
        return fj

    PAD = 20
    starts_f = []
    for c in range(1, 37):
        key = heb_key(c, 1)
        starts_f.append(to_whitt(cumv.get(key, 0) / tv) if c > 1 else 0.0)
    starts_f.append(1.0)
    line_at = lambda f: next((k for k, x in enumerate(cum) if x / tot >= f), len(sent))
    nsent = len(sent)
    good = []
    for c in range(1, 37):
        a, b = line_at(starts_f[c - 1]), line_at(starts_f[c])
        a2, b2 = max(0, a - PAD), min(nsent, b + PAD)
        secs.append((str(c), f"Whitt translation, Numbers {c} (English chapter; no verse numbers; edges placed by "
                             f"proportion, padded {PAD} lines each side)", tidy(sent[a2:b2])))
        good.append(c)
    pmap = {}
    print(f"  whitt landmarks used: {used}")

    # ---- notes
    notes = with_pages(L[i_notes + 1:i_comp], HEAD_NOTES)
    starts, prev = [], 0
    for i, l in enumerate(notes):
        m = NOTE_KEY.match(l.strip())
        if m and int(m[1]) >= 1 and (not starts or 0 <= int(m[1]) - prev <= 12):
            starts.append((i, m))
            prev = int(m[1])
    lead = notes[:starts[0][0]] if starts else notes
    secs.append(("intro", "Notes and comments: how Whitt works (method, sources, parashot)", tidy(lead)))
    unmapped = 0
    bounds = paragraph_bounds()
    for k, (i, m) in enumerate(starts):
        j = starts[k + 1][0] if k + 1 < len(starts) else len(notes)
        n = int(m[1])
        sub = int(m[2]) if m[2] else 0
        rng = note_range(bounds, n, sub)
        if rng is None:
            c = pmap.get(n)
            if c is None:
                lo = max((x for x in pmap if x <= n), default=None)
                c = pmap.get(lo)
            rng = str(c) if c else "intro"
            unmapped += 1
        key = f"{n}" + (f",{m[2]}" if m[2] else "") + m[3]
        lem = re.split(r":\s", m[4], maxsplit=1)[0][:60]
        # The paragraph numbering drifts by one or two against morphhb (Aleppo vs Leningrad breaks), so the
        # verse range is only approximate: index by the whole chapters it touches, keep the guess in the title.
        approx = ""
        mc = re.fullmatch(r"(\d+)(?::\d+)?(?:-(?:(\d+):)?\d+)?", rng)
        if mc and ":" in rng:
            approx = f" (approx. {rng})"
            c1 = int(mc[1])
            c2 = int(mc[2]) if mc[2] else c1
            rng = str(c1) if c1 == c2 else f"{c1}-{c2}"
        secs.append((rng, f"Whitt note P{key}{approx}: {lem}", tidy(notes[i:j])))

    # ---- composition history
    comp = with_pages(L[i_comp + 1:i_noise], HEAD_COMP)
    secs.append(("intro", "The composition history of Numbers (Whitt's essay, pp. 167-199)", tidy(comp)))

    head = ["#source: whitt",
            "#label: William Whitt, Numbers: A new translation with commentary (The Cutting Horse Press, 2022), "
            "archive.org OCR. Indexed by ENGLISH chapter (no verse numbers in the source; paragraph labels P1.. "
            "dropped from the lines). Masoretic marks: ** = petuhah break (OCR noise rewritten), line starting with an "
            "em-dash = setumah. Margin note letters stay in the text. Notes carry his label (P15,4c). Free from "
            "the author; still paraphrase, do not quote at length."]
    parts = ["\n".join(head)]
    for r, t, b in secs:
        if b.strip():
            parts.append(f"@@ {r} | {t}\n{b}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "whitt.txt").write_text("\n".join(parts) + "\n", encoding="utf-8", newline="\n")
    print(f"whitt: {len(secs)} sections; chapters {len(good)}; {len(starts)} notes ({unmapped} mapped by nearest P); "
          f"P labels mapped {len(pmap)} (max P{max(pmap) if pmap else 0}); petuhah noise marks {nbreak}")


if __name__ == "__main__":
    main()
