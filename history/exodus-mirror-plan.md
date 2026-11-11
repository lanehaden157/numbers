# Exodus ⇄ Numbers mirror: implementation plan (v1)

Status: plan only, nothing built. Decisions settled with Lane on 2026-11-10.
Source idea: Carmen Imes's reading that Exod 5–18 returns in reverse in Num 10–24,
with Sinai (Exod 19:1 – Num 10:10) at the centre. Treat it as a reading, not a fact.

## Decisions

- Generic **bible-core feature**, switched on per book. Numbers is the first user.
- **English versification** in all stored refs. Core already converts any OSHB book through
  `wlc/VerseMap.xml` (`versify.py`), so this covers Exodus too (Exod 8 and 22 shift).
- **Two tiers.** `chiasm` pairs have a position in the mirror. `echo` pairs are looser
  Exodus⇄Numbers parallels with no position (for example Exod 32 / Num 25).
- **Pair A keeps Imes's width** (Exod 5–15). B, C and D nest inside it, and the data shows
  that rather than hiding it.
- **Strength** is 1–3 dots labelled "Lane's read" (3 = shared words, 2 = same story beat,
  1 = thematic). It's stored in the data and Lane edits it.
- **Exodus English** comes from the chat, which translates the twin while it ports the Numbers unit.
- **Discovery.** The chat proposes new pairs in its port output, Lane decides through the popup,
  and kept pairs are written to the data file. The data file is policy, like `threads.json`.
- **Shared words** (for example kaved and levad in pair H) are highlighted inside the mirror box,
  and the build checks that each one is really in both passages.
- **v1 covers** the data, the checks, an Exodus section in each unit's prep sheet (unit pack),
  and a `mirror` box in the units. Deferred: the map page, the reader chip, and the
  "read its mirror" nudge.

## Verified so far (OSHB lemmas, morphhb 2.0.2)

| Pair | Claim | Result |
|---|---|---|
| F | Joshua (H3091) in both passages | Pass: Exod 17:9, 10, 13, 14; Num 13:16, 14:6, 30, 38 |
| H | kaved (H3515) and levad (H905) in Exod 18:18 and Num 11:14 | Pass in both verses (and both read *mimmekka / mimmenni*, "from you / from me") |
| I | Midian/Midianite in both passages | **Fail.** Num 10:29 has it (H4084). In Exodus it's only in 18:1, outside 18:19–27. Strength drops to 2 |
| C | Sihon is "king of the Amorites" | Num 21:21 has Amorite (H567) |

## Steps

