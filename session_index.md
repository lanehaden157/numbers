# Session Index

Read this first. 3 lines max per session.

- **2026-09-22**: Bootstrapped from `bible-core`'s `template/` (core `0.1.0`, commit `ecd5bf6`), corpus built (1,289 verses), style reference and chat-side instructions drafted. Synced project-side files; project side delivered the unit map (38 units/9 movements/2 parts) and resources.md.
  Encoded groupings into `book.json`/`data/units.json`; resolved the 1,289-vs-1,288 verse count via `numbers-versification-map.md` (one real merge, Heb 25:19 → Eng 26:1). No units built yet — next is unit 1 pass 1.
- **2026-09-23**: Unit 1 ported ("The First Accounting"): fixed candidate metadata formats, answered six porter questions by popup, revised draft, added table.list CSS.
  Promoted six book-wide threads, synced, committed and pushed. Open: 23 audit gaps in the collapsed vv22–43 table; not yet viewed in browser.
- **2026-09-26**: Reviewed `CHAT_SIDE_INSTRUCTIONS.md` for bloat (~580 words, not bloated); trimmed core repeats and updated lens notes with unit 1 evidence. Needs re-paste into the project field.
- **2026-09-26 (b)**: Unit 2 ported; 7 questions answered (degel = company, ʾotot = signs, pe = ph, both retrofitted into unit 1). Promoted camp/set-out/tribe-staff/chieftain (10 threads).
  Core 0.8.2 colour fix (readable colours first) after three threads came out grey in dark mode. Coordinated with the concurrent core session.
- **2026-09-27**: Unit 3 ported ("Aharon's line and the Levites in place of the firstborn"). Answered by popup: zar = stranger / strange fire (1:51 retrofitted), redemption price, ʿal pi YHWH literal, 6486 joins account.
  Promoted stranger, near, holy, firstborn (14 threads). Core 0.9.1 (bible-core `80642f8`): tracked spans inside a data-verses table are colour-only summary tags, so unit 3's table keeps its colours. Audit 0 gaps, test 8/8.
- **2026-09-27 (b)**: Closed the open BHS check (`CLAUDE.md` "Corpus"): BHS's own Masorah finalis gives 1,288 verses / 158 breaks for Numbers, in Hebrew — not 1,289/159 as morphhb has it. New section in `numbers-versification-map.md`; not a corpus error, doesn't affect porting.
- **2026-09-28**: Unit 4 ported (Kehat load, Levite service ages 30–50); all 8 porter questions answered as drafted (tachash skin, most holy things, serve/service, army + 6633).
  Promoted carry, serve, touch, cover, blue (19 threads); nine retro tags into units 1/3. Audit 0 gaps, test 8/8. Not yet browser-checked.
- **2026-09-29**: Vendored core 0.9.9 (speed only, outputs identical): build 18.6s to about 4.5s, test 9.5s to about 2s. Build and `biblecore test` 8/8.
