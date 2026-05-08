# Hermes-rss

[Hermes Agent](https://github.com/nousresearch/hermes-agent) 的 RSS 聚合 Skill，每天自动从 23 个 AI/科技/商业/论文 RSS 源收集资讯，由 Hermes Agent 的 AI 整理后输出结构化日报。

## 安装

```bash
# 克隆到 Hermes skills 目录
git clone https://github.com/vc999999999/Hermes-rss.git ~/.hermes/skills/rss-reader

# 安装依赖
pip install aiohttp pyyaml
```

## 使用

在 Hermes Agent 中触发：

```
/rss-reader
读RSS
今日资讯
RSS日报
```

## 输出格式

Agent 会按以下结构输出日报：

- **🔥 核心主题** — 相关新闻聚类，分析性叙述
- **🤖 LLM 动态** — 模型发布、工具平台、生态应用
- **💰 投融资快报** — AI 领域融资动态
- **🛠️ 开发者工具** — 新框架和工具发布
- **📰 行业深度** — 深度分析文章
- **📊 论文精选** — ArXiv 重要论文
- **💡 编者观察** — 当天趋势分析

## 自定义 RSS 源

编辑 `config.yaml` 添加或删除源：

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
| `rss_reader.py` | 抓取 + 去重脚本 |
| `config.yaml` | RSS 源配置 |

## 去重

已推送的内容在 7 天内不会重复出现，记录保存在 `~/.hermes/rss-history.json`。
