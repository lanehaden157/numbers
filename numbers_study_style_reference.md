# Numbers Study — Style Reference

> **The artifact contract.** What a unit artifact must contain and must not.
> `CHAT_SIDE_INSTRUCTIONS.md` and `core-workflow.md` say how to work;
> `resources.md` says what's on hand; `CLAUDE.md` says how the repo behaves.
> Each rule lives in one of them. `synced-index.md` lists every synced file.

A guide, not a spec: where a rule gives a reason, the reason outranks the rule.
Rules marked **(learned)** cost something to find in an earlier book — read
the lesson before relaxing one. This file starts as the shared defaults from
`bible-core/ARCHITECTURE.md`; **sections marked ✎ are this book's to decide**,
and anything else can change too, with the reason written here.

---

## 1. Colour policy

One **lexical root** per `data-root` — the root and its same-root forms,
never a theme or a bundle of words. Split a paired opposition into two roots;
drop a one-passage wordplay. Fixed phrases the book repeats verbatim are the one
exception and live in `threads.json`.

Tag **every** occurrence with the one slug, **including where the English uses a
different word** — the tag follows the lexeme, not the gloss.

`translit` is one bare root form (Hebrew books), not a list of inflected forms;
`gloss` is plain English (§3). No stem/binyan labels. A stem split that matters
goes in a thread `note` or a verse `.gloss`, in plain language.

Every slug must resolve — in `threads-digest.md` or this artifact's `roots[]` —
or the build fails. **`roots[]` is local roots only**: don't re-declare a
tracked thread there; `data/threads.json` is its single source of truth.

**Tag notable words even when they aren't threads.** A single striking
translation choice in a single verse earns a `data-root` span and a full
`{root, translit, gloss}` entry. Read for these deliberately.

**`example`** — optional on any root: one short quoted clause from the unit's
own English, no citation.

**`echo`** — optional on any root: one line saying where the word has already
appeared, or where it reappears distinctively later, shown in the root's
popover with a "cf.". Lead with the reference, then what it adds. Echoes come
from the kept rows of the intertext pass's ledger, not from memory at
drafting time.

**Resist a richer taxonomy. (learned:** a root/motif two-tier model was built
and reverted the same day. Root vs. stem vs. semantic field gets the same
answer: one slug, one colour.**)**

---

## 2. Root identity — ids, not strings

**A root is a hand-curated set of lemma ids in `roots.json`; every tracked
thread occurrence carries its word id** (`data-w`, from `Numbers-words.tsv`).
No original-language string is ever compared to another. **(learned:**
consonant-substring matching measured 0–42% recall on Joshua's weak-root
verbs.**)**

One root often spans several Strong's numbers, and one number can bundle
senses worth splitting, so a root is a **decision**, recorded as an id set
with a note. A bare id (`2416`) claims every lexeme under the number; a
suffixed id (`2416e`) claims exactly one.

```html
<span class="r" data-root="devote" data-w="068w5">devoted</span>
```

Local roots don't need `data-w`. **You never hand-chase word ids**: the porter
fills them by per-verse alignment and reports the few it can't decide.

