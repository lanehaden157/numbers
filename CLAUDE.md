# Numbers (v2)

38 units (map: 9 movements, 2 parts), 36 chapters, https://lanehaden157.github.io/numbers/ . All in Claude Code; Lane only answers calls (popups, recommended first, four each).

- `/unit N` or `/finish`; `fact-checker`, `builder` agents. Core's files (`biblecore/studio`); this file wins.
- Unit map `numbers-literary-unit-map.md` is authored and repo-owned; it drives `book.json` and `data/units.json`.
- Lens `lens.md`. Sources `resources.md`, read via `python tools/kit.py`. New source → `sources/marked/<key>.txt`, `python tools/split_sources.py`.
- Mistakes: `python tools/lessons.py known` before a unit; fact-checker and builder log kinds to it.
- Status `python tools/unit_status.py`. Other commands: `python -m biblecore`.
- Mirror: `python -m biblecore mirror` checks `data/mirror-exodus.json`; `keep|decline` settles a proposal.

## Strong suggestions

- English verse numbers differ from Hebrew in five chapters (`numbers-versification-map.md`): Eng 16:36-50 = Heb 17:1-15; Eng 17:1-13 = Heb 17:16-28; Eng 25 has 18 verses and Heb 25:19 folds into Eng 26:1; Eng 29:40 = Heb 30:1, Eng 30:1-16 = Heb 30:2-17. Everything else aligns. Levine, Sefaria voices, Rashi, JPS and LXX use Hebrew numbers; Doty, Constable, Tyndale, K&D family use English; Whitt has chapters only.
- Decided terms (`translation-choices.md`) in prose too.
- Promotions: book-wide bias, close call → Lane; `colour`; every occurrence needs `data-w`.
- After `port --dry`: check `opens` shape and `data-w` on split spans.

## Avoid

- Native Hebrew in chat or reader files: transliterate.
- Editing `biblecore/`, `.claude/`, core's `tools/*.py`, generated files (`Numbers-reading.txt`, `Numbers-words.tsv`, `candidate-boundaries.md`, `numbers-versification.md`). Look = `css/theme.css`.
- Inline Unicode in `bash -c`: use a `.py`. `git add -A`.

Corpus: morphhb 2.0.2 (`npm ci`), LXX (`biblecore fetch`). 1,289 verses (English editions 1,288), 16,422 words, 159 paragraph breaks (94 petuhah, 65 setumah); drift → flag.

`session_index.md` first.
