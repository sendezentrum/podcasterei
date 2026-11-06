#!/usr/bin/env python3
"""Populate missing frontmatter url fields from the first source URL in 'Quellen / Hinweise'.

Behavior:
- Scans Markdown files recursively.
- Only processes files with YAML frontmatter delimited by --- blocks.
- If frontmatter has a non-empty 'url:' value, file is skipped.
- If frontmatter has empty 'url:' or no 'url:' field, the script searches the
  first '## Quellen' or '## Quellen / Hinweise' section in the body.
- The first HTTP(S) URL found in that section is used to set frontmatter 'url:'.

Safety:
- Dry-run by default (no file writes).
- Use --apply to write changes.
"""

from __future__ import annotations

import argparse
import fnmatch
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
QUELLEN_HEADER_RE = re.compile(
    r"(?im)^##\s*quellen(?:\s*/\s*hinweise)?\s*$"
)
NEXT_HEADER_RE = re.compile(r"(?im)^#{1,6}\s+.+$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\((https?://[^)\s]+)\)")
URL_RE = re.compile(r"https?://[^\s)\]>\"]+")
URL_LINE_RE = re.compile(r"(?m)^url:\s*(.*?)\s*$")

DEFAULT_EXCLUDES = [
    "templates/**",
    ".obsidian/**",
    "copilot/**",
]


@dataclass
class Result:
    path: Path
    action: str
    detail: str


def has_frontmatter(text: str) -> bool:
    return FRONTMATTER_RE.match(text) is not None


def split_frontmatter(text: str) -> tuple[str, str, str] | None:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    full = m.group(0)
    frontmatter_body = m.group(1)
    rest = text[m.end() :]
    return full, frontmatter_body, rest


def get_newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def extract_first_quellen_url(body: str) -> str | None:
    match = QUELLEN_HEADER_RE.search(body)
    if not match:
        return None

    section_start = match.end()
    remaining = body[section_start:]
    next_header = NEXT_HEADER_RE.search(remaining)
    section = remaining[: next_header.start()] if next_header else remaining

    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        # Prefer markdown link targets over raw text.
        md_link = MARKDOWN_LINK_RE.search(line)
        if md_link:
            return md_link.group(1).strip()

        url = URL_RE.search(line)
        if url:
            return url.group(0).strip()

    return None


def upsert_url_in_frontmatter(frontmatter_body: str, url: str, nl: str) -> tuple[str, str]:
    lines = frontmatter_body.splitlines()

    # Update existing empty url field.
    for i, line in enumerate(lines):
        if re.match(r"^url:\s*$", line):
            lines[i] = f"url: {url}"
            return nl.join(lines), "filled-empty-url"

    # Keep existing non-empty url untouched (caller should have skipped already).
    if URL_LINE_RE.search(frontmatter_body):
        return frontmatter_body, "unchanged-existing-url"

    # Insert new url field near top for readability.
    insert_at = None
    for i, line in enumerate(lines):
        if line.startswith("name:"):
            insert_at = i + 1
            break
    if insert_at is None:
        for i, line in enumerate(lines):
            if line.startswith("type:"):
                insert_at = i + 1
                break
    if insert_at is None:
        insert_at = 0

    lines.insert(insert_at, f"url: {url}")
    return nl.join(lines), "inserted-url"


def is_excluded(path: Path, root: Path, excludes: Iterable[str]) -> bool:
    rel = path.relative_to(root).as_posix()
    return any(fnmatch.fnmatch(rel, pattern) for pattern in excludes)


def process_file(path: Path, apply: bool) -> Result:
    original = path.read_text(encoding="utf-8")
    nl = get_newline(original)

    split = split_frontmatter(original)
    if not split:
        return Result(path, "skip", "no-frontmatter")

    full_frontmatter, frontmatter_body, body = split

    url_line = URL_LINE_RE.search(frontmatter_body)
    if url_line and url_line.group(1).strip():
        return Result(path, "skip", "url-exists")

    first_url = extract_first_quellen_url(body)
    if not first_url:
        return Result(path, "skip", "no-url-in-quellen")

    updated_frontmatter_body, mode = upsert_url_in_frontmatter(frontmatter_body, first_url, nl)
    if mode == "unchanged-existing-url":
        return Result(path, "skip", "url-exists")

    new_full_frontmatter = f"---{nl}{updated_frontmatter_body}{nl}---{nl}"
    updated = new_full_frontmatter + body

    if updated == original:
        return Result(path, "skip", "no-change")

    if apply:
        path.write_text(updated, encoding="utf-8")
        return Result(path, "updated", mode)

    return Result(path, "would-update", mode)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Add/fill missing frontmatter url from first URL in 'Quellen / Hinweise' section."
        )
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory to scan (default: current directory).",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes to files. Without this flag, runs in dry-run mode.",
    )
    parser.add_argument(
        "--include",
        default="**/*.md",
        help="Glob pattern for files to include (default: **/*.md).",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Glob pattern to exclude (can be passed multiple times).",
    )

    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        print(f"Root does not exist or is not a directory: {root}")
        return 2

    excludes = list(DEFAULT_EXCLUDES)
    excludes.extend(args.exclude)

    files = sorted(root.glob(args.include))
    results: list[Result] = []

    for path in files:
        if not path.is_file():
            continue
        if is_excluded(path, root, excludes):
            continue
        if path.name == "AGENTS.md":
            continue
        results.append(process_file(path, apply=args.apply))

    updated = [r for r in results if r.action == "updated"]
    would_update = [r for r in results if r.action == "would-update"]
    skipped = [r for r in results if r.action == "skip"]

    mode_label = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{mode_label}] scanned: {len(results)}")
    print(f"[{mode_label}] updated: {len(updated)}")
    print(f"[{mode_label}] would-update: {len(would_update)}")
    print(f"[{mode_label}] skipped: {len(skipped)}")

    for r in (updated if args.apply else would_update):
        rel = r.path.relative_to(root).as_posix()
        print(f" - {rel} ({r.detail})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
