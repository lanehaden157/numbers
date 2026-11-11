# Session summary — 2026-09-30 (lens notes move)

## What was done
- Lane asked why the instruction field carried a very specific list of Numbers features. Answer: two of the four lens bullets apply to every unit (generational hinge, "priestly and legal material is not filler"); the other two (forward reuse, type-scenes) are per-unit lookups.
- Moved the per-unit items into `numbers-literary-unit-map.md` at U06, U10, U13, U14, U16, U22, the movement VI intro, U30 and U38. Several were already there (Heb 3–4, John 3:14, 2 Pet/Jude at U25, Rev 2:14 at U28); those were only made more exact.
- `CHAT_SIDE_INSTRUCTIONS.md`: 415 -> 364 words. "Not filler" is one sentence (glory citations dropped); a new bullet points to the unit's map entry before pass 1.
- `units-from-map --dry` leaves all 38 rows untouched; `biblecore test` 8/8; synced.

## Takeaways
- The field should hold only what applies on every turn. Anything keyed to one unit goes in that unit's map entry, which the chat side reads per unit.
- `core-workflow.md` doesn't tell the chat side to read the map entry, so the field's pointer bullet is what makes the moved notes get read.

## Open
- Re-paste `CHAT_SIDE_INSTRUCTIONS.md` into the project field, then `python -m biblecore sync-check --mark-pasted`.
- "The blessing's later use in liturgy" (U06) is still vague; name the texts when unit 6 is walked.
