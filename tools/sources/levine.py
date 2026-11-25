"""Levine, Numbers (Anchor Bible 4A 1993, 4B 2000) OCR text -> sources/marked/levine-1.txt, levine-2.txt

Usage:  python -I tools/sources/levine.py [levine-1] [levine-2]

Reads sources/downloads/levine-1/*.txt (Numbers 1-20) and levine-2/*.txt (Numbers 21-36), copies of
the Downloads files (untrusted: plain text only). Both are OCR of the printed books.

What is indexed, in Hebrew (Masoretic) verse numbering, which Levine uses (Eng 16:36-50 = his 17:1-15):
  - the introduction to the book (all `intro`, split at its lettered headings), with [p. N] markers
  - per unit: the opening essay (unit range), the TRANSLATION verse by verse (`Translation c:v`),
    the NOTES note by note (`Note c:v lemma`), the COMMENT essays (range = the unit's verses)
  - NOT indexed: the front-matter copy of the whole translation (it repeats the body), the maps,
    the subject/author/sources indexes.
Printed page numbers become `[p. N]` lines (a page number alone on a line, followed by the running
head; the number opens that page). Verse splitting follows the sequence of verse numbers, so an OCR
slip can glue a verse onto its neighbour: see work/sources-local-notes.md.
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DL = ROOT / "sources" / "downloads"
OUT = ROOT / "sources" / "marked"

# last verse of each chapter, Hebrew numbering (Eng 16:36-50 = Heb 17:1-15, Eng 29:40 = Heb 30:1 ...)
CHMAX = {1: 54, 2: 34, 3: 51, 4: 49, 5: 31, 6: 27, 7: 89, 8: 26, 9: 23, 10: 36, 11: 35, 12: 16, 13: 33,
         14: 45, 15: 41, 16: 35, 17: 28, 18: 32, 19: 22, 20: 29, 21: 35, 22: 41, 23: 30, 24: 25, 25: 18,
         26: 65, 27: 23, 28: 31, 29: 40, 30: 17, 31: 54, 32: 42, 33: 56, 34: 29, 35: 34, 36: 13}

VOL = {
    "levine-1": dict(
        glob="abNumbers1-20*.txt", intro=r"^A\. THE CASTING OF THE WILDERNESS", body=r"^NUMBERS 1-4:$",
        end=r"^Map I$", run=r"^NUMBERS 1-20$",
        label="Levine, Numbers 1-20 (Anchor Bible 4A, Doubleday, 1993). OCR text, Hebrew (Masoretic) verse "
              "numbering. Private copy: paraphrase, never quote at length."),
    "levine-2": dict(
        glob="Numbers 21-36*.txt", intro=r"^INTRODUCTION TO THE BOOK\s*$", body=r"^PART I\.$",
        end=r"SUBJECT INDEX", run=r"^NUMBERS 21-36$",
        label="Levine, Numbers 21-36 (Anchor Bible 4B, Doubleday, 2000). OCR text, Hebrew (Masoretic) verse "
              "numbering. Private copy: paraphrase, never quote at length."),
}

DIG = {"l": "1", "I": "1", "|": "1", "!": "1", "O": "0"}


def num(tok):
    return int("".join(DIG.get(c, c) for c in tok))


def is_caps(s):
    s = s.strip()
    return len(re.findall(r"[A-Za-z]", s)) >= 3 and not re.search(r"[a-z]", s)


# ------------------------------------------------------------------ pages and running heads
def paginate(lines, runhead):
    """Replace page numbers with [p. N] lines and drop running heads. lines: list of str."""
    n = len(lines)

    def next_nb(i):
        j = i + 1
        while j < n and not lines[j].strip():
            j += 1
        return j

    def prev_nb(i):
        j = i - 1
        while j >= 0 and not lines[j].strip():
            j -= 1
        return j

    cnt = Counter()
    for i, l in enumerate(lines):
        if re.fullmatch(r"\d{1,3}", l.strip()):
            j = next_nb(i)
            if j < n and len(lines[j].strip()) < 70 and not lines[j].strip().isdigit():
                cnt[lines[j].strip()] += 1
    heads = {h for h, c in cnt.items() if c >= 2 and not re.match(r"^\d+[.)]", h)}
    heads.add(runhead)
    out, last, drop = [], None, set()
    for i, l in enumerate(lines):
        s = l.strip()
        if i in drop:
            continue
        part = re.fullmatch(r"PART [IVX]+\.?", s) is not None
        if (s in heads and s != "") or part:
            p = prev_nb(i)
            prevs = lines[p].strip() if p >= 0 else ""
            m = re.fullmatch(r"\d{1,3}", prevs)
            if m and 0 < int(prevs) < 800 and (last is None or last < int(prevs) <= last + 12):
                last = int(prevs)
                # the page number line was already copied: replace it
                k = len(out) - 1
                while k >= 0 and not out[k].strip():
                    k -= 1
                out[k] = f"[p. {last}]"
            elif p >= 0 and (m2 := re.search(r"[^\d\s](\d{1,3})$", prevs)) and (last is None or last < int(m2[1]) <= last + 3):
                last = int(m2[1])           # number glued to the end of the page's last line
                k = len(out) - 1
                while k >= 0 and not out[k].strip():
                    k -= 1
                out[k] = out[k].rstrip()[: -len(m2[1])]
                out.append("")
                out.append(f"[p. {last}]")
            if part:
                out.append(l)    # a part title is not a running head: keep it
            continue
        out.append(l)
    return out, last or 0


# ------------------------------------------------------------------ verse leaders
def match_verse(line, expected):
    """Line starts with verse number `expected` (OCR-tolerant)? -> rest of line, or None."""
    m = re.match(r"^([0-9lI|!O]{1,4})", line)
    if not m:
        return None
    run = m[1]
    for k in range(1, len(run) + 1):
        try:
            if num(run[:k]) != expected:
                continue
        except ValueError:
            continue
        rest = line[k:]
        if rest[:1] in ("", " ", "\t") or not rest[:1].isdigit():
            if rest[:1] in "1lI|" and rest[1:2].islower():
                rest = "I" + rest[1:]
            elif rest[:1] == "0" and rest[1:2].isalpha():
                rest = "O" + rest[1:]
            elif rest[:1].isdigit():
                continue
            return rest.strip()
    return None


NOTE_LEAD = re.compile(
    r"^(?:(?P<c>[0-9lIO]{1,2})\.?\s+)?(?P<v>[0-9lIO]{1,3})(?:\s*[-–]\s*(?P<v2>[0-9lIO]{1,3}))?[a-z]{0,2}\s?[.:]\s+(?P<rest>\S.*)$")


# ------------------------------------------------------------------ headings
def heading_title(lines, i, first):
    t = [first]
    j = i + 1
    while j < len(lines) and len(t) < 4:
        s = lines[j].strip()
        if s and is_caps(s) and len(s) < 70 and not s.startswith("[p."):
            t.append(s)
            j += 1
        else:
            break
    return re.sub(r"\s+", " ", " ".join(t)).strip(), j


UNIT = re.compile(r"^(?:PART [IVX]+\.?\s*)?NUMBERS (\d+)(?::(\d+))?(?:\s*[-–—]\s*(?:(\d+):)?(\d+))?\s*[:.]?\s*(.*)$")
TRANS = re.compile(r"^TRANSLATION(?:\s*(?:OF|-)?\s*NUMBERS (\d+)(?::(\d+)(?:\s*[-–]\s*(\d+))?)?)?\s*[:.]?$")
NOTES = re.compile(r"^NOTES(?: TO(?: NUMBERS)? (\d+)(?::(\d+)(?:\s*[-–]\s*(?:(\d+):)?(\d+))?)?)?\s*[:.]?\s*(.*)$")
COMMENT = re.compile(r"^COMMENTS?(?:\s+(\d+))?\s*[:.]?\s*(.*)$")
INTRO_CH = re.compile(r"^INTRODUCTION TO NUMBERS (\d+)\s*[:.]?$")


def rng_str(lo, hi):
    (c1, v1), (c2, v2) = lo, hi
    if (c1, v1) == (c2, v2):
        return f"{c1}:{v1}"
    if c1 == c2:
        return f"{c1}:{v1}-{v2}" if v2 != 999 else f"{c1}:{v1}-999" if v1 != 1 else f"{c1}"
    return f"{c1}:{v1}-{c2}:{v2}"


class Parser:
    def __init__(self, lines):
        self.L = lines
        self.secs = []          # (range str, title, [lines])
        self.stats = Counter()
        self.tverses = {}       # chapter -> verses found in translation
        self.nnotes = Counter()

    def add(self, rng, title, body):
        text = "\n".join(body).strip("\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"(?m)^@@ ", " @@ ", text)
        if text.strip():
            self.secs.append((rng, re.sub(r"\s+", " ", title).strip(), text))

    def lookahead_chapter(self, i):
        for j in range(i, min(i + 2500, len(self.L))):
            m = NOTES.match(self.L[j].strip()) if is_caps(self.L[j]) else None
            if m and m[1]:
                return int(m[1])
        return None

    def run(self):
        L, n = self.L, len(self.L)
        mode, rng, title0 = None, None, ""
        buf = []
        ch, vexp = 1, 1
        cur = None                # current verse key in translation / note
        unit_lo = unit_hi = None
        after_comment = False
        unit_ch_valid = False
        unit_rng = ((1, 1), (1, 999))
        prev_v = 0
        i = 0

        def bump(c, v):
            nonlocal unit_lo, unit_hi
            if unit_lo is None or (c, v) < unit_lo:
                unit_lo = (c, v)
            if unit_hi is None or (c, v) > unit_hi:
                unit_hi = (c, v)

        def flush():
            nonlocal buf, cur
            if mode == "intro":
                self.add(rng_str(*unit_rng), "Introduction: " + title0, buf)
            elif mode == "trans":
                if cur:
                    self.add(f"{cur[0]}:{cur[1]}", f"Translation {cur[0]}:{cur[1]}", buf)
                    self.tverses.setdefault(cur[0], set()).add(cur[1])
                else:
                    self.add(rng_str(*unit_rng), "Translation (before verse 1)", buf)
            elif mode == "notes":
                if cur:
                    c, v, v2, lem = cur
                    r = f"{c}:{v}" if not v2 else f"{c}:{v}-{v2}"
                    self.add(r, f"Note {r} {lem}", buf)
                    self.nnotes[c] += 1
                else:
                    self.add(rng or rng_str(*unit_rng), "Notes: " + title0, buf)
            elif mode == "comment":
                self.add(rng, title0, buf)
            buf, cur = [], None

        while i < n:
            raw = L[i]
            s = raw.strip()
            prev_blank = (i == 0 or not L[i - 1].strip() or L[i - 1].startswith("[p. ")
                          or re.fullmatch(r"PART [IVX]+\.?", L[i - 1].strip()) is not None)
            if s and prev_blank and is_caps(s) and len(s) < 120:
                # --- unit heading
                m = UNIT.match(s)
                if m and not re.fullmatch(r"NUMBERS \d+-\d+", s) or (m and (m[3] or m[4]) and not s.startswith(("NUMBERS 1-20", "NUMBERS 21-36"))):
                    flush()
                    c1, v1, c2, v2 = m[1], m[2], m[3], m[4]
                    c1 = int(c1)
                    if v1 is None and c2 is None and v2:
                        c2, v2 = v2, None            # NUMBERS 13-14
                    c2 = int(c2) if c2 else c1
                    lo = (c1, int(v1) if v1 else 1)
                    hi = (c2, int(v2) if v2 else 999)
                    title, j = heading_title(L, i, s)
                    if not (c2 == c1 and not v1 and not v2 and c1 > 36):
                        mode, unit_rng, title0 = "intro", (lo, hi), title
                        unit_lo = unit_hi = None
                        after_comment = False
                        unit_ch_valid = True
                        ch, vexp = c1, lo[1]
                        i = j
                        continue
                # --- translation
                m = TRANS.match(s)
                if m:
                    flush()
                    if after_comment:
                        unit_lo = unit_hi = None
                        after_comment = False
                    mode = "trans"
                    c = int(m[1]) if m[1] else (ch if unit_ch_valid else (self.lookahead_chapter(i) or ch))
                    ch, vexp = c, int(m[2]) if m[2] else 1
                    bump(ch, vexp)
                    i += 1
                    continue
                # --- notes
                m = NOTES.match(s)
                if m:
                    flush()
                    if after_comment:
                        unit_lo = unit_hi = None
                        after_comment = False
                    mode = "notes"
                    title, j = heading_title(L, i, s)
                    title0 = title
                    if m[1]:
                        ch = int(m[1])
                        v1 = int(m[2]) if m[2] else 1
                        c2 = int(m[3]) if m[3] else ch
                        v2 = int(m[4]) if m[4] else (999 if not m[2] else v1)
                        rng = rng_str((ch, v1), (c2, v2))
                        prev_v = v1 - 1
                        bump(ch, v1)
                        bump(c2, v2 if v2 != 999 else CHMAX.get(c2, 999))
                    else:
                        rng = None
                        prev_v = 0
                    i = j
                    continue
                # --- comment
                m = COMMENT.match(s)
                if m and mode in ("notes", "comment", "trans", "intro"):
                    flush()
                    title, j = heading_title(L, i, s)
                    mode, title0 = "comment", "COMMENT " + title[len("COMMENT"):].strip(" S:") if False else title
                    lo = unit_lo or unit_rng[0]
                    hi = unit_hi or unit_rng[1]
                    rng = rng_str(lo, hi)
                    after_comment = True
                    unit_ch_valid = False
                    i = j
                    continue
                m = INTRO_CH.match(s)
                if m:
                    flush()
                    c = int(m[1])
                    mode, unit_rng, title0 = "intro", ((c, 1), (c, 999)), s
                    ch, vexp = c, 1
                    i += 1
                    continue
            # ---------------- body lines
            if mode == "trans" and s and not s.startswith("[p. "):
                rest = None
                got = match_verse(s, vexp)
                new_ch = None
                if got is None and (vexp == 1 or vexp > CHMAX.get(ch, 999)):
                    mm = re.match(r"^(\d{1,2})\s*(.*)$", s)
                    if mm:
                        for c in ((ch, ch + 1) if vexp > CHMAX.get(ch, 999) else (ch,)):
                            if int(mm[1]) == c:
                                g = match_verse(mm[2], 1)
                                if g is not None:
                                    got, new_ch = g, c
                                    break
                skipped = 0
                if got is None and vexp <= CHMAX.get(ch, 999):
                    for d in (1, 2, 3):
                        g = match_verse(s, vexp + d)
                        if g is not None and (g == "" or re.match(r"[A-Z\u201c\"'(\[<]", g)) and vexp + d <= CHMAX.get(ch, 999):
                            got, skipped = g, d
                            break
                if got is not None and (new_ch or vexp <= CHMAX.get(ch, 999)):
                    vexp += skipped
                    flush()
                    if new_ch:
                        ch = new_ch
                        vexp = 1
                    cur = (ch, vexp)
                    bump(ch, vexp)
                    buf = [got] if got else []
                    vexp += 1
                    i += 1
                    continue
            if mode == "notes" and s and not s.startswith("[p. "):
                m = NOTE_LEAD.match(s)
                if m:
                    try:
                        v = num(m["v"])
                        c = num(m["c"]) if m["c"] else None
                        v2 = num(m["v2"]) if m["v2"] else None
                    except ValueError:
                        v = None
                    ok = v is not None and v >= 1
                    if ok and c is not None:
                        ok = c in (ch, ch + 1) and c <= 36
                    if ok:
                        cc = c if c is not None else ch
                        newch = cc != ch
                        pv = 0 if newch else prev_v
                        ok = v <= CHMAX.get(cc, 99) and v >= max(pv, 1) and v - pv <= 30 and \
                            (v2 is None or (v < v2 <= CHMAX.get(cc, 99)))
                        if ok and c is None and cur is None and v == 1 and pv > 1:
                            ok = False
                    if ok:
                        flush()
                        ch = cc
                        prev_v = v
                        lem = re.split(r"[.:]\s", m["rest"], maxsplit=1)[0][:50]
                        cur = (ch, v, v2, lem)
                        bump(ch, v)
                        buf = [s]
                        i += 1
                        continue
            buf.append(raw.rstrip())
            i += 1
        flush()


def convert(key):
    cfg = VOL[key]
    f = next((DL / key).glob(cfg["glob"]))
    text = f.read_text(encoding="utf-8", errors="replace").replace("\x0c", "")
    lines = [l.rstrip() for l in text.split("\n")]

    def find(pat, start=0):
        rx = re.compile(pat)
        return next(i for i in range(start, len(lines)) if rx.search(lines[i].strip()))

    # the intro starts after the front-matter copy of the translation
    i_intro = max(i for i, l in enumerate(lines[:7000]) if re.search(cfg["intro"], l.strip()) and i > 2000)
    i_body = find(cfg["body"], i_intro + 500)
    i_end = find(cfg["end"], i_body + 5000)
    paged, lastpage = paginate(lines[i_intro:i_end], cfg["run"])
    split = next(i for i, l in enumerate(paged) if re.fullmatch(cfg["body"], l.strip()))
    secs = []
    # introduction: split at lettered headings
    intro = paged[:split]
    heads = [k for k, l in enumerate(intro)
             if re.match(r"^[A-F]\. [A-Z]", l.strip()) and is_caps(l.strip()) and (k == 0 or not intro[k - 1].strip())]
    heads = heads or [0]
    if heads[0] != 0:
        heads = [0] + heads
    for a, b in zip(heads, heads[1:] + [len(intro)]):
        body = "\n".join(intro[a:b]).strip()
        if body:
            t = re.sub(r"\s+", " ", intro[a].strip())[:90]
            secs.append(("intro", "Introduction to the book: " + t, re.sub(r"(?m)^@@ ", " @@ ", re.sub(r"\n{3,}", "\n\n", body))))
    P = Parser(paged[split:])
    P.run()
    secs += P.secs
    head = [f"#source: {key}", f"#label: {cfg['label']}", "#numbering: hebrew"]
    parts = ["\n".join(head)]
    for r, t, b in secs:
        parts.append(f"@@ {r} | {t}\n{b}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{key}.txt").write_text("\n".join(parts) + "\n", encoding="utf-8", newline="\n")
    print(f"{key}: {len(secs)} sections, last page {lastpage}, "
          f"{sum(len(v) for v in P.tverses.values())} translation verses, {sum(P.nnotes.values())} notes")
    off = {c: (len(P.tverses.get(c, ())), m) for c, m in CHMAX.items()
           if c in P.tverses and len(P.tverses[c]) != m}
    miss = [c for c in range(1, 37) if c in P.tverses and sorted(set(range(1, CHMAX[c] + 1)) - P.tverses[c])]
    print("  chapters with translation verses missing:",
          {c: sorted(set(range(1, CHMAX[c] + 1)) - P.tverses[c])[:12] for c in miss})
    print("  chapters with notes:", sorted(P.nnotes), "| notes per chapter:", dict(sorted(P.nnotes.items())))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    keys = [a for a in sys.argv[1:] if a in VOL] or list(VOL)
    for k in keys:
        convert(k)


if __name__ == "__main__":
    main()
