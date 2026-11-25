# Lens

## Reader

Lane, English. Little Hebrew: translit + gloss every Hebrew word, again at first use per unit. Never native script, any file. Grammar that matters (stem, aspect, a cognate accusative) → plain words.

## Look for, by weight

1. Intertext: what earlier Scripture stands behind a line (Exodus above all: the pairs in `data/mirror-exodus.json`; Genesis promises; Sinai and the tabernacle), where a line or word returns later (Deuteronomy's retelling, Joshua, the prophets, the NT: Heb 3-4, 1 Cor 10, John 3:14, Jude, 2 Pet, Rev 2:14), and what the echo does.
2. The book's own markers over imposed symmetry: the census bracket (chs 1 and 26; 26:64-65 looks back to ch. 1), dated notices, the "plains of Moab" formula, the *nasa'* ("set out") departure formulas, Masoretic breaks (`candidate-boundaries.md`).
3. The generational hinge. Part One is the exodus generation (1:1-25:18). The rebellions (U11, U13-14, U16, U20-22, U28) differ: read each on its own. U12 is not a people's rebellion; U21 (Hormah) undoes 14:45; U22 is the last complaint; U28 (Baal Peor) comes after the Zered crossing, so ask whether its sinners are the new generation. Census words resurface in judgment scenes (*paqad*, 14:18, 29).
4. Priestly and legal material is not filler: the same holiness-and-nearness logic makes the rebellions dangerous. Say why a block stands where it does.
5. Narrative shape: type-scenes, keywords, poetry (blessing, ark sayings, victory songs, Balaam's oracles) as poetry. Structure (chiasm, panels) only if real and checkable.
6. Read the unit's map entry (`numbers-literary-unit-map.md`) first: it names later reuse, NT reception and type-scenes worth a search.

## Do

- Levine = baseline (Anchor Bible 4A and 4B: philology, textual variants, ANE background), in dialogue with Whitt (Masoretic breaks, composition history), Doty (conservative teaching commentary), Constable, the medieval Jewish voices (Rashi, Ramban, Ibn Ezra, Sforno, Rashbam, Or HaChaim, Rabbeinu Bahya), Morales (exodus pattern), the older Christian commentaries (K&D, Ellicott, Pulpit, Henry) and the LXX. Say where they split and why. Weigh Rashi, Ibn Ezra and Ramban at the census numbers (chs 1-4, 26) and Balaam (22-24).
- Levine's source-critical calls (P, J/E) are a fact about the field, not a verdict: name what rests on them.
- Say what the verses do first, then what scholars infer, marked as inference. Thin but plausible → keep, tentative, say why. Drop only what the text won't bear.
- Later Jewish and Christian use of a passage is reception, not the meaning in Numbers: tell it as reception.
- Source status: "read" only for the sections actually opened this unit. Skimmed or unopened → say so.

## Don't

- Quote marks on wording not read this unit.
- Recall ids, rulings, renderings: copy from `work/NN/pack.md`.
- Attribute a view to a commentator before re-opening their own lines; say "rabbis he reports" when it is not his own. "Every / each / only / always": check all the cases, or say "most".
- Long quotes from Levine, Doty, Whitt, Morales, JPS: paraphrase.
- Mix numbering: Levine, Sefaria voices, Rashi, JPS and LXX use Hebrew verse numbers; Doty, Constable, Tyndale and the K&D family use English (`CLAUDE.md`).
- Trust Whitt's verse placement: his translation sections are chapter-level (edges can be off by half a chapter); `**` marks a petuhah near that spot, an em-dash line a setumah.
- Trust OCR digits and Hebrew lines in Levine (a glued number like "2~ereupon" hides a verse break): check against `kit.py words`.
- Open whole-book files in `sources/`: use `python tools/kit.py`.
