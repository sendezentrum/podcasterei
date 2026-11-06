#!/usr/bin/env python3
"""Create a PodcastSeries markdown page from an RSS feed.

Usage:
  python3 scripts/create_podcast_series_from_rss.py http://sendungsbewusstsein.info/feed/

Behavior:
- Fetches the RSS feed and extracts the channel metadata.
- Asks whether the note should be created in a folder with the same name.
- Writes a PodcastSeries markdown file using the vault's current template style.
- Defaults to the `05_shows/` directory as the output root.

This script uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import re
import sys
import textwrap
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.error import URLError
from urllib.request import Request, urlopen

DEFAULT_OUTPUT_ROOT = Path("05_shows")
RSS_TIMEOUT_SECONDS = 20

ATOM_NS = "{http://www.w3.org/2005/Atom}"
ITUNES_NS = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"
DC_NS = "{http://purl.org/dc/elements/1.1/}"


@dataclass
class FeedInfo:
    title: str
    site_url: str
    feed_url: str
    authors: list[str]
    topics: list[str]
    description: str


def fetch_feed_xml(feed_url: str) -> bytes:
    request = Request(feed_url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=RSS_TIMEOUT_SECONDS) as response:
        return response.read()


def first_text(element: ET.Element, names: Iterable[str]) -> str:
    for name in names:
        found = element.find(name)
        if found is not None and found.text and found.text.strip():
            return found.text.strip()
    return ""


def collect_authors(channel: ET.Element) -> list[str]:
    authors: list[str] = []

    for candidate in [
        channel.findtext(f"{ITUNES_NS}author"),
        channel.findtext(f"{DC_NS}creator"),
        channel.findtext("author"),
        channel.findtext("managingEditor"),
    ]:
        if candidate:
            cleaned = candidate.strip()
            if cleaned and cleaned not in authors:
                authors.append(cleaned)

    owner_name = channel.findtext(f"{ITUNES_NS}owner/{ITUNES_NS}name")
    if owner_name:
        cleaned = owner_name.strip()
        if cleaned and cleaned not in authors:
            authors.append(cleaned)

    return authors


def collect_topics(channel: ET.Element) -> list[str]:
    topics: list[str] = []
    for category in channel.findall("category"):
        text = (category.text or "").strip()
        if text and text not in topics:
            topics.append(text)
        for sub in category.findall("category"):
            sub_text = (sub.text or "").strip()
            if sub_text and sub_text not in topics:
                topics.append(sub_text)
        label = category.attrib.get("text", "").strip()
        if label and label not in topics:
            topics.append(label)

    return topics


def collect_description(channel: ET.Element) -> str:
    for candidate in [
        channel.findtext(f"{ITUNES_NS}summary"),
        channel.findtext("description"),
        channel.findtext(f"{DC_NS}description"),
    ]:
        if candidate and candidate.strip():
            return re.sub(r"\s+", " ", candidate.strip())
    return ""


def parse_feed(feed_url: str) -> FeedInfo:
    try:
        raw = fetch_feed_xml(feed_url)
    except URLError as exc:
        raise SystemExit(f"Could not fetch RSS feed: {exc}") from exc

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise SystemExit(f"Invalid RSS/XML feed: {exc}") from exc

    channel = root.find("channel")
    if channel is None:
        channel = root

    title = first_text(channel, ["title", f"{ATOM_NS}title"])
    site_url = first_text(channel, ["link", f"{ATOM_NS}link"])
    description = collect_description(channel)
    authors = collect_authors(channel)
    topics = collect_topics(channel)

    if not title:
        raise SystemExit("The feed did not contain a channel title.")
    if not site_url:
        site_url = feed_url

    return FeedInfo(
        title=title,
        site_url=site_url,
        feed_url=feed_url,
        authors=authors,
        topics=topics,
        description=description,
    )


def normalize_name(name: str) -> str:
    name = name.strip()
    name = re.sub(r"[\\/:*?\"<>|]", "-", name)
    name = re.sub(r"\s+", " ", name)
    return name


def slugify(name: str) -> str:
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9äöüß]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-") or "podcast-series"


def prompt_yes_no(question: str) -> bool:
    while True:
        answer = input(f"{question} [y/N]: ").strip().lower()
        if answer in {"y", "yes", "j", "ja"}:
            return True
        if answer in {"", "n", "no", "nein"}:
            return False
        print("Please answer y or n.")


def build_markdown(info: FeedInfo) -> str:
    authors_block = "\n".join(f'  - "[[{author}]]"' for author in info.authors) if info.authors else "  - []"
    topics_block = "\n".join(f"  - {topic}" for topic in info.topics) if info.topics else "  -"
    description = info.description or "(Max. 2–3 Sätze: Worum geht es?)"

    lines = [
        "---",
        "type: PodcastSeries",
        f"name: {info.title}",
        f"url: {info.site_url}",
        f"feed_url: {info.feed_url}",
        "",
        "authors:",
        authors_block,
        "",
        "topics:",
        topics_block,
        "",
        "events:",
        "  -",
        "",
        "source: community",
        "checked: false",
        "---",
        "",
        "## Beschreibung",
        description,
        "",
        "## Verbindungen",
        "(Max. 2–3 Sätze: wichtigste Beziehungen erklären)",
        "- Hosts:",
        "- Organisationen:",
        "- Podcasts:",
        "- Kooperationen:",
        "- Netzwerk:",
        "",
        "## Einordnung",
        "(Max. 1–2 Sätze: Warum relevant für die Szene?)",
        "",
        "## Quellen / Hinweise",
        "- RSS: " + info.feed_url,
        "- Website: " + info.site_url,
    ]

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a PodcastSeries markdown page from an RSS feed."
    )
    parser.add_argument("feed_url", help="RSS feed URL, for example http://sendungsbewusstsein.info/feed/")
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="Root folder for show notes (default: 05_shows).",
    )
    parser.add_argument(
        "--same-folder",
        action="store_true",
        help="Create the note in a folder with the same name as the show.",
    )
    parser.add_argument(
        "--flat",
        action="store_true",
        help="Create the note directly in the output root without a folder.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite an existing markdown file.",
    )

    args = parser.parse_args()

    if args.same_folder and args.flat:
        print("Choose only one of --same-folder or --flat.")
        return 2

    feed_url = args.feed_url.strip()
    if not feed_url:
        print("Please provide a feed URL.")
        return 2

    info = parse_feed(feed_url)

    same_folder = args.same_folder
    if not args.flat and not args.same_folder:
        same_folder = prompt_yes_no(
            f"Create the note in a folder with the same name as '{info.title}'?"
        )

    output_root = Path(args.output_root).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    name = normalize_name(info.title)
    if same_folder:
        target_dir = output_root / name
        target_path = target_dir / f"{name}.md"
    else:
        target_dir = output_root
        target_path = target_dir / f"{name}.md"

    if target_path.exists() and not args.overwrite:
        print(f"Target already exists: {target_path}")
        return 1

    target_dir.mkdir(parents=True, exist_ok=True)
    target_path.write_text(build_markdown(info), encoding="utf-8")

    print(f"Created: {target_path}")
    if info.authors:
        print("Authors: " + ", ".join(info.authors))
    if info.topics:
        print("Topics: " + ", ".join(info.topics))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
