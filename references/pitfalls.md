# RSS Reader Pitfalls

Keep this file as a living library. Add a short entry whenever a failure repeats or a user correction reveals a better handling pattern.

## Empty Result After a Successful Run

Symptom: script prints `暂无新内容`.

Likely causes:

- All items were already seen in the last 7 days.
- Feeds returned valid XML but no fresh links.
- `max_items_per_source` is too low for a slow-moving source.

Preferred handling:

- Tell the user whether dedupe likely caused the empty result.
- Offer to remove `~/.cache/rss-reader/rss-history.json` for a full refresh if they want.

## Feed Fetch Failure

Symptom: source appears under `错误`.

Likely causes:

- RSS source is temporarily down.
- RSSHub or a proxy feed changed route.
- The source blocks the default HTTP client.

Preferred handling:

- Continue with other sources.
- Mention failed source names briefly.
- If the same source fails repeatedly, update `references/config.yaml` or add a note here.

## Atom Link Missing or Wrong

Symptom: Atom entries parse but links are empty, duplicated, or point to feed metadata.

Likely causes:

- Feed uses multiple `link` elements.
- The useful link is marked `rel="alternate"`.

Preferred handling:

- Prefer `rel="alternate"` links when adjusting the parser.
- Keep the parser deterministic in `scripts/rss_reader.py`.

## First-Round Menu Becomes a Long Report

Symptom: output contains long analysis, too many links, or a full newsletter before the user picks a topic.

Likely causes:

- The agent treated RSS raw data as a report request.
- `references/output-format.md` was not loaded.

Preferred handling:

- Return to a short menu first.
- Expand only after the user chooses an item, category, or comparison.

## Preference Mismatch

Symptom: user says important topics are missing or unwanted topics dominate.

Likely causes:

- `focus` and `avoid` are too broad.
- A feed category does not match the user's mental category.
- A major event was demoted because it matched `avoid`.

Preferred handling:

- Ask whether to update `preferences.yaml`.
- Keep major events in `重点` when they clearly matter, even if they touch an avoided category.

## Follow-Up Cannot Find Item Number

Symptom: user asks `展开 2`, but the current conversation lacks the first-round menu.

Likely causes:

- Context was compacted.
- Another workflow is calling the skill after the menu was generated.

Preferred handling:

- Load `~/.cache/rss-reader/latest.json`.
- Reconstruct the last menu or ask the user to identify the title/category if numbering is ambiguous.