### 0. Pre-flight
- Run `git status` in both `bible-core` and `Numbers`. If either is dirty, work in a worktree
  (see "Concurrent sessions" in bible-core's CLAUDE.md).
- The core changes ship as one minor release (0.29.0), then Numbers vendors it.

### 1. Data file: `data/mirror-exodus.json` (Numbers, policy)
- `book.json` gains a key, for example `"mirrors": [{"with": "Exod", "file": "mirror-exodus.json"}]`.
  The key set is closed, so core has to accept it.
- Top level: `centre` (`Exod 19:1 – Num 10:10`, labelled "Imes's boundaries", cloud lifts 10:11–13),
  `sources` (Imes 2021 and 2019, ESV Global Study Bible chart, Lawlor BBR 21.1, with Lawlor's
  different boundary noted), and `pairs[]`.
- Each pair: `id`, `tier` (`chiasm` | `echo`), `pos` (outside-in, chiasm only), `numbers`,
  `other`, `title`, `strength`, `poetry` (`num` | `other` | `both`), `shared[]`
  (`{label, ids: [Strong's], where: {numbers: ref, other: ref}}`), `status` (`seed` | `kept`),
  `source`, and `note`.
- Seed it with the nine chiasm pairs A–I and the four ESV echoes (Exod 32:6/Num 25:2, 32:27/25:5,
  32:28–29/25:6–13, 32:35/25:9). Pair I is strength 2. Pair H's `shared` lists kaved and levad;
  pair F's lists Joshua.

### 2. Core: second-book reading
- A helper loads another OSHB book (for example `Exod.xml`) through `corpus/oshb.py` and
  `versify.py`, returning words with lemma, transliteration and English refs. Only
  `language: hebrew` books can mirror for now. Matthew's LXX path can come later.

### 3. Core: `mirror` check, run by `biblecore test` and `build`
- Every ref resolves in its corpus.
- Every `shared` entry's lemma IDs occur in both of its `where` refs. A strength-3 pair needs at
  least one passing `shared` entry; without one the check fails (it doesn't quietly downgrade).
- Report, but don't fail, on nesting and overlap (A ⊃ B, C, D; E spanning units 15–22) and on
  chiasm pairs whose order doesn't reverse cleanly. The map will show this later.
- Poetry sides are allowed. Nothing here parses poetry.

### 4. Core: Exodus section in the unit pack (`unit_pack.py`)
For each unit that overlaps a pair's Numbers side, add a section "Exodus mirror" with:
- the pair (title, tier, strength, Imes or proposed status), and the twin ref;
- the twin's Hebrew verse lines with transliteration and Strong's numbers, so the chat can
  translate it (glosses only where `lemmas.json` already has them; the chat supplies the rest);
- the lemmas the two passages share, rarest first, as **leads, not conclusions**, in the same
  style as the existing "Shared phrases with the Torah";
- for units with no pair, a short list of Exod 1–40 verses that share rare lemmas or two-word
  phrases with the unit (reusing `leads.py`'s phrase/rare logic, limited to Exodus), as raw
  material for proposing new connections.

Units with chiasm pairs: 10 (I), 11 (H), 12 (G), 13–14 (F), 15–22 (E; it starts at 15:32),
22 (D), 23 (C), 24–25 (B; 22:21 is in unit 24), 26–27 (A); 28 for the ESV echoes.
Units 1–9 sit inside the Sinai centre, so they have no pairs and need no retrofit.

### 5. Core: `mirror` component (`biblecore/components/mirror/`)
Modelled on `synoptic`:

```html
<aside class="mirror" data-anchor="11:14" data-pair="H" data-span="11:10–17">
  <h4><span class="par-title">The burden: too heavy … alone</span>
      <span class="par-ref">Exod 18:13–18</span>
      <span class="strength" data-n="3" title="Lane's read">●●●</span></h4>
  <div class="row"><span class="src">Exod 18:18</span><span class="txt">… <span class="sh" data-ids="3515">heavy</span> … <span class="sh" data-ids="905">alone</span></span></div>
  <p class="take">What the mirror shows here.</p>
</aside>
```

- Rules: `data-pair` must exist in the data file with status `seed` or `kept`; `data-anchor`
  is inside the unit; each `.sh` span's ids are in that pair's `shared` list; the
  `strength` dots match the data file (the build fills them in, so the chat doesn't have to).
- A poetry twin gets the ref and title only, with no rows, until poetry is in scope.
- An `echo`-tier pair uses the same box with no position or dots, or a one-line `aside.echo`
  if a sentence carries it.
- Canon: boxes are harvested into `data/canon.json` as intertext kind `mirror`, which needs
  a new entry in `canon.py` `KINDS`.
- Add `style.css` and `snippet.md`; the registry generates `components-reference.md`.

### 6. Core: proposals from the port
- New optional meta key `mirror[]`: `{ref, to, tier, title, strength, shared?, note}`.
- The port validates it (refs resolve, shared lemmas present), writes candidates to
  `out/mirror-delta.json`, and raises each one as a question. A kept proposal is written to the
  data file as `status: kept`. Lane decides; the porter never writes it on its own.

### 7. Chat side (Numbers)
- In the style reference, add a short "Exodus mirror" part to the component section:
  - when to ship a box, and when an echo is enough;
  - translate the twin in the unit's voice;
  - never raise a strength above what the shared words support;
  - propose new pairs in `mirror[]`.
- If needed, add a pointer in `core-workflow.md` (core) about using the pack's mirror section.
- Run `biblecore sync` once Lane gives the OK.

### 8. Tests and release
- Core: selftest for the check (a bad ref, a missing shared lemma, a strength 3 with no
  evidence), the component validator, and the pack section.
- Numbers: `python -m biblecore test` is green with the seed data and units 1–4 unchanged.
- Release core 0.29.0, vendor it into Numbers, build, commit, push, sync.

## Later (not v1)
- **Mirror map page.** Exodus column, Numbers column, Sinai centre, nesting drawn, with a
  "pairs / reading order" toggle.
- **Reader chip** when the open unit has a pair.
- **"Read its mirror" nudge**, off by default, with no streaks.
- An Exodus study in the hub would give the Exodus side a place to jump to.

## Open risks
- Glosses for Exodus-only lemmas: `lemmas.json` is built from Numbers, so the pack will have
  gaps that the chat fills.
- Pair B is listed as Num 22:21–35, but unit 25 starts at 22:22. The box anchors in unit 25,
  and 22:21 stays in unit 24 with no box.
- Pair E (Num 15:32–21:9) is too wide for one box. Plan on one box per sub-beat (manna and
  Sabbath, grumbling, water from the rock), each anchored in its own unit and sharing `data-pair="E"`.
