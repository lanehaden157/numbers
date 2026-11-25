#!/usr/bin/env python
"""Morales sources -> marked files.

  morales          Who Shall Ascend the Mountain of the Lord? (NSBT 37, 2015)
                   reads sources/morales/morales-who-shall-ascend.txt (converted, [pdf p. N] markers)
  morales-exodus   Exodus Old and New (ESBT 2020)
                   extracts sources/downloads/morales-exodus/*.pdf with pymupdf (page-marked
                   [pdf p. N], 'OceanofPDF.com' lines dropped) into
                   sources/downloads/morales-exodus/extracted.txt, then indexes it.

Usage: python tools/sources/morales.py [morales] [morales-exodus] [--extract-only]

Run the PDF extraction under isolation: the script re-invokes itself with `python -I`
for the pymupdf step (the PDF is an untrusted download).

Numbers v2 copy: only `morales-exodus` is used (the Leviticus book is not a Numbers source). It is a
biblical theology, not a verse commentary: everything is `intro` except the daily-service section
(Num 28:1-8). Other Numbers citations in it: ch. 6 (Num 11:16-17, 25, 29; 12:6-8), ch. 7 (Num 3:7-8; 6:22-27),
ch. 5 (Num 9:1-14), ch. 10-11 (Num 14:17-19; 16:3, 41; 20:3, 11), listed in work/sources-local-notes.md.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "sources"
OUT = SRC / "marked"
DL = SRC / "downloads" / "morales-exodus"
HERE = Path(__file__).resolve()

LABEL_1 = ("Morales, Who Shall Ascend the Mountain of the Lord? A Biblical Theology of the Book of Leviticus "
           "(NSBT 37, IVP/Apollos, 2015). Biblical theology, not a verse commentary. Private copy: paraphrase. "
           "Page markers are PDF pages.")
LABEL_2 = ("Morales, Exodus Old and New: A Biblical Theology of Redemption (ESBT, IVP Academic, 2020). "
           "Biblical theology, not a verse commentary. Private copy: paraphrase. Page markers are PDF pages.")


def write_marked(key, label, sections):
    OUT.mkdir(parents=True, exist_ok=True)
    parts = ["#source: %s\n#label: %s" % (key, label)]
    n = 0
    for rng, title, lines in sections:
        body = "\n".join(l.rstrip() for l in lines)
        body = re.sub(r"\n{3,}", "\n\n", body).strip("\n")
        body = re.sub(r"(?m)^@@ ", " @@ ", body)
        if not body.strip():
            continue
        parts.append("@@ %s | %s\n%s" % (rng, re.sub(r"\s+", " ", title).strip(), body))
        n += 1
    (OUT / (key + ".txt")).write_text("\n".join(parts) + "\n", encoding="utf-8", newline="\n")
    return n


def by_anchors(lines, anchors, end):
    """anchors: (line_no_1based, expected_line_prefix, range, title). Section runs to the next anchor."""
    secs = []
    for k, (ln, prefix, rng, title) in enumerate(anchors):
        got = lines[ln - 1].strip()
        if not got.startswith(prefix):
            sys.exit("anchor mismatch at line %d: wanted %r, found %r" % (ln, prefix, got[:60]))
        nxt = anchors[k + 1][0] - 1 if k + 1 < len(anchors) else end
        if rng is None:     # deliberately left out (indexes, praise pages)
            continue
        secs.append((rng, title, lines[ln:nxt]))   # skip the heading line itself: it is in the title
    return secs


# ------------------------------------------------------------------ morales

A1 = [
    (6, "Prologue", "intro", "Prologue: The glory of God's house: the lampstand and the table of the Presence"),
    (265, "Chapter One", "intro", "Ch 1: Leviticus within the Pentateuch: a theological structure"),
    (843, "Chapter Two", "intro", "Ch 2: Longing for Eden: Genesis, the narrative context of Leviticus"),
    (2030, "Chapter Three", "intro", "Ch 3: Returning to Eden: Exodus, the narrative context of Leviticus"),
    (3212, "Chapter Four", "1-10", "Ch 4: Approaching the house of God: introduction (Lev 1-10)"),
    (3331, "Genesis 3:9", "1:1-2", "Ch 4: the divine call from the tent (Lev 1:1; Exod 40:34-35)"),
    (3709, "The order and theology of sacrifice", "1-7", "Ch 4: The order and theology of sacrifice"),
    (3794, "The cultic journey", "1-7", "Ch 4: The cultic journey: ascent into the presence of God"),
    (3832, "The presentation rite", "1:3", "Ch 4: The presentation rite"),
    (3914, "The hand-leaning rite", "1:4", "Ch 4: The hand-leaning rite"),
    (3978, "The slaughter rite", "1:5", "Ch 4: The slaughter rite"),
    (4097, "The burning rite", "1:9", "Ch 4: The burning rite"),
    (4275, "The communion rite", "3", "Ch 4: The communion rite"),
    (4355, "The benediction", "9:22-24", "Ch 4: The benediction"),
    (4414, "Conclusion", "1-10", "Ch 4: Conclusion"),
    (4422, "The daily service", "9", "Ch 4: The daily service"),
    (4475, "Another crisis introduced", "10", "Ch 5: Another crisis introduced (Nadab and Abihu, Lev 10)"),
    (4487, "Chapter Five", "10", "Ch 5: Cleansing the house of God: introduction and Lev 10"),
    (4721, "Summary", "1-10", "Ch 5: Summary of Lev 1-10 in the cultic system"),
    (4770, "Considering that", "1-16", "Ch 5: The tabernacle cultus and the theophanies (Lev 1-16)"),
    (4907, "Life and death", "11-15", "Ch 5: Life and death (clean and unclean, Lev 11-15)"),
    (4996, "God’s holiness and sin’s pollution", "11-16", "Ch 5: God's holiness and sin's pollution"),
    (5102, "Israel and the nations", "11", "Ch 5: Israel and the nations (the food laws, Lev 11)"),
    (5153, "Clean and unclean within the cultic system", "11-16", "Ch 5: Clean and unclean within the cultic system"),
    (5346, "Cleansing God’s house", "16", "Ch 5: Cleansing God's house (the Day of Atonement, Lev 16)"),
    (5838, "Chapter Six", "17-27", "Ch 6: Meeting with God at the house of God: introduction (Lev 17-27)"),
    (5950, "The lampstand and bread of the presence in Numbers", "24:1-9", "Ch 6: The lampstand and bread of the presence in Numbers"),
    (5971, "The lampstand and bread of the presence in Leviticus", "24:1-9", "Ch 6: The lampstand and bread of the presence in Leviticus (24:1-9)"),
    (6035, "Leviticus 24:1–9 within", "23-25", "Ch 6: Leviticus 24:1-9 within the context of chapters 23-25"),
    (6263, "Meeting with God at the house", "23-25", "Ch 6: Meeting with God at the house of God (sacred time, terminology of meeting)"),
    (6374, "Narrative strategy", "17-27", "Ch 6: Narrative strategy"),
    (6436, "Literary structure and theme", "1-27", "Ch 6: Literary structure and theme of Leviticus"),
    (6697, "The only source of holiness", "17-27", "Ch 6: The only source of holiness: the presence of YHWH God"),
    (6731, "True holiness", "18-20", "Ch 6: True holiness: belonging exclusively to YHWH"),
    (6887, "The pursuit of holiness", "17-27", "Ch 6: The pursuit of holiness: the dynamic between cult and holiness"),
    (6975, "The goal of holiness", "17-27", "Ch 6: The goal of holiness: communion and fellowship with God"),
    (7165, "Chapter Seven", "intro", "Ch 7: Establishing the earthly house of God: from Sinai's tabernacle to Zion's temple"),
    (8402, "Chapter Eight", "intro", "Ch 8: Entering the heavenly house of God: from the earthly to the heavenly Mount Zion"),
]
NOTES_AT = 10287          # 1-based line of the "=== NOTES" marker
NOTE_HEADS = [  # (first line of the chapter's endnotes, title)
    (10291, "Prologue"), (10301, "Ch 1"), (10431, "Ch 2"), (10802, "Ch 3"), (10962, "Ch 4"),
    (11152, "Ch 5"), (11360, "Ch 6"), (11586, "Ch 7"), (11697, "Ch 8"),
]


def morales():
    lines = (SRC / "morales" / "morales-who-shall-ascend.txt").read_text(encoding="utf-8").split("\n")
    assert lines[NOTES_AT - 1].startswith("=== NOTES"), lines[NOTES_AT - 1]
    secs = by_anchors(lines, A1, NOTES_AT - 1)
    for k, (ln, title) in enumerate(NOTE_HEADS):
        end = NOTE_HEADS[k + 1][0] - 1 if k + 1 < len(NOTE_HEADS) else len(lines)
        secs.append(("intro", "Endnotes: " + title, lines[ln - 1:end]))
    return write_marked("morales", LABEL_1, secs), secs


# ------------------------------------------------------------------ morales-exodus
A2 = [
    (57, "SERIES PREFACE", "intro", "Series preface"),
    (102, "AUTHOR", "intro", "Author's preface"),
    (171, "INTRODUCTION", "intro", "Introduction"),
    (336, "Chapter One", "intro", "Ch 1: Exile before exodus (Part 0; Genesis 1-11 backdrop)"),
    (689, "PART 1", "intro", "Ch 2: The exodus prefigured (Part 1: the historical exodus; Genesis)"),
    (1275, "Chapter Three", "intro", "Ch 3: Glory to God in the highest! (Part 1; Exodus 1-11)"),
    (1657, "Chapter Four", "intro", "Ch 4: Slaying the sea dragon (Part 1; Exodus 14-15)"),
    (2248, "Chapter Five", "intro", "Ch 5: The blood of the Passover lamb (Part 1; Exodus 12)"),
    (2339, "A THEOLOGY OF THE PASSOVER RITUAL", "intro", "Ch 5: A theology of the Passover ritual (blood manipulation: Lev 4-5, 16)"),
    (2419, "UNLEAVENED BREAD", "intro", "Ch 5 (cont.): Unleavened bread, circumcision, the firstborn (Exodus 12-13)"),
    (2617, "Chapter Six", "intro", "Ch 6: Moses the servant of Yahweh (Part 1; Exodus 2-34)"),
    (3116, "Chapter Seven", "intro", "Ch 7: The cultic exodus: introduction (Exodus 25-40; Lev 1-9)"),
    (3146, "ISRAEL", "intro", "Ch 7: Israel's liturgy: a threefold movement to God's abode (Lev 1-9)"),
    (3348, "THE DAY OF ATONEMENT", "intro", "Ch 7: The Day of Atonement: through the gates of the garden of Eden (Lev 16)"),
    (3429, "THE DAILY SERVICE", "28:1-8", "Ch 7: The daily service: Yahweh's continual provision of lambs (burnt offering; Exod 29, Num 28)"),
    (3514, "PART 2", "intro", "Ch 8: The pattern of sacred history (Part 2: the prophesied second exodus)"),
    (3946, "Chapter Nine", "intro", "Ch 9: Greater than the first exodus (Part 2; Isaiah)"),
    (4497, "Chapter Ten", "intro", "Ch 10: The servant of the second exodus (Part 2; Isaiah 40-55)"),
    (4795, "Ultimately, it is Israel", "intro", "Ch 10: The servant's guilt offering (Isa 53:10; Lev 4-5, 16:22, 17:11)"),
    (4887, "ISAIAH 56", "intro", "Ch 10 (cont.): Isaiah 56-66: the servants of the servant"),
    (4957, "Chapter Eleven", "intro", "Ch 11: Who is the servant of Yahweh? (Part 2)"),
    (5258, "PART 3", "intro", "Ch 12: The new exodus in the Gospel of John (Part 3: Jesus the Messiah)"),
    (5744, "Chapter Thirteen", "intro", "Ch 13: The Spirit of the new exodus (Part 3)"),
    (6171, "Chapter Fourteen", "intro", "Ch 14: The only hope (Part 3)"),
    (6558, "FURTHER READING", "intro", "Further reading"),
    (6581, "AUTHOR INDEX", None, ""),
    (6693, "SCRIPTURE INDEX", "intro", "Scripture index (printed page numbers, not PDF pages)"),
    (7918, "NOTES", None, ""),
    (7919, "AUTHOR", "intro", "Endnotes: Author's preface"),
    (7921, "INTRODUCTION", "intro", "Endnotes: Introduction"),
    (7940, "CHAPTER 1:", "intro", "Endnotes: Ch 1"),
    (7949, "CHAPTER 2:", "intro", "Endnotes: Ch 2"),
    (7973, "CHAPTER 3:", "intro", "Endnotes: Ch 3"),
    (7978, "CHAPTER 4:", "intro", "Endnotes: Ch 4"),
    (8029, "CHAPTER 5:", "intro", "Endnotes: Ch 5"),
    (8046, "CHAPTER 6:", "intro", "Endnotes: Ch 6"),
    (8056, "CHAPTER 7:", "intro", "Endnotes: Ch 7 (Leviticus 1-9, 16)"),
    (8085, "CHAPTER 8:", "intro", "Endnotes: Ch 8"),
    (8093, "CHAPTER 9:", "intro", "Endnotes: Ch 9"),
    (8100, "CHAPTER 10:", "intro", "Endnotes: Ch 10"),
    (8135, "CHAPTER 11:", "intro", "Endnotes: Ch 11"),
    (8161, "CHAPTER 12:", "intro", "Endnotes: Ch 12"),
    (8197, "CHAPTER 13:", "intro", "Endnotes: Ch 13"),
    (8205, "CHAPTER 14:", "intro", "Endnotes: Ch 14"),
    (8220, "PRAISE", None, ""),
]


def morales_exodus():
    path = DL / "extracted.txt"
    if not path.exists():
        subprocess.run([sys.executable, "-I", str(HERE), "--extract"], check=True)
    lines = path.read_text(encoding="utf-8").split(chr(10))
    # chapter 2 anchor starts at its PART line; chapter 2 itself begins 9 lines later
    secs = by_anchors(lines, A2, len(lines))
    return write_marked("morales-exodus", LABEL_2, secs), secs


def extract():
    """Run under `python -I`: PDF -> extracted.txt (page-marked)."""
    pdfs = sorted(DL.glob("*.pdf"))
    if not pdfs:
        sys.exit("no PDF in " + str(DL))
    import pymupdf
    doc = pymupdf.open(str(pdfs[0]))
    out = []
    for i, page in enumerate(doc, 1):
        text = page.get_text("text").replace(chr(160), " ")
        lines = [l for l in text.split("\n") if "oceanofpdf" not in l.lower()]
        out.append("[pdf p. %d]\n%s" % (i, "\n".join(lines).strip("\n")))
    (DL / "extracted.txt").write_text("\n\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print("extracted %d pages from %s" % (len(doc), pdfs[0].name))


def main():
    args = sys.argv[1:]
    if args[:1] == ["--extract"]:
        extract()
        return
    which = [a for a in args if not a.startswith("--")] or ["morales-exodus"]   # Numbers: only the Exodus book
    if "morales" in which:
        n, _ = morales()
        print("morales: %d sections" % n)
    if "morales-exodus" in which:
        n, _ = morales_exodus()
        print("morales-exodus: %d sections" % n)


if __name__ == "__main__":
    main()
