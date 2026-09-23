# Cross-unit threads — canonical digest

Generated from `data/threads.json` (version 1). 6 threads, 6 open.

**This is the source of truth for thread tagging.** In a unit's fragment, a root that appears in the `id` column below is a *tracked thread*: tag every occurrence `<span class="r" data-root="<id>" data-w="<word id>">…</span>` (the word id from `Numbers-words.tsv`) and list it under `threads.opens` / `threads.payoffs` in the unit-meta block, with a matching id set in `data/roots.json`. A root that is recurring but *not* here is unit-local — tag it with its own name (no `data-w` needed) and just declare it in the unit's own `roots`. To propose promoting a local root to a tracked thread, add it to `threads.candidates` with a one-line reason (the Strong's/lemma `ids` you've actually observed in `Numbers-words.tsv`, plus a few representative `refs`, if you have them). **Claude decides, biased toward book-wide**: a local root that later pays off is worse than a tracked one that doesn't, so promote on a real second sighting. Ask Lane only when genuinely unsure.

| id | root (data-root) | translit | gloss | opens | payoffs | status |
|---|---|---|---|---|---|---|
| `account` | `account` | paqad | take account of, attend to; call to account; appoint, put in charge | 1 (1:3) | — | open |
| `army` | `army` | tsavaʾ | army, fighting force; organized service | 1 (1:3) | — | open |
| `called` | `called` | qaraʾ | call, summon; the summoned ones | 1 (1:16) | — | open |
| `charge` | `charge` | mishmeret | charge, guard-duty, what one keeps watch over | 1 (1:53) | — | open |
| `community` | `community` | ʿedah | community, assembly gathered as one body | 1 (1:2) | — | open |
| `wrath` | `wrath` | qetsef | wrath, anger that breaks out | 1 (1:53) | — | open |

## Notes per thread

- **`account`**: paqad opens the book: the two censuses (1, 26) and the Levite counts (3–4) are built on it; later it turns to ‘call to account’ (14:18, 29).
- **`army`**: tsavaʾ, the fighting force Israel is accounted into; 4:3 reuses it for Levite service at the tent and 31 for the Midian campaign.
- **`called`**: ‘The summoned of the community’ opens here and returns for Korach’s company and in the second census’s note on Datan and Aviram (16:2; 26:9).
- **`charge`**: mishmeret, the Levites’ and priests’ ‘charge’ that structures chs. 3–4 and 18.
- **`community`**: ʿedah, Israel as one assembled body; it becomes the actor that complains, rebels and is judged (14:1–2, 16:3, 20:1–2).
- **`wrath`**: The Levite cordon keeps wrath off the community; the word returns when the cordon is breached (16:46; 18:5).
