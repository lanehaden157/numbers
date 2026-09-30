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
- `python -m biblecore leads` produced nothing for unit 1: `data/units.json`'s per-unit rows are only written by `port` (after drafting), but `leads` needs a unit's passage before pass 1. Added a minimal pre-port row for unit 1 (n, slug, passage, title, movement, part, `built: false`) from the literary unit map — `port` will overwrite it in full later. Also found `corpus/lexicon/HebrewStrong.xml` was never set up for this book (glosses all showed "?"); copied it from Joshua's `pipeline/corpus/lexicon/HebrewStrong.xml` (sha1-verified identical, same shared OpenScriptures lexicon). Generated and synced `canon-leads-unit-01.md`.


## 2026-09-27
- Closed the open "BHS check" item from `CLAUDE.md`'s Corpus section: checked the corpus's verse/section counts against BHS's own Masorah finalis (not just an English edition), via independent web sources. Traditional Masoretic count is 1,288 verses / 158 breaks (92 pe + 66 sam) — in Hebrew, not just English — versus this corpus's 1,289 verses / 159 breaks (94 pe + 65 sam). Documented in a new section of `numbers-versification-map.md` and a short addendum to `CLAUDE.md`'s Corpus section: not a corpus error, a known trait of digital OSHB/morphhb verse/section markup diverging slightly from a printed BHS's summary note; doesn't affect porting (English versification throughout).

## 2026-09-23
- Unit 1 source artifact failed `port 1 --dry` on `threads.candidates` format: ids written as `"6485 a"` (TSV lemma spelling; validator wants `"6485a"`), refs as `"Num 1:3"` / ranges (validator wants bare `"C:V"`), four candidates had no `ids`. Fixed in `source-artifacts/numbers_01_translation.html` (ids looked up in `Numbers-words.tsv`); dry port now validates.
- Style reference §2 `candidates[]` now spells out the id/ref formats (strip space from TSV lemma, bare `C:V`, no ranges, always give `ids`) so drafts get it right first time; re-synced.
- Recorded unit 1's six porter-question decisions in `translation-choices.md` (paqad = account/appoint, army, community + chieftain, Dwelling / Tent of Meeting capitalized, names transliterated); table.list approved. Added an 'Asking Lane' section to CLAUDE.md and a §3a note: questions go through the AskUserQuestion popup.
- Revised `source-artifacts/numbers_01_translation.html` to the answered decisions: paqad → 'take account of' / 'accounted-for' / 'appoint' (root slug `muster` → `account`, candidate and gloss updated), names transliterated (Latin letters only), `questions[]` cleared. `port 1 --dry` validates. Scheme recorded in `translation-choices.md`.
- Renamed unit 1 title/headings from 'muster' to 'accounting' (also unit map U01 and U29 titles). Ran `port 1` → `units/unit-01.html`, 28 in-verse occurrences. Validate failed on the approved table.list (no CSS class); added `table.list` rules to `css/styles.css`; `build` ok. Thread delta (`out/thread-delta-01.md`) not yet applied.
- Promoted six book-wide threads from unit 1 (account, army, community, called, wrath, charge) into `data/threads.json` / `data/roots.json`, colours from `biblecore colour`; listed as `threads.opens` in the unit-1 source (candidates cleared). Re-ported with `--force`: 22 spans got `data-w`; `build` ok. Audit still shows 23 gaps for account/army — all in vv22–43, which the approved table.list collapses (no English text to tag).
- Fixed bible-core's sync tooling (vendored into Numbers): sync-check now says 'NEEDS RE-SYNCING (run `python -m biblecore sync`)' instead of 're-paste', and `sync` now marks files synced after pushing, so sync-check goes quiet. `project-side/sync-state.json` is per-machine and gitignored (Numbers + template).
- Made `lanehaden157/numbers` public and enabled GitHub Pages (main, /): https://lanehaden157.github.io/numbers/
- Unit 1's count table: added Reuven row (so rows sum) and a `<tfoot>` Total (603,550, v46; sum verified); `app/main.js` no longer hoists `section.block` containing `table.list` to the top, so the table now sits between v21 and v44; CSS for thead/tbody/tfoot; style reference notes both.
- Audit gaps in condensed tables resolved (Lane: declare the verses). bible-core `d9d18b3` adds `data-verses` (audit reports occurrences there as covered; build fails if a declared verse is also written out or leaves the passage). Re-vendored core; unit 1's census table now carries `data-verses="1:22–43"` (source artifact + built unit, same one-attribute edit). Audit: 0 gaps, 23 covered (account 12, army 11). Style reference §4 documents it.

