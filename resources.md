# Numbers Study — Resources

Read before pass 1 of every unit. Cite only the commentators below by name. Where these five can't reach something (a lead, a background question, a cross-reference), say so in the relevant pass and search the web there — don't stretch one of these past its actual content.

## Baruch A. Levine, *Numbers 1–20* (Anchor Bible, 1993)
File: `abNumbers1-20_LevineBA_1993-opt.txt`

Full critical commentary — translation, textual notes (LXX, Samaritan Pentateuch, Peshitta, Targum variants), and extended philological/historical comments. Source-critical method throughout (identifies P, J/E, and other strata) and strong on Ancient Near Eastern comparanda — this is the primary source for the military-census and royal-itinerary background the lens notes call for (chs. 1–4, 20 in this volume). Covers Numbers 1–20. Use it for: philology, ANE parallels, textual variants, the history-of-composition angle on a unit. Its source-critical judgments are a fact about the field, not a verdict to adopt uncritically — note where they shape a reading and where a synchronic reading of the received text differs.

## Baruch A. Levine, *Numbers 21–36* (Anchor Bible, 2000)
File: `abNumbers21-36_LevineBA_2000.txt`

Companion volume, same method and strengths as above, covering the Transjordan narratives, the Balaam pericope (22–24), Baal Peor (25), the second census and homicide/inheritance law (26–30), the Midian campaign (31), Transjordan settlement (32), the itinerary (33), and the boundary/inheritance material (34–36). Includes maps (Israel in Transjordan, the Moabite Stele evidence for ch. 21, the two Kadesh-to-Moab route options, greater Canaan's boundaries per ch. 34) worth pulling into pre-read briefings for those units.

## Thomas L. Constable, *Notes on Numbers* (2015 ed.)
File: `040125_Expository_Notes_on_the_Whole_Bible___Numbers__Thomas_Constable_.txt`

Conservative evangelical expository commentary, verse-by-verse, traditional Mosaic-authorship position, dispensational leaning. Its own argument is thinner than Levine's, but its bibliography is enormous and it functions as a digest of a wide range of other commentators (Wenham, Ashley, Milgrom, Wiersbe, and many journal articles) — useful for surfacing where a crux has been discussed elsewhere even when Constable's own take is brief. Good for quick doctrinal/devotional orientation and NT cross-references; treat its citations of other scholars as leads to verify, not as Constable's own research.

## William Whitt, *Numbers: A New Translation with Commentary* (Cutting Horse Press, 2022)
File: `New_Text_Document.txt`

A fresh translation with composition-history notes, source-critical (JEDP-informed) throughout. Its standout feature for this project: Whitt explicitly follows the Masoretic **parashah** divisions rather than the medieval chapter breaks — the *parashah petuhah* ("open," major unit) marked with a triple line break and `**`, the *parashah setumah* ("closed," minor unit) marked with a single line break and an em-dash — following the Aleppo Codex, cross-checked against the Qumran evidence for how old these divisions are. This is the direct source for "prefer the book's own... Masoretic paragraph breaks" in the lens notes — check it first when a unit's boundary is in question. Also useful for a second, more literal-leaning translation to set against the NT-adjacent English Lane already reads devotionally, and for the composition-history angle alongside Levine.

## *Rashi on Numbers* (Rosenbaum–Silbermann translation, merged with a Sefaria/National Library of Israel Hebrew text)
File: `Rashi_on_Numbers_-_en_-_merged.txt`

Classical medieval commentary, verse-by-verse, English translation alongside the original Hebrew lemmas and running text. Per the lens notes, weigh Rashi specifically at the census material (chs. 1–4, 26) and the Balaam narrative (22–24) — real, substantive comments there — rather than as a running presence through legal or itinerary units where he has little to add.

**Operational note:** this file contains native Hebrew script (both Rashi's lemma citations and the surrounding Masoretic verse text). Per Lane's standing rule, never copy that script into chat or an artifact — always transliterate and gloss any Hebrew pulled from this file before it's used.

## Gaps — not on hand

No Milgrom (JPS), Wenham (Tyndale), Ashley (NICOT), or Sailhamer in the project files; Constable's bibliography names them secondhand but their actual arguments aren't available here. Flag any unit where one of these would materially change the reading, and search the web for it in pass 2 rather than relying on Constable's summary.

## The synced folder

The repo pushes seven files into this project's `synced/` folder (via the GitHub connector reading `project-side/synced/` in the repo — see the repo's `project-side/README.md` for the round-trip). They round-trip automatically; don't edit them here. `python -m biblecore sync` on Lane's side refreshes them whenever the repo's copy changes, so re-read a file from `synced/` if a session note or Lane says it's stale rather than trusting an earlier read in this conversation.

**`numbers_study_style_reference.md`** — the artifact-shape reference for pass 4. Every structural rule for a fragment (the meta block, roots/threads/questions shape, glosses vs. footnotes, the optional components) lives here; it is authoritative over anything summarized about it elsewhere, including in these study instructions.

**`translation-choices.md`** — this book's own glossary of deliberate English rendering decisions, starting from `canon-conventions.md`'s defaults and recording only where Numbers deviates or decides something canon-conventions doesn't cover. Currently empty (seeded at unit 1 on purpose, unlike Matthew) — check it before rendering any lexeme once units start shipping.

**`canon-conventions.md`** — the cross-book defaults shared with Joshua and Matthew (y'all/y'all's, Yahweh for the divine name, sky/skies, ḥesed left untranslated, etc.), vendored from `bible-core/canon/conventions.md`. Defaults, not rules — `translation-choices.md` overrides a row here when Numbers has a real reason to.

**`threads-digest.md`** — the generated, human-readable digest of `data/threads.json` (the tracked-thread registry: which roots get a colour and a `data-root` tag book-wide, versus a unit-local root tagged with no colour). Currently 0 threads — nothing has been promoted book-wide yet, since no unit has shipped. Once threads exist, this is the reference for which roots are tracked vs. local when drafting a fragment's meta block.

**`roots.json`** (synced as `roots.json`, from the repo's `data/roots.json`) — the tracked-thread id sets and the declined-candidate ledger (candidates considered and deliberately kept local, with the reason, so they aren't re-argued). Currently empty. This is policy Lane applies by hand, not something the porter writes.

**`Numbers-words.tsv`** — the full word table for the book: one row per Hebrew word token, with a `word_id`, its verse reference, the surface form, the Strong's/lemma id, and the morphology code. This is where a lemma id for a `threads.candidates` proposal comes from (search by lemma column) — don't hand-guess an id.

**`numbers-literary-unit-map.md`** — the 38-unit map this project delivered by hand, now the repo's canonical copy (it drives `book.json`'s `groupings` and `data/units.json`'s grouping definitions), synced back here so it stays current if it's ever revised. Confirmed before unit 1: 9 movements nested in 2 generation-framed parts, each unit's passage, working title, petuḥah/setumah markers (Leningrad and Aleppo, with disagreements noted), why the boundary falls where it does, and relevant commentator notes. This is what "state the unit and passage from the Literary Unit Map" in the study instructions' Scope section refers to.

`canon-leads-unit-NN.md` (the per-unit intertext seed sheet that pass 3 starts from) is also meant to land in this same `synced/` folder, one file per built unit, but none exist yet since no unit has shipped — the repo's sync glob picks them up automatically as they're generated.
