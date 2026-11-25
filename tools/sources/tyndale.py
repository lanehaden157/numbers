"""Tyndale TOTHT (tagged Hebrew OT, CC BY 4.0) -> sources/marked/tyndale.txt

Usage:  python -I tools/sources/tyndale.py Leviticus

Input: Personal/Biblical Texts/Torah/TOTHT...Gen-Deu...txt, tab-separated:
  Ref in Heb | Eng ref | Pointed | Accented | Morphology | Extended Strongs
The file DOES carry pointed Hebrew (cols 3-4); the marked body has none: one line per
word  "NN translit | gloss | Strong's | grammar", where translit is made here from the
pointed text by a rough rule-based romanisation (reference only, not scholarly),
gloss/Strong's come from the extended-Strong's column (maqqef/sof-pasuq pieces H9014/H9016
dropped), grammar is the ETCBC/OSHB morphology code (HebrewMorphologyCodes, openscriptures).
Sections are per verse in ENGLISH numbering (Eng ref column), so Eng 6:1 holds Heb 5:20.
"""
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sources" / "marked"
SRC = Path(r"C:\Users\laneh\OneDrive\Documents\Personal\Biblical Texts\Torah")
ABBR = {"Genesis": "Gen", "Exodus": "Exo", "Leviticus": "Lev", "Numbers": "Num", "Deuteronomy": "Deu"}

LET = {"א": "ʼ", "ב": "v", "ג": "g", "ד": "d", "ה": "h", "ו": "w", "ז": "z", "ח": "ḥ", "ט": "ṭ", "י": "y",
       "כ": "kh", "ך": "kh", "ל": "l", "מ": "m", "ם": "m", "נ": "n", "ן": "n", "ס": "s", "ע": "ʿ", "פ": "f",
       "ף": "f", "צ": "ṣ", "ץ": "ṣ", "ק": "q", "ר": "r", "ש": "š", "ת": "t"}
HARD = {"ב": "b", "כ": "k", "ך": "k", "פ": "p", "ף": "p"}
VOW = {"ְ": "ə", "ֱ": "ĕ", "ֲ": "ă", "ֳ": "ŏ", "ִ": "i", "ֵ": "ē", "ֶ": "e", "ַ": "a", "ָ": "ā",
       "ֹ": "ō", "ֺ": "ō", "ֻ": "u", "ׇ": "o"}
BEGAD = set("בגדכךפףת")


def clusters(word):
    out = []
    for ch in unicodedata.normalize("NFD", word) if False else word:
        if "א" <= ch <= "ת":
            out.append([ch, set()])
        elif out and "֑" <= ch <= "ׇ":
            out[-1][1].add(ch)
    return out


def translit(word):
    cl = clusters(word)
    res, i = [], 0
    prev_vowel = False
    while i < len(cl):
        base, m = cl[i]
        vow = [VOW[x] for x in m if x in VOW]
        v = vow[0] if vow else ""
        dag = "ּ" in m
        nxt = cl[i + 1] if i + 1 < len(cl) else None
        # shuruq: vav + dagesh, no vowel, after a consonant
        if base == "ו" and dag and not vow:
            res.append("û")
            prev_vowel = True
            i += 1
            continue
        # vav carrying only holam after a bare consonant: holam male
        if base == "ו" and "ֹ" in m and res and not prev_vowel:
            res.append("ô")
            prev_vowel = True
            i += 1
            continue
        if base == "ש":
            c = "ś" if "ׂ" in m else "š"
        elif base in HARD and dag and (prev_vowel or not res or base in "בכך" and not res):
            c = HARD[base]
            if res and prev_vowel:
                c += c
        elif base in HARD and dag:
            c = HARD[base]
        else:
            c = LET[base]
            if dag and base not in BEGAD and base not in "אהעחר":
                c += c
        # matres: vowel + bare yod / vav / final he
        if v and nxt and not (nxt[1] & set(VOW)) and "ּ" not in nxt[1]:
            nb = nxt[0]
            if nb == "י" and v in ("i", "ē", "e"):
                res.append(c + {"i": "î", "ē": "ê", "e": "ê"}[v])
                prev_vowel = True
                i += 2
                continue
            if nb == "ו" and v == "ō":
                res.append(c + "ô")
                prev_vowel = True
                i += 2
                continue
            if nb == "ה" and i + 2 == len(cl) and v in ("ā", "e", "ē"):
                res.append(c + {"ā": "â", "e": "eh", "ē": "êh"}[v])
                prev_vowel = True
                i += 2
                continue
        if v == "ə" and not res:
            res.append(c + "ə")
        elif v == "ə":
            res.append(c + ("" if prev_vowel is False and False else "ə"))
        else:
            res.append(c + v)
        prev_vowel = bool(v) and v != "ə"
        i += 1
    s = "".join(res)
    return s.replace("ʼə", "ʼə")


