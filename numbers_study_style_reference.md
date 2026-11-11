# Numbers Study — Style Reference

Numbers' differences from `fragment-contract.md` (shared, read first). This
file wins.

## Components

On: echo, list, poem, itin, textform, story, mirror (`book.json`
`"components"`; markup in `components-reference.md`). Where Numbers uses each:

- **echo** (`aside.echo`): verse-level cross-book link.
- **story** (`aside.story`): earlier event with the same shape, such as the
  rock (Exod 17) beside 20:2–13 or the manna (Exod 16) beside ch. 11.
- **list** (`table.list`): the censuses (1, 26), camp order (2), Levite counts
  (3–4), tribal offerings (7), boundary lists (34), city lists (35). Collapse
  a repeated formula to one row with the variable called out; declare the
  verses it replaces (`data-verses="1:22–43"`).
- **poem** (`div.poem`): priestly blessing (6:24–26), ark sayings (10:35–36),
  victory songs (21:14–15, 17–18, 27–30), Balaam oracles (23:7–10, 18–24;
  24:3–9, 15–24). Don't run poetry as prose.
- **itin** (`div.itin`): the forty-two stations of ch. 33.
- **textform** (`aside.textform`): where LXX, Samaritan Pentateuch or Qumran
  read differently and it matters to the reading.
- **mirror** (`aside.mirror`): the Exodus twin of a stretch of Numbers, for a
  pair in `data/mirror-exodus.json` (the reading that Exod 5–18 returns in
  reverse in Num 10–24; a reading, not a fact). The unit pack's Exodus mirror
  section gives the pair, the twin's text, the shared words. Never raise a
  strength above what the shared words support. Pair the file lacks → meta
  block's `mirror[]` (`{ref, to, tier, title, strength, shared?, note}`) for
  Lane to decide; never write the data file. `mirror` is an allowed top-level
  meta key here.

## What belongs where

Each link lives in exactly one place:

| The link is… | It goes in |
|---|---|
| A word's history across books | root `echo` |
| One verse or phrase elsewhere sounding through this verse; one sentence says it | `aside.echo` |
| A different earlier event with the same shape, where the reader needs the background | `aside.story` |
| The Exodus twin of this stretch, from a pair in the mirror file | `aside.mirror` |
| A direct quotation of earlier Scripture | `intertext[]`, kind `quotation` |
| A contested reading, an argument about a link, a debate that needs room | footnote |

A story box holds its own word-level evidence: no echo for the same link. A
later retelling (Deut 1–3) is an echo or a footnote. Story and mirror boxes
are harvested like echoes: don't repeat them in `intertext[]`. Every story box
tells the story, states a difference, says what it does here.

**Handoff box kinds:** story → `aside.story`; echo → `aside.echo`; type-scene
→ the story box's `data-scene` when it is told, otherwise a `typescenes[]`
entry; intertext and quotations → `intertext[]`. No OT pointer or
parallel/synoptic box in Numbers: footnote or echo.

## Hebrew in English

**Transliteration** follows core's Hebrew adapter (`biblecore/lang/hebrew.py`):
diacritic only where the plain letter is already claimed (`ḥ ṭ ś`, `ʾ`/`ʿ`);
no vowel length; no spirantization; dagesh forte doubles; divine name `YHWH`,
rendered **Yahweh**.

**Translation.** Fresh, wooden-but-readable rendering from the Hebrew, not a
polish of an existing English version. Creative, intentional glosses
encouraged.

**Ids.** One root often spans several Strong's numbers, and one number can
bundle senses worth splitting. Bare id (`2416`) claims every lexeme under the
number; suffixed id (`2416e`) claims exactly one. Copy ids from the pack or
the `lemma` column of `Numbers-words.tsv` (`"6485 a"` and `"6485a"` both
work); don't guess. `candidates[]` needs `ids` here.

## Judgment

- Structure markers: Masoretic paragraph breaks (`candidate-boundaries.md`).
  Where they and the patterns you notice disagree, argue for the boundary you
  choose.
- Names are joined by hand: place-name wordplay is real, Strong's etymology
  unreliable.

**Genre cautions** (tentative; refine as units surface real cases):

- **Census numbers.** The totals (603,550 in ch. 1; 601,730 in ch. 26) are a
  live crux (a literal two million, or *elef* as "clan/military unit"). State
  the numbers as the text gives them; don't pick a rendering that begs the
  question. Discuss once, in ch. 1, with a footnote pointer from ch. 26.
- **Law.** Render the "if/when... then" structure plainly. No New Testament
  fulfilment or abrogation framing in verse text or gloss.
- **Itinerary (ch. 33).** Most of the forty-two places can't be located with
  confidence. Say so; don't assert a route.
- **Poetry.** Real parallelism, never a rhyme scheme or metre the Hebrew
  doesn't have. The four Balaam oracles escalate (Jacob blessed, a king
  exalted, the star and sceptre): surface that. A chiasm within one oracle
  only if it's there.

## Unit map

`numbers-literary-unit-map.md`: 38 units under 9 movements, inside 2
generation-framed parts (1:1–25:18, 26:1–36:13). `book.json` `groupings` =
`["movement", "part"]`. Renumbering after units ship means editing
`threads.json` opens/payoffs, every `retro` entry and every fragment's meta
block: ask Lane first.
