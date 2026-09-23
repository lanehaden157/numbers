# Improvements Log

Append-only. Concrete changes to this book's repo, most recent last.

## 2026-09-22
- Bootstrapped from `bible-core/template/` (core `0.1.0`, commit `ecd5bf6`) via `tools/core_sync.py`. `book.json` filled (osis Num, slug numbers); `groupings` left empty pending the unit map.
- `npm install` (morphhb 2.0.2, sha1-verified against Joshua's copy); `python -m biblecore corpus` → 1,289 verses / 16,422 words / 94 pe / 65 samekh (BHS check still open).
- Filled the style reference's ✎ sections: proposed `table.list`, `.poem`, `.itin` components (not built — H4), genre cautions (census numbers crux, law voice, list collapsing, itinerary uncertainty, poetry parallelism), two candidate groupings (generation vs. geography).
- Filled chat-side instructions' lens section with Numbers-specific reading notes and forward-reuse leads.
- `python -m biblecore build` clean (0 units).

