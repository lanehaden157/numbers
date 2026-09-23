# Numbers

How this repo behaves. The artifact contract lives in
`numbers_study_style_reference.md` and is authoritative over this file.

Built on **bible-core** (vendored in `biblecore/`, version in
`biblecore/CORE_VERSION`). The shared shape and the ways a book is expected to
differ are in `bible-core/ARCHITECTURE.md`; shared wording defaults in
`bible-core/canon/conventions.md`.

**State:** new book, no units built.

## Commands (run from this folder)

    python -m biblecore build            # everything downstream of units/*.html
    python -m biblecore port 5 [--dry]   # port source-artifacts/numbers_05_translation.html
    python -m biblecore port 5 --force   # re-port a built unit (source must be current)
    python -m biblecore audit            # tracked-thread coverage (--ids ROOT to preview an id set)
    python -m biblecore colour ROOT      # colour for a thread about to be promoted
    python -m biblecore leads            # canon-leads for built units + the next one
    python -m biblecore corpus           # rebuild the word table from morphhb (npm ci first)
    python -m biblecore sync             # push chat-side files to the synced mirror
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

## Corpus

**morphhb 2.0.2** — `package.json`/lock, npm-installed 2026-09-22. Its
`node_modules/morphhb/wlc/Num.xml` is byte-identical (sha1
`44eebbb1dd93dd680b2427ecb9804f0a750764bc`) to Joshua's pinned copy of the
same file, so this is the same corpus release Joshua verified.

`python -m biblecore corpus` (2026-09-22): **1,289 verses, 16,422 words,
94 petuḥah + 65 setumah = 159 breaks.** English editions commonly cite 1,288
verses for Numbers — the one-verse difference is expected from Hebrew/English
versification drift (chs. 16–17 and 29–30 are the usual places it happens in
Numbers) but has **not yet been checked against a printed BHS**, and no
per-chapter versification map exists yet. Do this — and build the
Hebrew↔English map from the corpus plus a real English versification source,
not from memory — before unit 1. If a count drifts on re-fetch, flag it
loudly; it likely means the corpus changed, not that the earlier count was
wrong.

`Numbers-reading.txt`, `Numbers-words.tsv`, `candidate-boundaries.md` are
generated (`python -m biblecore corpus`) — don't hand-edit.

## Session files

`session_index.md` (read first), `improvements_log.md`, and a
`session_summary_<date>.md` per session.
