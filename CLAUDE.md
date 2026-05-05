# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

An **Obsidian vault** documenting the German-speaking (DACH) podcast ecosystem — its people, organizations, projects, networks, and events. Content is in German. There are no build, lint, or test commands.

Remote: `ssh://git@codeberg.org/sendezentrum/podcasterei.git`

## Directory structure

| Folder | Content |
|--------|---------|
| `01_event-series/` | Recurring podcast conferences and events |
| `02_networks/` | Podcast networks and communities |
| `03_orgs/` | Organizations (companies, platforms) |
| `04_projects/` | Tools and larger initiatives (Podlove, Ultraschall, etc.) |
| `05_shows/` | Individual podcasts |
| `10_people/` | Person profiles |
| `50_questionnaires/` | Survey and interview data |
| `99_community/` | Contribution guidelines and template examples |
| `templates/` | Obsidian Templater templates (one per entity type) |

## Frontmatter schema by type

All notes use YAML frontmatter. The `type` field determines the template:

- **person** (`templates/Personen_Vorlage.md`): `name`, `datum`, `contributes`, `orgs`, `podcasts`, `topics`, `source`, `checked`
- **Project** (`templates/Projekt_Vorlage.md`): `name`, `beteiligte`, `podcasts`, `events`, `topics`, `source`, `checked`
- **firma** (`templates/Firma_Vorlage.md`): `name`, `podcasts`, `projekte`, `labels`, `events`, `topics`, `source`, `checked`
- **event** (`templates/Event_Vorlage.md`): `name`, `datum`, `participants`, `orgs`, `podcasts`, `topics`, `source`, `checked`

`source` is typically `community`. `checked: false` until the entry has been reviewed.

## Content conventions (from `99_community/README_Checkliste.md`)

- Use `[[Wikilinks]]` for all connections between entities — one link per line in list fields
- Do **not** use Wikilinks for `topics` values (plain text only: `politik`, `tech`, etc.)
- Use official names
- Keep prose sections to **6–8 sentences total** per note; focus on relationships, not details
- No markdown formatting inside YAML values
- Each note has four sections: **Beschreibung**, **Verbindungen/Beteiligte**, **Bedeutung/Einordnung**, **Quellen / Hinweise**

## Obsidian plugins in use

`dataview`, `templater-obsidian`, `notebook-navigator`, `obsidian-icon-folder`, `calendar` — configuration lives in `.obsidian/`.

## Git commits

- Always add `Co-Authored-By: <model>` trailer to every commit message.
- Set author to the same ident when the model wrote the content. User is only committer, not author.
