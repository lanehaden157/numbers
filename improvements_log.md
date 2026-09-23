# Improvements Log

Append-only. Concrete changes to this book's repo, most recent last.

## 2026-09-22
- Bootstrapped from `bible-core/template/` (core `0.1.0`, commit `ecd5bf6`) via `tools/core_sync.py`. `book.json` filled (osis Num, slug numbers); `groupings` left empty pending the unit map.
- `npm install` (morphhb 2.0.2, sha1-verified against Joshua's copy); `python -m biblecore corpus` → 1,289 verses / 16,422 words / 94 pe / 65 samekh (BHS check still open).
- Filled the style reference's ✎ sections: proposed `table.list`, `.poem`, `.itin` components (not built — H4), genre cautions (census numbers crux, law voice, list collapsing, itinerary uncertainty, poetry parallelism), two candidate groupings (generation vs. geography).
- Filled chat-side instructions' lens section with Numbers-specific reading notes and forward-reuse leads.
- `python -m biblecore build` clean (0 units).
- Ran `python -m biblecore sync`: mirrored the six `book.json` sync files into `project-side/synced/`, committed and pushed.
- Project side delivered `numbers-literary-unit-map.md` (38 units, 9 movements, 2 generation-framed parts) and `resources.md` (commentary inventory, project-only per `project-side/README.md`). Committed the unit map; `resources.md` stays untracked (project-only).
- Encoded the map into `book.json` (`groupings: ["movement", "part"]`) and `data/units.json` (`groupings[]` with all 11 definitions — 9 movements + 2 parts, span/label/member units; per-unit rows still fill in at port time).
- Resolved the 1,289 vs. 1,288 verse-count question: built `numbers-versification-map.md` from the raw corpus XML plus a live ESV check. Five chapters (16, 17, 25, 26, 29, 30) diverge; the net is one genuine merge (Hebrew 25:19 folds into English 26:1) — everything else is renumbering, not a real count difference.
- Updated `numbers_study_style_reference.md` §9 (unit map now delivered, ✎ removed) and `CLAUDE.md`'s Corpus section (versification resolved; noted `candidate-boundaries.md` vs. the unit map are not redundant — raw machine list vs. authored interpretation).

