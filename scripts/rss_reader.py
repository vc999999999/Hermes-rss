#!/usr/bin/env python3
"""RSS 聚合 skill - 抓取原始数据，由 Hermes Agent 的 AI 负责总结"""

import asyncio
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import aiohttp

SKILL_DIR = Path(__file__).parent.parent
CONFIG_PATH = SKILL_DIR / "references" / "config.yaml"
HISTORY_PATH = Path.home() / ".hermes" / "rss-history.json"

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml", "-q"])
    import yaml


# ── 配置加载 ──────────────────────────────────────────────

def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ── 去重历史 ──────────────────────────────────────────────

def load_history():
    if HISTORY_PATH.exists():
        with open(HISTORY_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"read_links": {}, "last_run": None}


def save_history(history):
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    cutoff = (datetime.now() - timedelta(days=7)).isoformat()
    history["read_links"] = {
        url: date for url, date in history["read_links"].items()
        if date > cutoff
    }
    history["last_run"] = datetime.now().isoformat()
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


# ── HTML 清理 ────────────────────────────────────────────

def strip_html(text: str) -> str:
    clean = re.sub(r"<[^>]+>", "", text)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


# ── RSS 解析 ─────────────────────────────────────────────

def parse_rss(xml_text: str) -> list[dict]:
    items = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return items

    ns = {"atom": "http://www.w3.org/2005/Atom"}

    # RSS 2.0
    for item in root.iter("item"):
        desc = strip_html(item.findtext("description") or "")
        items.append({
            "title": (item.findtext("title") or "").strip(),
            "link": (item.findtext("link") or "").strip(),
            "description": desc[:200],
            "pubDate": item.findtext("pubDate") or "",
        })

    # Atom
    if not items:
        for entry in root.iter(f"{{{ns['atom']}}}entry"):
            link_el = entry.find(f"{{{ns['atom']}}}link")
            link = link_el.get("href", "") if link_el is not None else ""
            desc = strip_html(entry.findtext(f"{{{ns['atom']}}}summary") or "")
            items.append({
                "title": (entry.findtext(f"{{{ns['atom']}}}title") or "").strip(),
                "link": link.strip(),
                "description": desc[:200],
                "pubDate": entry.findtext(f"{{{ns['atom']}}}updated") or "",
            })

    return items


# ── 网络抓取 ─────────────────────────────────────────────

async def fetch_one(session: aiohttp.ClientSession, url: str) -> Optional[str]:
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if resp.status == 200:
                return await resp.text()
    except Exception:
        pass
    return None


async def fetch_all(urls: list[str]) -> dict[str, Optional[str]]:
    async with aiohttp.ClientSession() as session:
        tasks = {url: asyncio.create_task(fetch_one(session, url)) for url in urls}
        results = {}
        for url, task in tasks.items():
            results[url] = await task
        return results


# ── 主流程 ───────────────────────────────────────────────

async def run():
    config = load_config()
    sources = config["sources"]
    max_items = config.get("max_items_per_source", 10)
    group_by = config.get("group_by", "category")

    urls = [s["url"] for s in sources]
    raw_results = await fetch_all(urls)

    history = load_history()
    read_links = history["read_links"]
    today = datetime.now().strftime("%Y-%m-%d")

    grouped: dict[str, list[dict]] = {}
    errors: list[str] = []
    total_count = 0

    for source in sources:
        url = source["url"]
        name = source["name"]
        category = source.get("category", "未分类")
        xml_text = raw_results.get(url)

        if xml_text is None:
            errors.append(f"[!] {name}: 抓取失败")
            continue

        items = parse_rss(xml_text)
        new_items = []
        for item in items[:max_items]:
            link = item["link"]
            if link and link not in read_links:
                item["_source"] = name
                new_items.append(item)
                read_links[link] = today

        if not new_items:
            continue

        total_count += len(new_items)
        group_key = category if group_by == "category" else (name if group_by == "source" else "all")
        grouped.setdefault(group_key, []).extend(new_items)

    history["read_links"] = read_links
    save_history(history)

    # ── 输出原始数据，交给 Hermes AI 处理 ──────────────
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    print(f"[RSS Daily Brief — {date_str} {time_str}]")
    print(f"共 {total_count} 条新内容 | 来自 {len(sources)} 个源")
    print()

    if not grouped:
        print("（暂无新内容）")
        return

    for category, items in grouped.items():
        print(f"## {category} ({len(items)} 条)")
        print()
        for item in items:
            print(f"- {item['title']}")
            print(f"  链接: {item['link']}")
            print(f"  简介: {item['description']}")
            print()

    if errors:
        print("## 错误")
        for e in errors:
            print(e)


if __name__ == "__main__":
    asyncio.run(run())
