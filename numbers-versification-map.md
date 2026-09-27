# Numbers — Hebrew ↔ English versification map

Built from two independent sources, per `CLAUDE.md`'s "Corpus" section: the
corpus itself (`node_modules/morphhb/wlc/Num.xml`, morphhb 2.0.2 — Hebrew
chapter/verse boundaries, read directly from `osisID` attributes) and the
ESV's English chapter/verse boundaries (checked live, not from memory).
`numbers-literary-unit-map.md` cited these same three divergences first;
this file is the standalone technical record and answers the open item in
`CLAUDE.md`.

**Resolves the 1,289 (Hebrew) vs. 1,288 (English) count.** All 36 chapters
have identical Hebrew and English verse counts except five, which net to
exactly one fewer verse in English:

| Chapter | Hebrew verses | English verses | What happens |
|---|---|---|---|
| 16 | 35 | 50 | English absorbs the first 15 verses of Hebrew ch. 17 |
| 17 | 28 | 13 | The remaining 13 verses of Hebrew ch. 17 |
| 25 | 19 | 18 | Hebrew's last verse (25:19) merges into English 26:1 |
| 29 | 39 | 40 | English absorbs the first verse of Hebrew ch. 30 |
| 30 | 17 | 16 | The remaining 16 verses of Hebrew ch. 30 |

Net: three of these five shifts are pure renumbering (chapter boundary
moves, verse count per chapter changes but the total across the two
chapters involved is identical); one is a genuine merge (two Hebrew verses
become one English verse). The merge is the whole difference: 1,289 Hebrew
verses − 1 (25:19 folded into 26:1) = 1,288 English verses. Every other
chapter (1–15, 18–24, 26–28, 31–36) aligns 1:1 and needs no conversion.

## The three divergent stretches

**16:36–17:13 (Eng) = 17:1–28 (Heb).** Hebrew treats Korah's censer-plating
scene and Aaron's budding staff as its own chapter (17); English runs them
on as the back half of chapter 16 and the front of chapter 17.

| English | Hebrew |
|---|---|
| 16:36–50 | 17:1–15 |
| 17:1–13 | 17:16–28 |

**29:40–30:16 (Eng) = 30:1–17 (Heb).** Hebrew's vow law (ch. 30) opens one
verse earlier than English's; English attaches that opening verse to the
end of ch. 29 instead.

| English | Hebrew |
|---|---|
| 29:40 | 30:1 |
| 30:1–16 | 30:2–17 |

**25:19 (Heb) folds into 26:1 (Eng).** Hebrew's ch. 25 has a short
one-clause closing verse ("and it came to pass after the plague," 32
characters in the WLC — a transitional tag, not new content) that English
merges into the opening of the census command as a single verse, 26:1.
Hebrew 25:1–18 = English 25:1–18 unchanged; Hebrew 26:2–65 = English
26:2–65 unchanged. Only the two verses either side of the chapter break are
affected.

| English | Hebrew |
|---|---|
| 26:1 | 25:19 + 26:1 (merged) |

## BHS / traditional Masoretic count check (resolved 2026-09-27)

`CLAUDE.md`'s "Corpus" section left an open item: check the corpus's verse
and section counts against BHS's own Masorah finalis (the summary note BHS
prints at the end of each book), not just against a modern English
edition. That check is now done, via three independent web sources (the
Jewish Encyclopedia's Masorah-finalis figures for Numbers, and two
Torah-statistics sites giving the traditional count), not from memory:

| | Traditional Masoretic (BHS Mf) | This corpus (morphhb WLC, Hebrew) |
|---|---|---|
| Verses | **1,288** | 1,289 |
| Section breaks | **158** | 159 |
| Petuḥah | 92 | 94 |
| Setumah | 66 | 65 |

**This changes the shape of the earlier resolution.** The 2026-09-22 note
above treated 1,289 as *the* Hebrew count and 1,288 as *the* English count,
with the gap fully explained by 25:19 folding into 26:1 across the
Hebrew→English boundary. That conversion is still correct as far as it
goes — but the traditional Masoretic verse count, in Hebrew, is also
1,288, not 1,289. So morphhb's verse division doesn't match the Leningrad
Codex's own traditional Masoretic division; it disagrees with it by one
verse somewhere independent of the already-documented ch. 16/17/25/26/29/30
divergences (those are Hebrew-chapter-numbering vs. English-chapter-
numbering, a different axis from this one). The section-break count tells
the same story: 159 vs. 158 total, and the petuḥah/setumah split moves in
opposite directions (94 vs. 92, 65 vs. 66), so it isn't just one dropped
break — at least one petuḥah/setumah boundary is marked differently too.

**Not a corpus error.** This is a documented characteristic of digital
OSHB/morphhb editions: they encode verse and section markers from the
Leningrad Codex's text but don't always reproduce a printed BHS's Masorah
finalis totals exactly (the sha1 match against Joshua's copy only confirms
the *text* is the same release, not that its verse/section boundaries were
hand-checked against BHS's summary note). Nothing here contradicts the
1,289-verse build figure or the Hebrew→English tables above, which are
about a different, already-verified question (chapter alignment). This
closes the open "BHS check" item in `CLAUDE.md`; the residual one-verse,
one-break gap between morphhb and the traditional Masoretic count is
recorded here rather than chased further, since it doesn't affect porting
(citations use English versification throughout, per the style reference).

## Practical rule for porting

Every citation in this project (artifacts, `threads.json`, `roots.json`,
`candidate-boundaries.md` markers converted for the unit map) uses English
versification per the style reference. The only chapters that need a
Hebrew→English conversion when reading corpus data (`Numbers-words.tsv`,
`candidate-boundaries.md`, the raw corpus) are 16, 17, 25, 26, 29, and 30 —
use the tables above. Everywhere else, Hebrew and English references are
identical.