## 2026-09-24
- Re-vendored core `42ee2d3`: after promoting a thread, `python -m biblecore data-w N` fills the new spans in place (verified on a scratch copy: it reproduces unit 1's `--force` re-port byte for byte); validate, the port refusal and the thread delta now say so. Candidate ids written `"6485 a"` are normalized at port time. Style reference §2 and CLAUDE.md commands updated to match; CLAUDE.md state line was stale (said no units built).
- Re-vendored core `49db52a` (adds `units-from-map`). Not run on this book yet: it would add unbuilt rows for units 2–38 (groupings already match the map apart from names).
- Re-vendored core `7e4aa14` (table.list check; unit 1's table passes) and `7d6bcbe` (E1 versification): corpus reads now convert Hebrew → English numbering through morphhb's VerseMap, so units 17, 28, 31, 32 (and 29's `26:1b`) select the right verses for leads/audit/data-w. `corpus` regenerated: word table/reading unchanged, new `numbers-versification.md` (46 verses, same as the hand-built map), added to sync globs. Build ok, audit 0 gaps.
- Ran `units-from-map`: unit rows 2–38 added to `data/units.json` (unit 1 and groupings untouched); site's book map shows them as not yet built (browser-checked). Canon leads for unit 2 generated.
- Re-vendored core `c206d27` (G9 canon registries). Build writes `data/canon.json`: 14 echo edges from unit 1's asides and root echoes. Style reference §3 documents the optional `intertext[]` / `typescenes[]` meta keys; chat-side instructions gain a seventh standing move. Leads headers now note English numbering.

## 2026-09-26
- `CHAT_SIDE_INSTRUCTIONS.md`: trimmed repeats of core-workflow (closing "field wins" paragraph, blind-to-theme note, two restated clauses); lens notes revisited against unit 1: generational bullet now cites the census vocabulary resurfacing in judgment (paqad 14:18/29, "summoned" 16:2/26:9), priestly bullet adds the Levite cordon (1:51–53, qetsef). Needs re-paste into the project instruction field.
- Unit 2 ported ("The Camp around the Tent"). Seven porter questions answered by popup: degel → **company** (unit 1's 1:52 and root slug changed too), ʾotot → **signs**, camp, set out, facing at a distance, Reuel as written, soft pe → **ph** (Ephrayim, Naphtali, Yoseph, Elyasaph; unit 1 retrofitted, "Eliasaf" normalized). Recorded in `translation-choices.md`.
- Promoted camp, set-out, tribe-staff, chieftain (opens in unit 2; unit 1's 11 in-prose occurrences tagged in its source and re-ported with `--force`). Applied the `account` payoff at 2:33. Audit: 0 gaps across 10 threads; test 8/8.
- The colour tool handed set-out/tribe-staff/chieftain the palette's dark L≈25 tail (dull grey in dark mode). Fixed in bible-core `2d8d35e`: `assign_hues` tries readable colours first (Lab L ≥ 30, chroma ≥ 20). Re-coloured: set-out #7a3f5c, tribe-staff #005847, chieftain #006494; unit 1's local `company` re-picked (#5a5a9c). Vendored core at `2a20fe4` (includes another session's ornament commit).
- Added `.claude/launch.json` (python http.server on 8765) for browser checks.

## 2026-09-27
- Unit 3 ported. Porter questions: zar → **stranger / strange fire** (root slug `outsider` → `stranger`; unit 1's 1:51 root, gloss and note changed too), toledot kept, peduyim/pidyom → **redemption price** (local root `ransom` → `redemption`; title now "…in place of the firstborn"), ʿal pi YHWH kept literal (Lane, after asking what it was), per skull matches 1:2, 6486 (pequddah) added to `account`. Recorded in `translation-choices.md`.
- Promoted stranger, near, holy, firstborn (colours from `biblecore colour`); redemption stays local. Applied the unit 3 account/charge/community payoffs.
- Unit 1 retro tags in source: "comes near" (near) at 1:51, "firstborn" (firstborn) at 1:20; re-ported with `--force`.
- Unit 3 fixes: tagged camp (3:38) and tribe-staff (3:6); stripped tracked-thread spans from the 3:21–37 table, since core can't give table words a data-w (same as unit 1's table); soft pe → ph (Elyasaph, Elitsaphan, Tselophchad).
- Build ok, audit 0 gaps / 0 missing data-w across 14 threads, test 8/8, browser-checked in dark mode.
- bible-core `80642f8` (core 0.9.1): tracked-thread spans inside a `data-verses` component need no `data-w` (summary tags; a data-w given there is still audited). Checklist 7 and the audit's missing-data-w skip them; list/itin snippets, template style reference and ARCHITECTURE updated; core tests 233/233. Vendored into Numbers from a clean worktree (another session had uncommitted core.css); `book.json` core → 0.9.1. Unit 3's table colour spans restored and re-ported.

## 2026-09-28
- Unit 4 ported ("The Kehat load and the Levite service" per units/unit-04.html). Porter questions all answered as drafted: tachash skin, the most holy things, even for the space of a swallow, set its poles, serve/service throughout; nagash stays out of near; basin textform left out (unverified). Add `6633` (li-tsvo) to `army` (4:23 tagged "enlist").
- Promoted carry, serve, touch, cover, blue (19 threads); colours assigned one at a time via `biblecore colour` (batch-calling it gives every root the same colour). Applied army/holy/charge/account payoffs at 4:3/4:15/4:27/4:32.
- "most holy things" split into two spans (qodesh, ha-qodashim) so data-w aligns. Nine retrofit `add` tags in `retrofit/retrofit-tags.json` for carry/serve in units 1 and 3 and the 4:23 verb. Audit 0 gaps, test 8/8.

## 2026-09-29
- Vendored bible-core 0.9.9 (`2219cb5`, `book.json` core 0.9.9): speed only (audit and leads indexes, caches, one git call for sync-check). Build 18.6s to about 4.5s; output identical. Build ok, test 8/8.
- Instruction-file review, each change approved by Lane (`../instructions_review_2026-09-29.md`, R8, R12, R18, R19, R21, R22, R25, R30): CLAUDE.md (concurrent-sessions paragraph now a pointer to core CLAUDE.md, policy paragraph points to style reference §3 with colours as a default, Corpus section cut to pin + counts + pointer; chapter list fixed: 16, 17, 25, 29, 30 not 26). Style reference: §8 is now a real abridged unit 1 example (`biblecore test` example check ok), type-scene bullet dropped from the genre cautions (kept in the chat-side field), §5 ✎ dropped. CHAT_SIDE_INSTRUCTIONS: one precedence sentence (needs a re-paste). project-side README: sync pushes on its own, run when Lane OKs. Numbers `biblecore test --quick` 8/8. Uncommitted; mirror not synced yet.

## 2026-09-29 (structural audit step 1)
- `.gitattributes` (`* text=auto eol=lf`, from the template; `b782b81`); working copy re-checked out LF. Vendored core 0.9.10 (`a38d235`; `b138613`): every core writer writes LF, plus core `b625d80`'s canon file wording. Build changes no files; test 8/8.
- `CHAT_SIDE_INSTRUCTIONS.md` trimmed 595 -> 415 words (`c409ae4`): cut the canon-leads framing core-workflow.md already gives, process notes, the ANE bullet, the priestly example list. Needs a re-paste.

## 2026-09-29 (structural audit step 2)
- Vendored core 0.10.0 (`561e618`; `57d69a2`): `book.json` `sync` -> `{"extra": [], "skip": []}` (core supplies the defaults; resolved list unchanged, 17 files). CLAUDE.md State line -> `python -m biblecore book`; commands cut to the everyday six. project-side README: extras/skips, pruning. Build changed only version stamps; test 8/8. Synced `331e4bc` (index row order).

## 2026-09-29 (structural audit step 3)
- Vendored core 0.11.0 (`59068a9`; `a1a555c`): the app shell is written by `assets` from `biblecore/web/`, content-hash `?v=` replaces the hand-bumped `?v=N`. Shell diff only ?v values + generated-file comments. CLAUDE.md "Site" section. Test 8/8.

## 2026-09-30 (structural audit step 4)
- Core 0.11.1 (`4cde316`) by `tools/core_sync.py --all` (`5edadbf`, 13 files). book.json `template: ecd5bf6` (`060a09f`), read by `core_diff.py --template`. Test 8/8.
