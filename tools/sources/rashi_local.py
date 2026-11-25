"""Rashi on Numbers (Sefaria export, local copy) -> sources/marked/rashi.txt

Usage:  python -I tools/sources/rashi_local.py

Input: sources/downloads/rashi/Rashi on Numbers - en - merged.txt (copied from Downloads;
untrusted, read as plain text only). Layout: a header, then "Chapter N" and "Verse M" lines,
each followed by that verse's comments, one per line (Hebrew lemma, then the English).
English translation: Rosenbaum and Silbermann (1929-34), public domain. Hebrew (Masoretic)
numbering. The Hebrew-script lemmas stay in the source file; never quote them in chat or reader files.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "sources" / "downloads" / "rashi"
OUT = ROOT / "sources" / "marked"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    f = next(SRC.glob("*.txt"))
    ch, v, cur, secs = 0, 0, [], []

    def flush():
        txt = "\n".join(x for x in cur if x.strip()).strip()
        if ch and v and txt:
            secs.append((ch, v, txt))

    started = False
    for line in f.read_text(encoding="utf-8").split("\n"):
        s = line.strip()
        m = re.fullmatch(r"Chapter (\d+)", s)
        if m:
            flush()
            ch, v, cur, started = int(m[1]), 0, [], True
            continue
        m = re.fullmatch(r"Verse (\d+)", s)
        if m and started:
            flush()
            v, cur = int(m[1]), []
            continue
        if started and v:
            cur.append(re.sub(r"[ \t]+", " ", s))
    flush()
    label = ("Rashi on Numbers, English translation by M. Rosenbaum and A.M. Silbermann (1929-34), via Sefaria "
             "export (public domain). Hebrew (Masoretic) numbering. Hebrew-script lemmas stay in the text.")
    out = ["#source: rashi", f"#label: {label}", "#numbering: hebrew"]
    for c, vv, txt in secs:
        out += [f"@@ {c}:{vv} | Rashi on {c}:{vv}", txt]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "rashi.txt").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    chs = sorted({c for c, _, _ in secs})
    print(f"rashi: {len(secs)} verse sections, chapters {chs[0]}-{chs[-1]} ({len(chs)})")


if __name__ == "__main__":
    main()
