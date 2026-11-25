"""Fetch Sefaria English commentaries on a Torah book into sources/marked/<key>.txt.

Usage:  python -I tools/sources/sefaria.py Leviticus [key ...]
        python -I tools/sources/sefaria.py Leviticus --probe   (report coverage only)

Keys not given = all in COMMENTARIES. Raw JSON is cached in sources/downloads/sefaria/
(1 request/second, generic User-Agent). Numbering is Hebrew (Masoretic) as on Sefaria.
Only writes a marked file when the English covers every chapter (see MIN_COVER);
otherwise prints the gap and skips.
"""
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DL = ROOT / "sources" / "downloads" / "sefaria"
OUT = ROOT / "sources" / "marked"
UA = "bible-study-fetch"
CHAPTERS = {"Leviticus": 27, "Numbers": 36, "Deuteronomy": 34, "Joshua": 24, "Genesis": 50, "Exodus": 40}

# key -> (Sefaria title template, display name)
COMMENTARIES = {
    "rashi": ("Rashi on {b}", "Rashi"),
    "ramban": ("Ramban on {b}", "Ramban"),
    "ibn-ezra": ("Ibn Ezra on {b}", "Ibn Ezra"),
    "sforno": ("Sforno on {b}", "Sforno"),
    "rashbam": ("Rashbam on {b}", "Rashbam"),
    "chizkuni": ("Chizkuni, {b}", "Chizkuni"),
    "or-hachaim": ("Or HaChaim on {b}", "Or HaChaim"),
    # kli-yakar: skipped, Sefaria English is a 2026 machine translation (Claude 3.7)
    "rabbeinu-bahya": ("Rabbeinu Bahya, {b}", "Rabbeinu Bahya"),
    "tur-harokh": ("Tur HaArokh, {b}", "Tur HaArokh"),
    # haamek-davar: skipped, English covers 5% of verses
}
MIN_COVER = 0.95  # share of Hebrew-commented verses that must also have English


def get(title, ch):
    f = DL / f"{re.sub(r'[^A-Za-z0-9]+', '_', title)}.{ch}.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    url = ("https://www.sefaria.org/api/v3/texts/" + urllib.parse.quote(f"{title}.{ch}") +
           "?version=english&version=hebrew")
    time.sleep(1)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        data = json.load(urllib.request.urlopen(req, timeout=60))
    except Exception as e:  # 404 etc.
        data = {"error": str(e)}
    f.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return data


def clean(s):
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"</?(p|div)[^>]*>", "\n", s)
    s = re.sub(r"<sup[^>]*class=\"footnote-marker\"[^>]*>.*?</sup>", "", s, flags=re.S)
    s = re.sub(r"<i class=\"footnote\">(.*?)</i>", r" [note: \1]", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s).replace("\xa0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\s*\n\s*", "\n", s)
    return s.strip()


def flat(x):
    """Comments for one verse -> list of strings."""
    if isinstance(x, str):
        return [x] if x.strip() else []
    if isinstance(x, list):
        out = []
        for y in x:
            out += flat(y)
        return out
    return []


def pick(data, lang):
    for v in data.get("versions", []):
        if v.get("language") == lang:
            return v
    return None


def build(book, key):
    tmpl, name = COMMENTARIES[key]
    title = tmpl.format(b=book)
    secs, he_n, en_n, miss, info, nochap = [], 0, 0, [], None, []
    for ch in range(1, CHAPTERS[book] + 1):
        d = get(title, ch)
        if "error" in d or not d.get("versions"):
            continue
        en, he = pick(d, "en"), pick(d, "he")
        if en and not info:
            info = (en.get("versionTitle", ""), en.get("license", ""), en.get("versionSource", ""))
        ent = en["text"] if en else []
        het = he["text"] if he else []
        n = max(len(ent), len(het))
        got = False
        for v in range(n):
            h = flat(het[v]) if v < len(het) else []
            e = flat(ent[v]) if v < len(ent) else []
            e = [c for c in (clean(c) for c in e) if c]
            he_n += bool(h)
            if h and not e:
                miss.append(f"{ch}:{v + 1}")
            if e:
                en_n += 1
                got = True
                secs.append((ch, v + 1, e))
        if not got and any(flat(x) for x in het):
            nochap.append(ch)
    return title, name, secs, he_n, en_n, miss, info, nochap


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    probe = "--probe" in args
    args = [a for a in args if a != "--probe"]
    book = args[0]
    keys = args[1:] or list(COMMENTARIES)
    DL.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for key in keys:
        title, name, secs, he_n, en_n, miss, info, nochap = build(book, key)
        cover = (he_n - len(miss)) / he_n if he_n else 0
        print(f"{key}: {title}: English verses {en_n}, Hebrew-commented verses {he_n}, "
              f"missing English {len(miss)} ({cover:.0%} cover); chapters w/o English {nochap}; {info}")
        if miss:
            print("   missing:", " ".join(miss[:40]), "..." if len(miss) > 40 else "")
        if probe or not secs or cover < MIN_COVER:
            print("   -> NOT written" if not probe else "")
            continue
        label = (f"{name} on {book}, English translation on Sefaria: {info[0]} ({info[1] or 'licence not stated'}); "
                 f"{info[2]}. Hebrew (Masoretic) numbering.")
        lines = [f"#source: {key}", f"#label: {label}", "#numbering: hebrew"]
        for ch, v, e in secs:
            lines.append(f"@@ {ch}:{v} | {name} on {ch}:{v}")
            lines.append("\n\n".join(e))
        (OUT / f"{key}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"   -> wrote {len(secs)} sections")


if __name__ == "__main__":
    main()
