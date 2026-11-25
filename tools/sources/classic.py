"""Fetch + convert public-domain classic commentaries into marked files.

    python tools/sources/classic.py Leviticus [keil-delitzsch ellicott pulpit henry]
    python tools/sources/classic.py Leviticus --fetch-only

Cache: sources/downloads/<key>/chNN.html (biblehub.com). Output: sources/marked/<key>.txt.
Read downloaded HTML only with this script (it never executes it).
"""
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHAPTERS = {"Leviticus": 27, "Numbers": 36, "Deuteronomy": 34, "Joshua": 24}
SLUG = {"Leviticus": "leviticus", "Numbers": "numbers", "Deuteronomy": "deuteronomy", "Joshua": "joshua"}
# key -> (biblehub path, label)
SOURCES = {
    "keil-delitzsch": ("kad", "Keil & Delitzsch, Commentary on the Old Testament, Pentateuch (public domain), via biblehub.com/commentaries/kad."),
    "ellicott": ("ellicott", "Ellicott's Commentary for English Readers (public domain; Leviticus: C. D. Ginsburg), via biblehub.com/commentaries/ellicott."),
    "pulpit": ("pulpit", "Pulpit Commentary, EXPOSITION ONLY (homiletics and homilies dropped; public domain), via biblehub.com/commentaries/pulpit."),
    "henry": ("mhcw", "Matthew Henry, Complete Commentary on the Whole Bible (public domain), via biblehub.com/commentaries/mhcw."),
}
UA = "bible-study-fetch"


def fetch(book, key):
    path = SOURCES[key][0]
    d = ROOT / "sources" / "downloads" / key
    d.mkdir(parents=True, exist_ok=True)
    for c in range(1, CHAPTERS[book] + 1):
        f = d / f"ch{c:02d}.html"
        if f.exists() and f.stat().st_size > 2000:
            continue
        url = f"https://biblehub.com/commentaries/{path}/{SLUG[book]}/{c}.htm"
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                f.write_bytes(urllib.request.urlopen(req, timeout=60).read())
                break
            except Exception as e:  # noqa
                print("retry", url, e)
                time.sleep(3)
        time.sleep(1)


