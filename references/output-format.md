# RSS Reader Output Formats

These are default shapes, not hard limits. Follow them when the user asks for the normal RSS menu. Adapt when the user explicitly asks for a report, links, export, or another workflow shape.

## First-Round Menu

```markdown
今天抓到 N 条，按你的偏好整理出 X 个重点。
偏好：偏好 A / 偏好 B
可回：展开编号 / 对比编号 / 改偏好 / 看被降权类别

## 重点

1. 主题名

判断：一句话判断这件事的核心变化。

值得看：
用 2 句解释背景和影响。
说明它为什么值得你点开。

关注点：
- 开发：……
- 产品：……
- 风险：……

来源：来源 A / 来源 B / 来源 C
可回：展开 1

## 其他扫过
- [产品] 短标题总结 1
- [工具] 短标题总结 2
- [安全] 短标题总结 3

## 被降权
- 社媒热帖：X 条
- 论文：X 条
- 纯融资：X 条

共 N 条 | 来自 N 个源 | 更新时间 HH:MM
```

Default menu guidance:

- Put preference-matching items in `重点`; keep it around `max_focus_topics`, default 5.
- Put valuable but weaker matches in `其他扫过`; keep it around `max_other_titles`, default 10.
- Use short labels such as `[模型]`, `[产品]`, `[Agent]`, `[工具]`, `[论文]`, `[公司]`, `[开源]`, `[安全]`, `[监管]`, `[行业]`.
- Keep first-round sources as source names, not URLs, unless the user asks for links.
- Keep a `被降权` section when avoid categories were found, showing category counts rather than titles.

## Single Expansion

```markdown
# 展开 X：主题名

## 简述
用 3-5 句讲清楚发生了什么。
先讲结论，再讲背景。

## 为什么重要
- 开发：……
- 产品：……
- 行业：……

## 关键信息
- ……
- ……
- ……

## 我的判断
用 3-5 句说趋势判断。
可以说明不确定性。

## 可继续深挖
- 技术细节
- 商业影响
- 相关产品
- 未来信号
- 原文链接

## 来源
- 来源 A：标题
  链接
- 来源 B：标题
  链接
```

Expansion guidance:

- Use the cached raw RSS result when possible.
- Include titles and links in `来源`.
- Avoid mixing unrelated topics unless the user asked for comparison or clustering.

## Comparison

```markdown
# 对比：主题 A vs 主题 B

## 一句话结论
用 1 句说明它们最关键的差异。

## 对比表
| 维度 | 主题 A | 主题 B |
|---|---|---|
| 核心变化 | …… | …… |
| 影响对象 | …… | …… |
| 短期价值 | …… | …… |
| 风险 | …… | …… |

## 你该优先看哪个
用 2-4 句给出建议。

## 可继续深挖
- 展开 A
- 展开 B
- 只看技术差异
- 只看商业影响
```

## Demoted Category

```markdown
# 被降权：类别名

- [标签] 短标题 1
- [标签] 短标题 2
- [标签] 短标题 3
```

Show short titles first. Add links or detail only if the user asks to expand a specific item.
