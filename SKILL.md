---
name: rss-reader
description: Use when the user asks to read, fetch, summarize, filter, rank, compare, or expand RSS/news updates, especially AI, agent development, open source, papers, tools, and industry news. Trigger for /rss-reader, 读RSS, 今日资讯, RSS资讯, 今日AI新闻, 展开RSS条目, 对比资讯编号, 修改RSS偏好.
---

# RSS 资讯菜单

Use this skill to turn configured RSS feeds into a preference-aware, mobile-friendly Chinese news menu. Treat the filesystem as the working memory: configuration, preferences, run history, cached raw results, output templates, and known pitfalls all live beside the skill or under the user's cache directory.

## Resolve Skill Directory

Before reading or writing skill files, resolve the current skill directory. Prefer explicit environment variables, then common personal and project-level locations:

```bash
SKILL_DIR="${RSS_READER_SKILL_DIR:-}"
if [ -z "$SKILL_DIR" ]; then
  for dir in \
    "$PWD" \
    "$PWD/.claude/skills/rss-reader" \
    "$PWD/.codex/skills/rss-reader" \
    "${CLAUDE_HOME:-$HOME/.claude}/skills/rss-reader" \
    "${CODEX_HOME:-$HOME/.codex}/skills/rss-reader" \
    "${HERMES_HOME:-$HOME/.hermes}/skills/rss-reader" \
    "${OPENCLAW_HOME:-$HOME/.openclaw}/skills/rss-reader"; do
    if [ -f "$dir/SKILL.md" ] && [ -f "$dir/scripts/rss_reader.py" ]; then
      SKILL_DIR="$dir"
      break
    fi
  done
fi
```

If no directory is found, ask the user where the skill is installed or ask them to set `RSS_READER_SKILL_DIR`.

## Workflow

1. Check preferences in `preferences.yaml`. If missing, empty, or `initialized` is not `true`, ask the three short setup questions from `preferences.example.yaml` and write the answers locally.
2. Run `python3 "$SKILL_DIR/scripts/rss_reader.py"` to fetch RSS items. The script reads `references/config.yaml`, deduplicates recently seen links, and writes the latest raw result to the cache.
3. Summarize the raw result according to `preferences.yaml`. Use `references/output-format.md` as the default first-round menu and expansion format.
4. When the user asks to expand, compare, view a demoted category, change preferences, or use this result in another workflow, load only the relevant cached raw result and reference file.
5. After a recurring failure or useful correction, update `references/pitfalls.md` with the symptom, cause, and preferred handling.

## Filesystem Context

- `references/config.yaml`: RSS source list and grouping config.
- `preferences.yaml`: local personal preferences. Do not commit real user preferences.
- `preferences.example.yaml`: preference template and first-run defaults.
- `references/output-format.md`: default output shapes for menu, expansion, comparison, and demoted categories.
- `references/workflow-contract.md`: input/output contract for orchestration by other agents or workflows.
- `references/pitfalls.md`: living library of known mistakes and recovery patterns.
- `scripts/rss_reader.py`: deterministic fetch, parse, dedupe, and cache script.
- `~/.cache/rss-reader/rss-history.json`: dedupe history.
- `~/.cache/rss-reader/latest.json`: latest normalized raw result for follow-up expansion.

## Preference Setup

Ask only these three questions on first use:

```text
第一次使用，我先记一下你的资讯偏好。之后会按这个筛选。

1. 你最关心哪几类？
可选：AI产品工具 / Agent开发 / 模型论文 / 公司商业 / 监管社会 / 开源项目 / AI安全 / 行业应用

2. 你想少看或不看哪几类？
可选：论文 / 融资 / 社媒热帖 / 海外长文 / 开发工具 / 监管 / 纯产品发布

3. 推送希望多短？
可选：极短 / 标准 / 稍详细
```

Write the result as YAML:

```yaml
initialized: true
focus:
  - Agent开发
  - AI产品工具
avoid:
  - 社媒热帖
must_include: []
summary_style: detailed
max_focus_topics: 5
max_other_titles: 10
```

## Operating Guidance

- Provide useful defaults instead of rigidly enforcing a format. If the user asks for a different shape, adapt while keeping the same RSS evidence base.
- Teach only the workflow-specific parts: where files are, how data is fetched, how preferences are applied, and how follow-up expansion works.
- Keep first-round output as a menu unless the user explicitly asks for a report, deep analysis, links, or a workflow handoff.
- Use Chinese by default for user-facing output.
- Do not copy long RSS text verbatim. Summarize in your own words and include links only when expanding or when the user asks.
- If the feed result is empty, explain whether it is because of dedupe, fetch failures, or genuinely no parsed items. Use `references/pitfalls.md` for recovery.
