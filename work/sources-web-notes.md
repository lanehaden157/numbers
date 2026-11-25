# Numbers v2: free web sources (fetched 2026-11-25)

Converters: `tools/sources/sefaria.py` and `classic.py` (copied from Leviticus v2; edits: K&D regex generic in book name, Sefaria no longer refuses a file when a whole chapter lacks English, Henry "Verses N-M" heading fix, labels). Raw cache: `sources/downloads/<key>/` (biblehub HTML; `sefaria/` JSON; `brenton/`). Rebuild: `python -I tools/sources/sefaria.py Numbers <keys>`, `python -I tools/sources/classic.py Numbers`, then `python tools/split_sources.py`. Not touched: sibling keys (rashi, constable, jps, tyndale, levine, doty, whitt, morales). Not indexed on purpose: chizkuni (83% English), tur-harokh (not asked).

## Sefaria English (Hebrew numbering; split_sources converts to English numbers, section titles keep the Hebrew ref, e.g. "Ibn Ezra on 17:2 [16:37]")
- `ibn-ezra`: Strickman-Silver (CC-BY-NC). 662 verses, all 36 ch. Good plain-sense/grammar; bracketed [note: ...] are translators' notes.
- `ramban`: Chavel (CC-BY). 233 verses, all ch except 30 (no comment). Long essays, ~930 KB; strongest on Num 13-14, 21, 24.
- `sforno`: Munk (CC-BY). 330 of 343 commented verses; ch 29 has no English; missing 4:49, 18:5, 21:15-16, 22:34, 24:18-21, 24:23, 26:55, 31:17. Hebrew-script lemmas stay in the text.
- `rashbam`: Munk (CC-BY). 207 of 214 verses; commentary stops after ch 25 (no ch 26-29 comment, expected). Missing 7:84, 8:26, 16:4, 21:8, 24:22, 34:6, 35:11. Sparse in 14, 22.
- `or-hachaim`: Munk (CC-BY). 388 of 403 verses, all ch; long (~950 KB). Missing English 9:1, 9:13-22 (parts), 15:2-39 (6), 20:17.
- `rabbeinu-bahya`: Munk (CC-BY). 402 of 403 verses (27:4 missing), ~1.1 MB; opens each parashah with a proem verse (sits on 1:1). No comment on 13:30-33 (it comments on 13:1-2 etc.).
- Quirks: Munk volumes put Hebrew lemmas in the text; Hebrew numbering means Eng 16:36-50 / 17 / 25:19 / 29:40 / 30 are converted by `numbers-versification.md`. Sefaria rate: 1 call/s (7 min for 9 keys x 36 ch).

## biblehub classics (public domain; English numbering; anchors approximate)
- `keil-delitzsch`: 417 sections, all ch. Biblehub anchors a paragraph at a verse; sections run to the next anchor, so read ranges as stretches (13-14 is one chapter-level block). Quality: best of the old set (Hebrew grammar, Balaam prophecy 24:17 full).
- `ellicott`: 524 sections, per verse, all ch (Numbers is not Ginsburg; label is generic). Short, textual notes.
- `pulpit`: 775 sections, exposition only (homiletics dropped), all ch. Good on 22:28 (ass), 24:17.
- `henry`: 143 sections, paragraphs "Verses N-M" plus a chapter-level section per chapter (13-14 are chapter-level only). Devotional. Fix applied: ch 1 "Verses 1-16" had been absorbed in the intro.

## Texts
- `brenton-lxx.txt`, `web-bible.txt` (`sources/text/`): whole-Bible files copied from Matthew v2 (source: ebible.org eng-Brenton_vpl, `downloads/brenton/`); NUM has 1288 lines each. `kit.py bible NUM 16:36 --lxx` correctly shows "[LXX 17:1]".
- LXX numbering: Brenton follows the Hebrew verse numbers in Num 17 (28 verses) and 30 (Hebrew 30:2-17 = English 30:1-16); `lxx_numbering: hebrew` in book.json handles it. No LXX 25:19 line (folds into 26:1, as in Hebrew). Greek-vs-Hebrew content differences not surveyed here.

## Not found
- Origen, Homilies on Numbers: only Scheck's ACT translation (IVP, copyrighted); CCEL has Rufinus's preface only. No `origen` key. Other fathers: none checked.

## Spot checks (kit.py range, 1:1-3, 13:30-33, 14:1-5, 22:28-30, 24:17)
All six Sefaria keys and K&D, Ellicott, Pulpit return the right verse text (gaps above: ramban 22:28 none, rashbam 14/22 none, rabbeinu-bahya 13:30-33 none, henry verse-level only as ranges).