**Never hand-type Hebrew; pull by word id. (learned:** NFC normalisation alone
reorders marks in 47% of Joshua's words.**)**

---

## 3. The hard contract

The artifact is **one `<article class="unit" data-unit="N">` and nothing
else** — no doctype/html/head/body/style/link, no inline `style`, no `--c-*`
vars. It opens with `<script type="application/json" id="unit-meta">`.

**Unknown top-level keys are a hard error. (learned:** Matthew's `descriptor`
and `discourse` were authored for eleven units and silently discarded.**)**

### Top-level keys

| key | required | type | rule |
|---|---|---|---|
| `unit` | ✓ | int | an integer, not a string |
| `passage` | ✓ | str | `"Numbers 6:1–27"` |
| `title` | ✓ | str | |
| `roots` | ✓ | array | §1 |
| `threads` | ✓ | object | all four sub-keys, empty lists fine |
| `slug` | — | str | `"unit-06"`; derived from `unit` if omitted |
| ✎ grouping keys | — | int | one per grouping kind in `book.json` (e.g. `movement`); looked up from the unit map if omitted |
| `questions` | — | array | wording/data calls only Lane can make, §3a |
| `intertext` | — | array | cross-book links worth recording, below |
| `typescenes` | — | array | type-scene instances in this unit, below |

### `intertext[]` and `typescenes[]` — canon rows (optional)

The porter moves these into `data/canon.json` and the canon registries in
`bible-core/canon/`; they aren't re-emitted in the built meta block.

- `intertext[]` — `{ref, to, kind, note?}`: `ref` a bare `"C:V"` in this
  book, `to` a reference like `"Ps 67:1"`, `kind` one of `quotation`,
  `allusion`, `echo`, `type-scene`. An `aside.echo` or a root's `echo` is
  already harvested as an `echo` edge, so list here only what those don't
  say: a quotation, an allusion without an aside, a link worth keeping
  without cluttering the page.
- `typescenes[]` — `{id, ref, note?, label?}`: `id` from the type-scene
  index (`commissioning`, `scouts`, `water-crossing`, `census`,
  `mountain-theophany`, `annunciation`, ...). A new `id` is fine; give it a
  `label` and it's added to the index for Lane to place under an arc.

### `roots[]` — every entry `{root, translit, gloss, example?, echo?}`

`root` matches `[a-z0-9-]+`. **No** `color`/`colour`, **no** `kind`/`members`,
no other keys. `gloss` is a short general definition — no stem or
part-of-speech labels. Never seed a gloss from Strong's first definition
(misleading in 9 of 16 sampled Joshua words).

### `threads` — `{opens, payoffs, candidates, retro}`

All four present, each a list, empty allowed.

**`opens[]` / `payoffs[]`** — `{id, ref, note}`. `id` must exist in
`threads-digest.md` (propose new ones via `candidates`); `note` is the
one-line popover prose.

**`candidates[]`** — `{root, why, ids?, refs?}`. Proposals only; `ids` are the
lemma ids you saw (evidence), `refs` a few representative verses. Formats
are checked at port time:

- `ids` — the `lemma` column of `Numbers-words.tsv` with prefixes removed.
  Either spelling works: the table writes `6485 a` and the porter reads it
  as `"6485a"`. Look it up there; don't guess.
- `refs` — bare `"C:V"` strings only: `"1:3"`, not `"Num 1:3"`. No ranges
  (`"3:7–8"`): list each verse (`"3:7", "3:8"`).
- Give every candidate an `ids` entry so the evidence is checkable.

**Claude
decides whether a candidate is promoted, biased toward book-wide**, and asks
Lane only when genuinely unsure.

**`retro[]`** — `{unit, verse, text, root, why, nth?, op?, w?}`. Fixes for
**earlier** units (`unit` is a slug like `"unit-04"`). `why` required. `op` ∈
`add` (default), `retag`, `retag_word`, `untag_word`, `unwrap`, `strip_span`,
`text`. `w` is optional — the porter fills it.

---

## 3a. `questions[]` — asking Lane in Claude Code, not on the project side

**`questions[]`** — `{topic, note, options?}`. A wording or data call only Lane
can make goes here **instead of** being asked in chat. `topic` is a few words;
`note` is the question, answerable cold; `options` optional short answers.
Render your best provisional choice so the draft keeps moving, and flag it.
Claude Code then asks Lane each question in the AskUserQuestion popup
(multiple choice, `options` become the choices, best provisional first) —
not as a chat list. The porter prints every question at port time; the decision then goes in
`translation-choices.md` or the thread/root entry.

---

## 4. Components

Deliberately small. The base components below are in every book. **Optional
components** come from bible-core's component registry: `book.json`
`"components"` enables them (Numbers: echo, list, poem, itin, textform),
any unit may use any enabled one, and **`components-reference.md`** (synced,
generated by the build) holds the exact markup and rules for each. A class
that's neither base nor an enabled component fails the build by name. **A new
class is a decision**, so it goes into the registry with its CSS, its check and
its snippet.

| component | shape | note |
|---|---|---|
| coloured word | `<span class="r" data-root="X" data-w="…">…</span>` | `class="rl"` only **outside** verse blocks |
| verse | `<p class="v"><span class="n">17</span> … text<sup class="en"><a href="#n1">1</a></sup></p>` | one per verse, in order. The endnote marker is the last thing in the verse `<p>`, **never** inside the `.gloss` |
| gloss | `<span class="gloss">…</span>` | **following sibling** of the verse, never nested, always closed. Short |
| pericope heading | `<h3 class="pericope">Title <span>· 6:1–7</span></h3>` | `· C:V` range required |
| legend | `<section class="block legend" aria-label="color key"><ul></ul></section>` | **required, even as an empty stub** |
| notes | `<div class="notes"><h2>Notes</h2><ol><li id="n3"><strong>hid him (v4).</strong> …</li></ol></div>` | every `href` resolves to an `id` in the fragment |

**Where Numbers uses each optional component** (markup and rules in
`components-reference.md`):

- **echo** (`aside.echo`): a verse-level cross-book link.
- **list** (`table.list`): the censuses (1, 26), the camp order (2), the Levite
  counts (3–4), the twelve near-identical tribal offerings (7), the boundary
  lists (34), and the refuge-city and Levite-city lists (35). Collapse large
  blocks of repeated formula to one row, with the variable called out. Don't
  write out twelve paragraphs of "on the Nth day, NAME the son of NAME … offered".
  See *Balance* below. A table that replaces verses declares them with
  `data-verses="1:22–43"` (Lane, 2026-09-23).
- **poem** (`div.poem` around ordinary verse blocks whose text is set in
  `span.l` lines): the priestly blessing (6:24–26), the ark sayings
  (10:35–36), the victory songs (21:14–15, 17–18, 27–30), and the Balaam oracles
  (23:7–10, 18–24; 24:3–9, 15–24). The line break *is* the argument: `span.l in`
  indents the second half of a parallel couplet. Don't run poetry as prose with a
  note explaining the parallelism after the fact.
- **itin** (`div.itin` chips in a `section.block`): the forty-two stations of
  ch. 33, which is exactly that shape and gains nothing from prose. Use
  `data-verses` when the chips replace the station verses.
- **textform** (`aside.textform data-src="lxx|sp|dss|…"`): where the LXX,
  Samaritan Pentateuch or Qumran read differently and it matters to the
  reading. Levine's textual notes are the usual source.

**Not proposed:** a dedicated law-code component. Law reads as ordinary
verse text, with `.gloss` or footnotes for the casuistic "if… then" structure
when it matters. Deuteronomy-family books will likely make the same call, so a
component isn't obviously worth it until one of them needs it too.

**(learned:** endnote markers inside `.gloss` hid the footnote behind the
toggle; the legend was once "optional" and a unit shipped with no colour key;
asides spliced inside unclosed glosses silently collapsed.**)**

### Balance — what goes where

Strong suggestions:

- **Glosses stay short** — a phrase or one sentence, roughly 25 words or
  fewer. A grammar point, a textual variant, a debate between readings goes
  in a **footnote**.
- **Grammar and medieval commentary are seasoning, not the meal.** Include a
  grammar point when it changes how the verse reads.
- **Intertextuality is the main course.** Say where earlier Scripture stands
  behind a line and where a line reappears later, including in the New
  Testament. `aside.echo` for a verse-level link, a root `echo` for a word.

**Voice: no named commentators or resources, and no project-internal
references, anywhere in fragment prose.** Where views differ, say so in
general terms and give the content of the disagreement. **(learned:** Joshua
unit 1's first draft named eight sources and two repo files.**)**

---

## 5. Hebrew in English ✎

**Transliteration** comes only from the core's Hebrew adapter
(`biblecore/lang/hebrew.py`; its test file is the authoritative definition).
Scheme: a diacritic only where the plain letter is already claimed (`ḥ ṭ ś`,
`ʾ`/`ʿ`); no vowel length; no spirantization; dagesh forte doubles; `יהוה` →
`YHWH`, rendered **Yahweh**.

**Translation philosophy.** A fresh, wooden-but-readable rendering from the
Hebrew, not a polish of an existing English version. Creative, intentional
glosses are encouraged.

**Wording.** Check `translation-choices.md` (which starts from
`canon-conventions.md`) before rendering a lexeme. A better
verse-specific rendering is fine — **flag the deviation**. Update the file in
the same turn as any wording decision. **(learned:** Matthew started its
glossary at unit 10 and paid with a retroactive audit.**)**

---

## 6. Judgment

**Be tough on structures.** Chiasms and rings only when textually verifiable.
Prefer the Masoretic paragraph breaks (`candidate-boundaries.md`) over
patterns you noticed. **(learned:** eight over-reaching chiasms were cut from
Matthew.**)**

**`threads.json` and `roots.json` are Lane's policy.** Nothing in the pipeline
writes either.

**Names are joined by hand.** Place-name wordplay is real but Strong's
etymology is unreliable. Add names to `roots.json` one at a time, with the
reason.

✎ **Genre cautions for this book — tentative, refine as units surface real
cases:**

- **Census numbers.** The totals (603,550 in ch. 1; 601,730 in ch. 26) are a
  live scholarly crux (a literal ~2 million people in the wilderness vs.
  *elef* read as "clan/military unit" rather than "thousand," among other
  proposals). State the numbers as the text gives them, note that the
  question exists and what's at stake exegetically, and don't quietly
  resolve it by picking a translation that begs the question. Not a crux to
  relitigate in every unit that touches a number — once, where it first
  matters (ch. 1), with a footnote pointer from ch. 26.
- **Law.** Render the casuistic "if/when... then" structure plainly; a
  grammar footnote earns its place only when the conditional structure
  itself is the point (e.g. the Nazirite vow's contingencies, 6:1–21). Don't
  import New Testament fulfillment/abrogation framing into the verse text or
  gloss — that's commentary-dialogue material for pass 2, not the
  translation.
- **Lists (census, camp order, offerings, boundaries).** Formulaic
  repetition is the genre, not a bug — but a reader doesn't need "Nadab and
  Abihu" spelled out with patronymic and tribe twelve times running when the
  pattern is `<name>, son of <name>, tribe of <name>: <items>`. Collapse to a
  table (`table.list` above) rather than translating every repetition as
  full prose; say so in the pericope's gloss so the collapse is visible, not
  silent.
- **Itinerary (ch. 33).** Most of the forty-two place names can't be located
  with confidence. Say so plainly rather than asserting a route on a map;
  where a location is genuinely uncertain, the footnote says uncertain — no
  invented certainty for the sake of a tidy travelogue.
- **Poetry (Balaam's oracles, the victory songs, the blessing).** Real
  parallelism (`.poem` above), never a rhyme scheme or metre the Hebrew
  doesn't have. Balaam's oracles are also a structural chiasm-risk case (§6
  above already warns against imposed structure) — the four-oracle sequence
  has a real escalating shape (Jacob/Israel blessed → a king/kingdom exalted
  → the star and sceptre) that's worth surfacing; a chiasm *within* one
  oracle's four lines is not, unless it's actually there.
- **Type-scenes worth watching for, across units:** the spies' report
  (13–14) against Joshua and Caleb's minority report — read against the
  conquest generation's death sentence and the second generation's second
  chance; Balaam, the outside prophet who cannot curse what Yahweh has
  blessed (22–24); Zelophehad's daughters' legal petition and its answer
  (27, closed out at 36) as a real instance of law developing inside the
  narrative, not handed down complete.

---

## 7. Before saving — the checklist

1. One `<article>`, nothing above or below it.
2. Meta parses as JSON; required keys and all four `threads` sub-keys; no
   unknown top-level keys.
3. Every `roots[]` entry: `root` + bare `translit` + plain `gloss`, optional
   `example`/`echo`; nothing else.
4. Every notable translation choice has a local span and `roots[]` entry, and
   so does every word with a canon history, with an `echo`.
5. Every `opens`/`payoffs` `id` is in `threads-digest.md` and has a `note`.
6. Every `retro` targets an earlier unit, has a `why`, and resolves.
7. Every `data-root` is in `threads-digest.md` or `roots[]`.
8. Legend present, stub or filled.
9. Every pericope heading has its `· C:V` range.
10. `.gloss` and `aside.echo` blocks are closed following siblings, never
    nested; every `aside.echo` has a `data-anchor` matching its verse.
11. Every endnote `href` resolves to an `id` in the file.
12. **Zero native Hebrew or Greek anywhere — attribute values included.**
13. No inline `style`, no `--c-*` vars, no class the stylesheet doesn't know.
14. Wording matches `translation-choices.md`, or the deviation is flagged.
15. No named commentator or project-internal reference in prose.
16. Glosses are short, longer material is in footnotes, and the unit's
    intertextual links are surfaced.

Save as `numbers_NN_translation.html`, zero-padded, and present the file.

---

## 8. Worked example ✎

Replace with a minimal, valid example from this book's own unit 1 once it
exists. Until then the shape is:

```html
<article class="unit" data-unit="1">
<script type="application/json" id="unit-meta">
{
  "unit": 1,
  "passage": "Numbers 1:1–10",
  "title": "Working Title",
  "roots": [
    { "root": "count", "translit": "paqad", "gloss": "count, muster, attend to",
      "echo": "Gen 50:24 — 'God will surely attend to you'" }
  ],
  "threads": { "opens": [], "payoffs": [], "candidates": [], "retro": [] }
}
</script>

<header class="mast">
  <div class="kicker">The Book of Numbers · Study Translation</div>
  <h1>Working Title</h1>
  <div class="unit">Unit 1 · Numbers 1:1–10</div>
</header>

<section class="block legend" aria-label="color key"><ul></ul></section>

<h3 class="pericope">Heading <span>· 1:1–3</span></h3>

<p class="v"><span class="n">1</span> Verse text with a
<span class="r" data-root="count">counted</span> word.<sup class="en"><a href="#n1">1</a></sup></p>
<span class="gloss"><em>counted</em> — a short note.</span>

<div class="notes">
  <h2>Notes</h2>
  <ol>
  <li id="n1"><strong>counted (v1).</strong> The longer discussion.</li>
  </ol>
</div>
</article>
```

---

## 9. The Literary Unit Map — delivered

Delivered from the project side (2026-09-22) as `numbers-literary-unit-map.md`:
38 units under 9 movements, themselves bracketed by 2 generation-framed
parts (1:1–25:18, 26:1–36:13). The two candidate framings once weighed here
(generation vs. geography) weren't a choice after all — the map combines
both, nested. `book.json`'s `groupings` is `["movement", "part"]`;
`data/units.json`'s `groupings[]` holds the full definitions (span, label,
member units). Renumbering after units ship means editing `threads.json`
opens/payoffs, every `retro` entry, and every fragment's meta block, so this
is confirmed before unit 1, not after.
