# Numbers

How this repo behaves. The artifact contract lives in
`numbers_study_style_reference.md` and is authoritative over this file.

Built on **bible-core** (vendored in `biblecore/`, version in
`biblecore/CORE_VERSION`). The shared shape and the ways a book is expected to
differ are in `bible-core/ARCHITECTURE.md`; shared wording defaults in
`bible-core/canon/conventions.md`. The chat-side loop is `core-workflow.md`
(vendored, synced); `CHAT_SIDE_INSTRUCTIONS.md` is pasted by hand into the
project's instruction field and only carries what's Numbers-specific.

**State:** unit 1 built (of 38); six tracked threads.

## Commands (run from this folder)

    python -m biblecore build            # everything downstream of units/*.html
    python -m biblecore port 5 [--dry]   # port source-artifacts/numbers_05_translation.html
    python -m biblecore port 5 --force   # re-port a built unit (source must be current)
    python -m biblecore audit            # tracked-thread coverage (--ids ROOT to preview an id set)
    python -m biblecore colour ROOT      # colour for a thread about to be promoted
    python -m biblecore data-w 5         # after promoting: fill the new thread's spans in place
    python -m biblecore leads            # canon-leads for built units + the next one
    python -m biblecore corpus           # rebuild the word table from morphhb (npm ci first)
    python -m biblecore sync             # push chat-side files to the synced mirror
    python -m biblecore sync-check --mark-pasted   # after pasting CHAT_SIDE_INSTRUCTIONS.md into the project
    python -m biblecore test [--quick]   # check the book: pin, units, contracts, build idempotence
    python -m biblecore migrate [--dry]  # after re-vendoring: move built units to the new contract
    python -m biblecore book             # show resolved settings

`book.json` holds everything book-specific (closed keys: an unknown key is an
error). Change behaviour for this book by adding a book-local module that
wraps a core function, not by editing `biblecore/`; `python ../bible-core/tools/core_diff.py`
reports edits made there. Update the vendored copy with
`python ../bible-core/tools/core_sync.py .`.

## Policy files

`data/threads.json` and `data/roots.json` are policy: the porter proposes, a
human applies. Thread colours come from `python -m biblecore colour`, never
picked by eye. Claude decides whether a candidate becomes a tracked thread,
biased toward book-wide, and asks Lane only when genuinely unsure.

## Asking Lane

Questions for Lane (the porter's `questions[]`, wording calls, thread
decisions) go through the **AskUserQuestion popup** with multiple-choice
options, best provisional choice first and marked "(Recommended)" — not as a
list in chat. The tool takes 4 questions per call, so batch a longer list
across calls. Lane wants this every time.

## Corpus

**morphhb 2.0.2** — `package.json`/lock, npm-installed 2026-09-22. Its
`node_modules/morphhb/wlc/Num.xml` is byte-identical (sha1
`44eebbb1dd93dd680b2427ecb9804f0a750764bc`) to Joshua's pinned copy of the
same file, so this is the same corpus release Joshua verified.

`python -m biblecore corpus` (2026-09-22): **1,289 verses, 16,422 words,
94 petuḥah + 65 setumah = 159 breaks.** English editions commonly cite 1,288
verses — **resolved** (2026-09-22) in `numbers-versification-map.md`: five
chapters (16, 17, 25, 26, 29, 30) diverge, and the net difference is a
genuine one-verse merge (Hebrew 25:19 folds into English 26:1), checked
against the raw corpus XML and a live ESV read, not from memory. If a count
drifts on re-fetch, flag it loudly; it likely means the corpus changed, not
that the earlier count was wrong.

`Numbers-reading.txt`, `Numbers-words.tsv`, `candidate-boundaries.md` are
generated (`python -m biblecore corpus`) — don't hand-edit. They keep Hebrew
numbering. Core converts to English numbering whenever it reads them
(`book.json` `versification`, default `kjv`), and `corpus` also writes
`numbers-versification.md`, the generated table of the 46 renumbered
verses. It matches `numbers-versification-map.md`, which stays as the
explained version.
`candidate-boundaries.md` is the raw machine list (Leningrad/OSHB markers
only, in document order, no interpretation). `numbers-literary-unit-map.md`
is the authored counterpart: it adds the Aleppo Codex witness and narrative
judgment on top of that raw list to reach the 38 units and 9 movements. The
two aren't redundant — the map is built from the list, not a replacement
for it — so both stay.

## Session files

`session_index.md` (read first), `improvements_log.md`, and a
`session_summary_<date>.md` per session.
