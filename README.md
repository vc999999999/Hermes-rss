# RSS Reader Skill

适配 Claude Code、Codex、Hermes 和 OpenClaw 的 RSS 聚合 Skill。它会从配置的 AI、开源、论文、深度报道、开发工具 RSS 源收集资讯，由宿主 Agent 按用户偏好整理成手机友好的资讯菜单，并把原始结果沉淀到文件系统，方便后续展开、对比或交给其他工作流。

## 安装

```bash
# 克隆仓库
git clone https://github.com/vc999999999/Hermes-rss.git rss-reader
cd rss-reader

# 安装依赖
pip install -r requirements.txt

# 同步安装到 Claude Code、Codex、Hermes、OpenClaw
python3 scripts/install_skill.py --targets all
```

也可以只安装到某一个宿主：

```bash
python3 scripts/install_skill.py --targets claude
python3 scripts/install_skill.py --targets claude-project
python3 scripts/install_skill.py --targets codex
python3 scripts/install_skill.py --targets codex-project
python3 scripts/install_skill.py --targets hermes
python3 scripts/install_skill.py --targets openclaw
```

默认安装位置：

| 宿主 | 目录 |
|------|------|
| Claude Code | `~/.claude/skills/rss-reader` |
| Claude Code 项目级 | `./.claude/skills/rss-reader` |
| Codex | `~/.codex/skills/rss-reader` |
| Codex 项目级 | `./.codex/skills/rss-reader` |
| Hermes | `~/.hermes/skills/rss-reader` |
| OpenClaw | `~/.openclaw/skills/rss-reader` |

可通过 `CLAUDE_HOME`、`CODEX_HOME`、`HERMES_HOME`、`OPENCLAW_HOME` 或 `RSS_READER_SKILL_DIR` 覆盖默认路径。

## 使用

在 Hermes Agent 中触发：

```
/rss-reader
读RSS
今日资讯
RSS资讯
```

在 Claude Code 或 Codex 中可以使用 `$rss-reader`，或直接输入“读RSS / 今日资讯 / RSS资讯”。

## 偏好记录

第一次使用时，Agent 会先询问 3 个偏好问题，并写入本地 `preferences.yaml`。这个文件只保存个人偏好，不提交到 GitHub。之后每次输出都会优先展示符合偏好的主题，不符合偏好的内容只保留带标签短标题。

## 输出格式

Agent 会按以下结构输出资讯菜单：

- **重点** — 最多 5 个符合偏好的主题，每条包含判断、值得看、关注点和来源
- **其他扫过** — 最多 10 条不完全符合偏好但值得知道的带标签短标题
- **被降权** — 只显示类别和数量，不展开具体内容
- 用户回复“展开 1 / 深挖 2 / 对比 1 和 3”后，再进入深度解释

## 自定义 RSS 源

编辑 `references/config.yaml` 添加或删除源：

```yaml
sources:
  - name: 源名称
    url: https://example.com/rss
    category: 分类名
```

## 文件说明

| 文件 | 用途 |
|------|------|
| `SKILL.md` | Skill 定义，包含触发词和输出格式指令 |
| `scripts/rss_reader.py` | 抓取 + 去重脚本 |
| `scripts/install_skill.py` | 同步安装到 Claude Code / Codex / Hermes |
| `references/config.yaml` | RSS 源配置 |
| `references/output-format.md` | 默认菜单、展开、对比格式 |
| `references/workflow-contract.md` | 给其他 Agent 或工作流调用的输入/输出契约 |
| `references/pitfalls.md` | 持续沉淀的易错点库 |
| `preferences.example.yaml` | 用户偏好模板 |

## 去重

已推送的内容在 7 天内不会重复出现，记录默认保存在 `~/.cache/rss-reader/rss-history.json`。最近一次抓取的规范化结果保存在 `~/.cache/rss-reader/latest.json`，用于后续展开、对比和工作流编排。
