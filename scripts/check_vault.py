#!/usr/bin/env python3
"""Check vault notes for problems that break publishing.

- invalid YAML frontmatter
- duplicate note basenames (ambiguous [[Wikilinks]])
- unresolved [[Wikilinks]] (target note missing)

Usage:  uv run --with pyyaml scripts/check_vault.py [--report 'Fehlende Einträge.md']
Exit code 1 if invalid YAML or duplicate basenames are found.
Unresolved links are only reported (stubs are expected).
"""
import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {'.obsidian', '.git', '.raw', 'copilot', 'templates', 'scripts', 'Fehlende Einträge.md'}
LINK_RE = re.compile(r'\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]')


def notes():
    for p in sorted(ROOT.rglob('*.md')):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in EXCLUDE:
            continue
        yield rel, p.read_text()


def split_frontmatter(text):
    if not text.startswith('---\n'):
        return None, text
    end = text.find('\n---', 4)
    return text[4:end], text[end + 4:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', help='write unresolved links as Markdown to this file')
    args = ap.parse_args()

    names = defaultdict(list)   # basename/alias -> [paths]
    invalid = []
    links = defaultdict(set)    # target -> {source paths}

    for rel, text in notes():
        names[rel.stem].append(rel)
        fm, _ = split_frontmatter(text)
        if fm is not None:
            try:
                meta = yaml.safe_load(fm) or {}
            except yaml.YAMLError as e:
                invalid.append((rel, str(e).splitlines()[0]))
                meta = {}
            aliases = meta.get('aliases') if isinstance(meta, dict) else None
            for a in aliases or []:
                if isinstance(a, str) and a != rel.stem:
                    names[a].append(rel)
        for target in LINK_RE.findall(text):
            links[target.strip()].add(rel)

    dupes = {n: ps for n, ps in names.items() if len({p for p in ps}) > 1}
    unresolved = {t: s for t, s in links.items() if t not in names and Path(t).name not in names}

    for rel, err in invalid:
        print(f'INVALID YAML  {rel}: {err}')
    for n, ps in sorted(dupes.items()):
        print(f'DUPLICATE     {n}: ' + ', '.join(map(str, ps)))
    print(f'\n{len(invalid)} invalid, {len(dupes)} duplicate, '
          f'{len(unresolved)} unresolved link targets ({len(links)} total)')

    if args.report:
        lines = ['# Fehlende Einträge', '',
                 'Automatisch erzeugt von `scripts/check_vault.py`. Verlinkte Namen ohne eigene Notiz, '
                 'sortiert nach Anzahl der verweisenden Notizen.', '']
        for t, srcs in sorted(unresolved.items(), key=lambda kv: (-len(kv[1]), kv[0].lower())):
            lines.append(f'- {t} ({len(srcs)})')
        Path(args.report).write_text('\n'.join(lines) + '\n')

    return 1 if invalid or dupes else 0


if __name__ == '__main__':
    sys.exit(main())
