# Session summary: 2026-09-27, unit 3

## Done
- Ported unit 3 (Num 3:1–51, "Aharon's line and the Levites in place of the firstborn").
- Lane's answers:
  - zar → **stranger / strange fire**, with unit 1's 1:51 changed to match.
  - toledot kept.
  - **redemption price** instead of "ransom".
  - **at the mouth of Yahweh** kept literal, after Lane first picked "at Yahweh's command" and then asked what it was.
  - pequddah (6486) joins `account`.
- Promoted stranger, near, holy and firstborn. Redemption stays local until 18:15–16.
- Retro-tagged unit 1: near at 1:51, firstborn at 1:20.
- Checks: build ok, audit 0 gaps, test 8/8.

## Takeaways
- Tracked-thread spans inside a `data-verses` table used to fail validation because they had no data-w. Core 0.9.1 (`80642f8`) now treats them as colour-only summary tags, so unit 3's table keeps its colours.
- Drafts still spell soft pe as f in names, so check names against the ph rule on every port.
- If Lane picks an unexpected option, a short explanation can change the answer. al pi YHWH did.

## Open
- bible-core `80642f8` (0.9.1) is not pushed yet.
- Carried over: `CHAT_SIDE_INSTRUCTIONS.md` re-paste. Numbers is not pushed.
