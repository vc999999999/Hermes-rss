#!/usr/bin/env python3
"""Install rss-reader skill for Claude Code, Codex, Hermes, and OpenClaw."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "rss-reader"

def env_home(name: str, fallback: str) -> Path:
    return Path(os.environ.get(name, Path.home() / fallback)).expanduser()


def target_paths() -> dict[str, Path]:
    return {
        "claude": env_home("CLAUDE_HOME", ".claude") / "skills" / SKILL_NAME,
        "claude-project": Path.cwd() / ".claude" / "skills" / SKILL_NAME,
        "codex": env_home("CODEX_HOME", ".codex") / "skills" / SKILL_NAME,
        "codex-project": Path.cwd() / ".codex" / "skills" / SKILL_NAME,
        "hermes": env_home("HERMES_HOME", ".hermes") / "skills" / SKILL_NAME,
        "openclaw": env_home("OPENCLAW_HOME", ".openclaw") / "skills" / SKILL_NAME,
    }

EXCLUDE_DIRS = {".git", "__pycache__"}
EXCLUDE_FILES = {"README.md", "preferences.yaml"}


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    return any(part in EXCLUDE_DIRS for part in rel.parts) or path.name in EXCLUDE_FILES


def copy_tree(dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)

    for src in ROOT.rglob("*"):
        if should_skip(src):
            continue

        rel = src.relative_to(ROOT)
        dst = dest / rel

        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    prefs = dest / "preferences.yaml"
    prefs_example = dest / "preferences.example.yaml"
    source_prefs = ROOT / "preferences.yaml"
    if source_prefs.exists() and (
        not prefs.exists() or "initialized: false" in prefs.read_text(encoding="utf-8")
    ):
        shutil.copy2(source_prefs, prefs)
    elif not prefs.exists() and prefs_example.exists():
        shutil.copy2(prefs_example, prefs)


def parse_targets(value: str) -> list[str]:
    targets = target_paths()
    requested = [item.strip().lower() for item in value.split(",") if item.strip()]
    if requested == ["all"]:
        return ["claude", "codex", "hermes", "openclaw"]

    unknown = [item for item in requested if item not in targets]
    if unknown:
        names = ", ".join(sorted(targets))
        raise ValueError(f"Unknown target(s): {', '.join(unknown)}. Use one of: all, {names}")

    return requested


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--targets",
        default="all",
        help=(
            "Comma-separated targets: all, claude, claude-project, codex, "
            "codex-project, hermes, openclaw"
        ),
    )
    args = parser.parse_args()

    try:
        targets = parse_targets(args.targets)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2

    targets_map = target_paths()
    for target in targets:
        dest = targets_map[target]
        copy_tree(dest)
        print(f"installed {target}: {dest}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