# ---------------------------------------------------------------- convert
BLOCK = {"p", "div", "br", "h1", "h2", "h3", "h4", "li", "tr", "table", "blockquote"}
SKIP = {"script", "style", "nav", "noscript", "iframe", "ins"}


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip, self.stack = [], 0, []

    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get("class") or ""
        if tag in SKIP:
            self.skip += 1
        elif tag in BLOCK:
            self.out.append("\n")
        if tag == "span" and ("sectionheading" in cls or "cmt_sub_title" in cls):
            self.out.append("\n\x01")
            self.stack.append("sh")
        elif tag == "span":
            self.stack.append("")

    def handle_endtag(self, tag):
        if tag in SKIP and self.skip:
            self.skip -= 1
        elif tag in BLOCK:
            self.out.append("\n")
        if tag == "span" and self.stack:
            if self.stack.pop() == "sh":
                self.out.append("\x02\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def to_text(html):
    p = Text()
    p.feed(html)
    t = "".join(p.out).replace("\xa0", " ")
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    t = re.sub(r" ?\n ?", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def page_blocks(f):
    """-> (pre_html, [(verse_int, ref_text, body_html)]) for one cached chapter page."""
    h = f.read_text("utf-8", errors="replace")
    a = h.find('class="chap">')
    b = h.find('<div id="rightbox">')
    h = h[a + len('class="chap">'):b if b > a else len(h)]
    parts = re.split(r'<div class="versenum">', h)
    pre, blocks = parts[0], []
    for part in parts[1:]:
        m = re.match(r"\s*<a [^>]*>([^<]*)</a></div>", part)
        ref = m.group(1) if m else ""
        body = part[m.end():] if m else part
        body = re.sub(r'<div class="verse">.*?</div>', "", body, count=1, flags=re.S)
        vm = re.search(r":(\d+)\s*$", ref)
        blocks.append((int(vm.group(1)) if vm else 0, ref, body))
    return pre, blocks


FOOT = re.compile(r"\n?Biblical Commentary on the Old Testament, by Carl Friedrich Keil.*", re.S)


def clean_foot(t):
    t = FOOT.sub("", t)
    t = re.sub(r"\n*(?:[^\n]*Commentary[^\n]*\n+)?Text Courtesy[^\n]*(?:\n+Bible Hub)?\s*$", "", t)
    t = re.sub(r"\n+Bible Hub\s*$", "", t)
    t = re.sub(r"\n*The Pulpit Commentary, Electronic Database.*$", "", t, flags=re.S)
    return t.strip()


def rng(c, a, b=None):
    return f"{c}:{a}" if not b or b == a else f"{c}:{a}-{b}"


def convert(book, key):
    d = ROOT / "sources" / "downloads" / key
    secs, missing = [], []   # (range, title, text)
    for c in range(1, CHAPTERS[book] + 1):
        f = d / f"ch{c:02d}.html"
        if not f.exists():
            missing.append(c)
            continue
        pre, blocks = page_blocks(f)
        pt = clean_foot(to_text(pre))
        if pt:
            first = c == 1 and key in ("keil-delitzsch", "ellicott")
            r, title = ("intro", "Introduction") if first else (str(c), f"{book} {c} (chapter-level)")
            hm = re.match(r"(.{3,100}?)\. - ", pt)
            if hm and not first:
                title = f"{hm.group(1)} ({book} {c}, chapter-level)"
            secs.append((r, title, pt))
        for v, ref, body in blocks:
            t = clean_foot(to_text(body))
            if not t:
                continue
            if key == "henry":
                chunks = re.split(r"\x01(.*?)\x02", t)
                # a "Verses N-M" line that biblehub left unmarked (Numbers 1) is a heading too
                t = re.sub(r"\n(Verses? \d+(?:\s*[-–—]\s*\d+)?)\n", "\n\x01\\1\x02\n", t)
                chunks = re.split(r"\x01(.*?)\x02", t)
                head = chunks[0].strip()
                if head:
                    secs.append((rng(c, v), f"{book} {c}:{v}", head))
                for i in range(1, len(chunks), 2):
                    title, txt = chunks[i].strip(), chunks[i + 1].strip()
                    m = re.match(r"Verses? (\d+)(?:\s*[-–—]\s*(\d+))?", title)
                    if m:
                        r = rng(c, int(m.group(1)), int(m.group(2) or 0))
                    elif title.startswith("Chapter"):
                        r = str(c)
                    else:
                        r = "intro" if c == 1 and not secs else rng(c, v)
                        if "Exposition" in title or "Observations" in title:
                            r = "intro"
                    if txt:
                        secs.append((r, f"{book} {r}" if title.startswith("Verse") else title, txt))
                continue
            r, title = rng(c, v), f"{book} {c}:{v}"
            if key == "pulpit":
                chunks = re.split(r"(.*?)", t)
                if chunks[0].strip():
                    secs.append((r, title, chunks[0].strip()))
                for i in range(1, len(chunks), 2):
                    ttl, txt = chunks[i].strip(), chunks[i + 1].strip().lstrip("-– ").strip()
                    m = re.match(r"Verses? (\d+)(?:\s*[-–—,]\s*(\d+))?", ttl)
                    rr = rng(c, int(m.group(1)), int(m.group(2) or 0)) if m else rng(c, v)
                    if txt:
                        secs.append((rr, f"{book} {rr}", txt))
                continue
            t = t.replace("", "").replace("", "")
            if key == "keil-delitzsch":
                # biblehub anchors each K&D paragraph at a verse; K&D comment on stretches:
                # span = from this anchor to just before the next anchored paragraph.
                nxt = [bv for bv, _, bb in blocks if bv > v and clean_foot(to_text(bb))]
                end = (nxt[0] - 1) if nxt else max(bv for bv, _, _ in blocks)
                lo, hi = v, max(v, end)
                m = re.match(rf"(.{{3,140}}?)\. - {book} (\d+):(\d+)(?:\s*[-–]\s*(?:(\d+):)?(\d+))?", t)
                if m and int(m.group(2)) == c and not m.group(4):
                    lo, hi = min(lo, int(m.group(3))), max(hi, int(m.group(5) or m.group(3)))
                    title = f"{m.group(1).strip()} ({book} {rng(c, lo, hi)})"
                r = rng(c, lo, hi)
                if title.startswith(book):
                    title = f"{book} {r}"
            secs.append((r, title, t))
    return secs, missing


def write(book, key, secs):
    out = Path(ROOT / "sources" / "marked")
    out.mkdir(parents=True, exist_ok=True)
    lines = [f"#source: {key}", f"#label: {SOURCES[key][1]}", "#numbering: english"]
    for r, title, t in secs:
        lines += [f"@@ {r} | {title}", t, ""]
    (out / f"{key}.txt").write_text("\n".join(lines).rstrip() + "\n", "utf-8", newline="\n")


def main(argv):
    if not argv or argv[0] not in CHAPTERS:
        sys.exit(f"usage: classic.py <{'|'.join(CHAPTERS)}> [keys] [--fetch-only]")
    book = argv[0]
    keys = [a for a in argv[1:] if a in SOURCES] or list(SOURCES)
    for k in keys:
        fetch(book, k)
        if "--fetch-only" in argv:
            continue
        secs, missing = convert(book, k)
        write(book, k, secs)
        have = set()
        for r, _, _ in secs:
            m = re.match(r"(\d+)", r)
            if m and r != "intro":
                have.add(int(m.group(1)))
        gaps = [c for c in range(1, CHAPTERS[book] + 1) if c not in have]
        print(f"{k}: {len(secs)} sections, chapters with no section: {gaps}" + (f" (pages missing: {missing})" if missing else ""))


if __name__ == "__main__":
    main(sys.argv[1:])