def parse_strongs(field):
    """'H9001=ו=seq/H7121=קָרָא=to call_§1_call_to|invite' -> ([H], [gloss])"""
    ids, gl = [], []
    for piece in field.split("/"):
        parts = piece.split("=")
        sid = parts[0]
        if sid in ("H9014", "H9016"):
            continue
        g = parts[2] if len(parts) > 2 else ""
        g = re.sub(r"_§.*$", "", g)
        sub = re.search(r"_§([^_@]*)(?:_([^@]*))?", parts[2]) if len(parts) > 2 else None
        if sub and sub.group(2) and sub.group(1).isdigit():
            g += " (" + sub.group(2).replace("|", "; ") + ")"
        elif sub and sub.group(1) and not sub.group(1).isdigit():
            g += f" [{sub.group(1).replace('|', '; ')}]"
        ids.append(sid)
        gl.append(g.strip().replace("|", " / "))
    return ids, gl


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    book = sys.argv[1]
    ab = ABBR[book]
    src = next(SRC.glob("TOTHT*Gen-Deu*.txt"))
    verses, order = {}, []
    for line in src.read_text(encoding="utf-8-sig").split("\n"):
        if not line.startswith(ab + "."):
            continue
        f = line.rstrip("\n").split("\t")
        if len(f) < 6:
            continue
        m = re.match(rf"{ab}\.(\d+)\.(\d+)-(\d+)(\.\w)?", f[1])
        if not m:
            continue
        key = (int(m[1]), int(m[2]))
        wn = m[3] + (m[4] or "")
        ids, gl = parse_strongs(f[5])
        body = f"{wn} {translit(f[2])} | {' + '.join(g for g in gl if g)} | {'/'.join(ids)} | {f[4]}"
        if key not in verses:
            verses[key] = []
            order.append(key)
        verses[key].append(body)
    out = ["#source: tyndale",
           f"#label: Tyndale House TOTHT, tagged Hebrew OT (STEPBible; CC BY 4.0, Tyndale House Cambridge): {book}, "
           "word by word. Line = word no., rough auto-transliteration (reference, not scholarly), English gloss "
           "(+ joins prefix/suffix pieces; [..] = proper name/sense, (..) = sub-meaning), extended Strong's "
           "(H9xxx = prefixes/suffixes), morphology code (OSHB scheme: H=Hebrew, V=verb, N=noun, R=prep., "
           "C=conj., T=particle, S=suffix; verb stems q/n/p/h etc.). ENGLISH verse numbering; Eng 6:1-7 = Heb 5:20-26. "
           ".K/.Q/.X after a word no. = ketiv/qere/LXX-only word."]
    for c, v in order:
        out += [f"@@ {c}:{v} | {c}:{v}"] + verses[(c, v)]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "tyndale.txt").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    chs = sorted({c for c, _ in order})
    print(f"tyndale: {len(order)} sections, {sum(len(x) for x in verses.values())} words, chapters {chs[0]}-{chs[-1]} ({len(chs)})")


if __name__ == "__main__":
    main()
