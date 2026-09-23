# Session summary — 2026-09-22 (bootstrap)

## Done
- Created this repo as a sibling of `Matthew`/`Joshua`, from `bible-core`'s starter template (core `0.1.0`).
- Vendored `biblecore/` via `tools/core_sync.py` (pinned to commit `ecd5bf6`); confirmed a clean `core_diff.py`.
- `npm install` for morphhb 2.0.2; its `Num.xml` is byte-identical to Joshua's pinned copy (sha1 check), so this is the same verified corpus release.
- Built the corpus: 1,289 verses, 16,422 words, 94 petuḥah / 65 setumah.
- Drafted (not finalized) the style reference's book-specific sections and the chat-side instructions' lens section, informed by Numbers' actual genre mix.
- `python -m biblecore build` runs clean with 0 units.

## Takeaways
- The one-verse gap against the commonly cited 1,288-verse English count is expected (Hebrew/English versification drift) but unverified — flagged loudly in `CLAUDE.md` rather than assumed.
- This is real setup work per `bible-core/ARCHITECTURE.md` §8 step 1–3, done ahead of the unit map since it doesn't depend on it.

## Open questions (for Lane / the project side)
- Which grouping (generation vs. geography, or both) for `book.json`'s `groupings` — see style reference §9.
- The unit map itself (`numbers_literary_unit_map.md`), once resources are compiled.
- The proposed `table.list`/`.poem`/`.itin` components (style reference §4) — react to the shapes, nothing is built yet.
- This book's own palette/theme — currently just the template's copy of Joshua's.
- BHS verse-count check for the corpus (`CLAUDE.md` "Corpus").
