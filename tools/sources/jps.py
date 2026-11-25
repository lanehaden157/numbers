"""JPS Tanakh (gender-sensitive), Sefaria export -> sources/marked/jps.txt

Usage:  python -I tools/sources/jps.py Leviticus

Input: Personal/Biblical Texts/Torah/<Book> - en - merged.plain.txt (one line per verse
under "Chapter N"; Hebrew numbering). Sefaria's export runs the footnotes into the
verse text as  "<word> <letter> <lemma> <note>" (lemma repeats the words just before
the letter). They are pulled out as "[note: lemma: note]" right after the lemma.
The note's end is a heuristic (first sentence end that is not an abbreviation); a few
longer notes may leave a tail in the verse text.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sources" / "marked"
SRC = Path(r"C:\Users\laneh\OneDrive\Documents\Personal\Biblical Texts\Torah")
ABBR = {"heb", "lit", "cf", "v", "vv", "e.g", "i.e", "mss", "ch", "chs", "num", "exod", "gen", "lev", "deut",
        "ibid", "esp", "sam", "kgs", "ps", "isa", "jer", "ezek", "cp", "mt", "vs", "ff", "no", "nos", "pl", "sing"}
MAXLEMMA = 10


def strip_p(w):
    return re.sub(r"^[^\w]+|[^\w]+$", "", w).lower()


CONT = re.compile(r"\s*(Exact meaning|Meaning of|Cf\.|See |Where a human|Traditionally|Precise|Heb\.|Lit\.|In contrast|Trad\.)")


def note_end(s):
    e = note_end1(s)
    while e < len(s) and CONT.match(s[e:]):
        e += note_end1(s[e:])
    return e


def note_end1(s):
    """Index in s where one note sentence ends (after its closing period)."""
    for m in re.finditer(r"[.!?][”’\"')\]]*(?=\s|$)", s):
        pre = re.search(r"([\w.]+)$", s[:m.start()])
        word = pre.group(1).lower().rstrip(".") if pre else ""
        if word in ABBR or re.fullmatch(r"[a-z]", word) and m.start() < 3:
            continue
        return m.end()
    return len(s)


def extract_notes(line):
    toks = line.split(" ")
    out, notes, i = [], [], 0
    while i < len(toks):
        t = toks[i]
        if re.fullmatch(r"[a-z]", t) and out:
            hit = None
            for k in range(min(MAXLEMMA, len(out)), 0, -1):
                after = toks[i + 1:i + 1 + k]
                if len(after) == k and [strip_p(x) for x in after] == [strip_p(x) for x in out[-k:]] \
                        and all(strip_p(x) for x in after):
                    hit = k
                    break
            if hit:
                rest = " ".join(toks[i + 1 + hit:])
                e = note_end(rest)
                note, tail = rest[:e].strip(), rest[e:].strip()
                lemma = " ".join(toks[i + 1:i + 1 + hit])
                out.append(f"[note {t}: {lemma} — {note}]")
                notes.append(note)
                toks = toks[:i + 1] + (tail.split(" ") if tail else [])
                # continue after the marker; tokens consumed
                i += 1
                continue
        out.append(t)
        i += 1
    return " ".join(out)


def join_continuations(lines):
    """Numbers export: the divine name sits alone on a line ("G OD ") and the rest of the verse
    follows on a line that starts with a space. Join any line starting with a space to the verse
    line before it, and drop blank lines."""
    out, pending = [], ""
    for l in lines:
        if not l.strip():
            continue
        if re.match(r"^[a-z] (In some editions|This verse is labeled)", l) and len(l) < 140 \
                and re.search(r"(below|in some editions)\.\s*$", l):
            pending = l.strip() + " "       # a verse-numbering note on a line of its own (Num 17:1, 17:16)
            continue
        if out and l[0] == " " and not re.match(r"^Chapter \d+\s*$", out[-1]):
            out[-1] = out[-1].rstrip() + " " + l.strip()
            continue
        if pending and not l.startswith("Chapter"):
            l, pending = pending + l, ""
        out.append(l)
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    book = sys.argv[1]
    src = SRC / f"{book} - en - merged.plain.txt"
    lines = join_continuations(src.read_text(encoding="utf-8").split("\n"))
    out = [f"#source: jps",
           f"#label: JPS Tanakh, gender-sensitive edition (Jewish Publication Society, via Sefaria export). "
           "Copyrighted: quote sparingly, a phrase at most. Hebrew (Masoretic) numbering. Footnotes pulled "
           "out as [note ...].",
           "#numbering: hebrew"]
    ch, v, perch, nnotes = 0, 0, {}, 0
    for l in lines:
        m = re.match(r"^Chapter (\d+)\s*$", l)
        if m:
            ch, v = int(m[1]), 0
            continue
        if not ch or not l.strip():
            continue
        v += 1
        perch[ch] = v
        txt = extract_notes(l.strip())
        nnotes += txt.count("[note ")
        txt = re.sub(r"\bG OD\b", "GOD", txt)
        out += [f"@@ {ch}:{v} | {ch}:{v}", txt]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "jps.txt").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print(f"jps: {sum(perch.values())} sections, {nnotes} notes, chapters {len(perch)}; verses per chapter {perch}")


if __name__ == "__main__":
    main()
