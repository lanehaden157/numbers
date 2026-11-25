# Numbers: Resources

How to weigh each source. Read them through `python tools/kit.py` (`kit.py sources` lists what is indexed). Page markers: `[p. N]` printed page (cite it), `[pdf p. N]` PDF page. Private copies: paraphrase, never quote at length. Start, not limit: search the web for voices missing here. Conversion details: `work/sources-local-notes.md`, `work/sources-web-notes.md`.

## Read whole per unit (`kit.py parts N`)

- **Levine**, Numbers 1-20 (AB 4A, 1993) and 21-36 (AB 4B, 2000): `levine-1`, `levine-2`. Baseline. Translation, notes by verse, long COMMENT essays; philology, textual variants (LXX, Samaritan), ANE background (census and itinerary in chs 1-4 and 20; Moabite Stele for ch. 21; Balaam). Hebrew numbering. OCR: digit/O/I swaps, glued verse numbers, a few Hebrew lines turned to symbols; vol 2 is weaker (chs 22, 33, 35 worst); the Balaam comments (22:2-24:25) are one 68 KB essay. His source-critical calls are the field's, not verdicts.
- **Whitt**, Numbers: a new translation with commentary (2022): `whitt`. English chapters only (no verse numbers); notes are indexed by whole chapter with the approximate verse range in the title. Follows Masoretic paragraphs: `**` = petuhah near here, em-dash line = setumah; Aleppo vs Leningrad can drift by 1-2 paragraphs. Check it first when a boundary is in question; composition-history angle beside Levine.
- **Doty**, Numbers (College Press, 1973): `doty`. KJV text, paraphrase, commentary, study questions; conservative teaching commentary, strong on NT links and typology. English numbering. OCR: spaced digits, "w." for "vv.".

## By key verses (`kit.py keyverses N`, then `kit.py extra N`)

- **Constable**, Notes on Numbers (2015 ed.): `constable`. Evangelical survey; good outline and NT links, thin on Hebrew; his citations of other scholars are leads, not his research. English numbering.
- **Morales**, Exodus Old and New (2020): `morales-exodus`. Biblical theology, not commentary; almost all `intro`. Use `kit.py grep` for Num 6:22-27, 3:7-8, 9:1-14, 11:16-17, 25, 12:6-8, 14:17-19, 16:3, 20:3, 11.
- **Rashi** (`rashi`), **Ramban** (`ramban`; strongest on chs 13-14, 21, 24; none on ch 30), **Ibn Ezra** (`ibn-ezra`), **Sforno** (`sforno`; gaps at 4:49, 18:5, 21:15-16, 22:34, 24:18-21, 24:23, 26:55, 31:17; ch 29 none), **Rashbam** (`rashbam`; stops after ch 25), **Or HaChaim** (`or-hachaim`), **Rabbeinu Bahya** (`rabbeinu-bahya`; no comment on 13:30-33; his proem sits on 1:1). Hebrew numbering; section titles keep the Hebrew ref, e.g. "Ibn Ezra on 17:2 [16:37]". A missing comment is no comment, not a gap. Munk volumes keep Hebrew-script lemmas in the text. Plain sense and midrash (Rashi), grammar (Ibn Ezra), theology and typology (Ramban), purpose (Sforno).

## Searched on demand (`kit.py grep N term`)

- **Keil & Delitzsch** (`keil-delitzsch`): best of the old set; sections run to the next biblehub anchor, so read ranges as stretches (chs 13-14 are one block). **Ellicott** (`ellicott`; short textual notes). **Pulpit** (`pulpit`; exposition only). **Henry** (`henry`; devotional; chs 13-14 chapter-level only). English numbering.
- **JPS** (`jps`): a second English, Hebrew numbering, notes as [note ...]; copyrighted, a phrase at most. **Tyndale** tagged Hebrew (`tyndale`; English numbering, rough transliteration: glosses only; use `kit.py words`).

## Texts

`kit.py words <range>`: each verse's English (WEB), words (transliteration, Strong's, gloss, parsing) and Brenton's LXX English. `kit.py bible <CODE> <range> [--lxx]`: any book. `python -m biblecore lxx Numbers <C:V>`: LXX Greek lemmas. Brenton follows Hebrew numbers in Num 17 and 30 (`lxx_numbering: hebrew`).

## Not on hand

Milgrom (JPS Numbers; only a review is here), Wenham (Tyndale), Ashley (NICOT), Sailhamer, Origen's Numbers homilies (Scheck, copyrighted; no free text). Search the web when a unit turns on them; say what you read and that it is secondhand where it is.
