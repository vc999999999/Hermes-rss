# Hermes-rss

[Hermes Agent](https://github.com/nousresearch/hermes-agent) 的 RSS 聚合 Skill，每天自动从配置的 AI、开源、论文、深度报道、开发工具 RSS 源收集资讯，由 Hermes Agent 的 AI 按用户偏好整理成手机友好的资讯菜单。

## 安装

```bash
# 克隆到 Hermes skills 目录
git clone https://github.com/vc999999999/Hermes-rss.git ~/.hermes/skills/rss-reader

# 安装依赖
pip install -r requirements.txt
```

## 使用

在 Hermes Agent 中触发：

```
/rss-reader
读RSS
今日资讯
RSS日报
```

## 偏好记录

第一次使用时，Agent 会先询问 3 个偏好问题，并写入 `preferences.yaml`。之后每次输出都会优先展示符合偏好的主题，不符合偏好的内容只保留带标签短标题。

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
| `references/config.yaml` | RSS 源配置 |
| `preferences.yaml` | 用户偏好记录 |

## 去重

已推送的内容在 7 天内不会重复出现，记录保存在 `~/.hermes/rss-history.json`。
