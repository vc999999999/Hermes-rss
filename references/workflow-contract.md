# RSS Reader Workflow Contract

Use this contract when another agent, command, or workflow calls `rss-reader` as one step in a larger process.

## Inputs

- `preferences.yaml`: user focus, avoid list, must-include topics, summary style, and item limits.
- `references/config.yaml`: RSS sources, categories, and per-source max items.
- Optional user request:
  - normal menu
  - expand item
  - compare items
  - show demoted category
  - change preferences
  - export or hand off to another workflow

## Deterministic Step

Run:

```bash
python3 "$SKILL_DIR/scripts/rss_reader.py"
```

The script fetches feeds, parses RSS/Atom, removes recently seen links, prints a readable raw feed, and writes `~/.cache/rss-reader/latest.json`.

## Normalized Output

The cached JSON contains:

```json
{
  "generated_at": "YYYY-MM-DDTHH:MM:SS",
  "total_count": 12,
  "source_count": 22,
  "grouped": {
    "AI": [
      {
        "title": "Item title",
        "link": "https://example.com",
        "description": "Short summary from feed",
        "pubDate": "Feed date",
        "source": "Source name",
        "category": "AI"
      }
    ]
  },
  "errors": []
}
```

## Agent Step

The host agent ranks and summarizes the normalized output. It should preserve item numbers in the first-round menu so later expansion can refer to the same cached evidence.

## Workflow Handoff

When handing off to another workflow, provide:

- cache path: `~/.cache/rss-reader/latest.json`
- selected item numbers or categories
- user preference summary
- requested next action, such as `expand`, `compare`, `research`, `draft`, or `monitor`

## Suggested Compositions

- `rss-reader -> research`: select one topic, then verify with web sources.
- `rss-reader -> writing`: select several items, then draft a newsletter or post.
- `rss-reader -> product-watch`: select product/tool items, then update a competitor or tool watch file.
- `rss-reader -> automation`: run daily, then output only items matching `must_include` or high-priority focus topics.
