# Podcasterei / Podcasting DACH

> Ein LLM-gepflegtes Wiki für Podcasting-Wissen, Community-Kontext und Sendezentrum-/Podcasterei-Material.

Dieses Repository ist als Wissensbasis gedacht– es strebt am dem Muster eines **LLM Wiki** zu folgen:

Rohquellen bleiben nachvollziehbar erhalten, während ein LLM daraus eine strukturierte, verlinkte Markdown-Wiki-Schicht pflegt.  Ziel ist, Wissen über Podcasting, Veranstaltungen, Formate, Menschen, Tools, Begriffe und offene Fragen nicht jedes Mal neu aus verstreuten Quellen rekonstruieren zu müssen, sondern es Schritt für Schritt zu verdichten.

## Worum geht es?

Dieses Repository sammelt und organisiert Wissen rund um Podcasting und die Podcasterei-/Sendezentrum-Community. Es kann beispielsweise verwendet werden für:

- Veranstaltungswissen rund um Sendezentrum, Sendegate,Congress, SUBSCRIBE und verwandte Formate
- Personen, Projekte, Begriffe und wiederkehrende Themen
- Votrags-Mitschnitte, Shownotes, Session-Beschreibungen und Diskussionsmaterialien
- Podcasting-Werkzeuge, Workflows, Produktionsnotizen und Distribution
- Fragen, Analysen und Synthesen, die später wieder auffindbar sein sollen

Das Wiki soll nicht nur Material ablegen, sondern Zusammenhänge sichtbar machen: Welche Themen tauchen wiederholt auf? Welche Tools gehören zu welchen Workflows? Welche Fragen sind offen? Welche Aussagen wurden durch spätere Quellen ergänzt, relativiert oder überholt?

## Grundprinzip

Das Repository ist nach dem LLM-Wiki-Ansatz organisiert:

1. **Rohquellen bleiben Rohquellen.**
   Dateien in `raw/` werden nicht umgeschrieben. Sie sind die überprüfbare Ausgangslage.

2. **Das Wiki ist eine kuratierte Arbeitsschicht.**
   Dateien in `wiki/` werden vom LLM gepflegt: Zusammenfassungen, Begriffseiten, Personen-/Projektseiten, Themenübersichten, Vergleiche und Synthesen.

3. **Jede Änderung bleibt nachvollziehbar.**
   `log.md` dokumentiert Ingests, größere Umbauten, offene Fragen und Lint-Durchläufe.

4. **Das Wiki wächst durch Benutzung.**
   Gute Antworten, Vergleiche oder neue Einsichten sollen nicht im Chat verschwinden, sondern als Wiki-Seiten oder Ergänzungen abgelegt werden.

5. **Quellen vor Behauptungen.**
   Aussagen im Wiki sollen auf konkrete Rohquellen oder externe Referenzen zurückführbar sein.

## Vorgeschlagene Struktur

```text
.
├── AGENTS.md              # Arbeitsanweisung für LLM-Agenten
├── README.md              # Einstieg für Menschen
├── index.md               # Inhaltlicher Einstieg in das Wiki
├── log.md                 # Chronologisches Änderungs- und Ingest-Protokoll
├── raw/                   # Unveränderte Quellen
│   ├── articles/
│   ├── events/
│   ├── transcripts/
│   ├── notes/
│   └── assets/
└── wiki/                  # LLM-gepflegte Wissensschicht
    ├── overview.md
    ├── people/
    ├── projects/
    ├── events/
    ├── topics/
    ├── tools/
    ├── sources/
    └── questions/
```

Die Struktur ist bewusst einfach gehalten. Wenn das Wiki wächst, können weitere Unterordner entstehen, aber neue Kategorien sollten in `AGENTS.md` dokumentiert und in `index.md` auffindbar gemacht werden.

## Wichtige Dateien

### `AGENTS.md`

Arbeitsvertrag für LLM-Agenten. Diese Datei beschreibt:

- welche Ordner wofür gedacht sind
- wie neue Quellen verarbeitet werden
- welche Metadaten Wiki-Seiten enthalten sollen
- wie Links, Tags und Quellenangaben aussehen
- wann bestehende Seiten aktualisiert statt neue Seiten angelegt werden
- wie Widersprüche, Unsicherheiten und offene Fragen markiert werden

### `index.md`

Der inhaltliche Einstiegspunkt. Der Index listet Wiki-Seiten mit kurzer Beschreibung, Kategorie und optionalen Metadaten. Vor jeder größeren Antwort sollte ein LLM zuerst den Index lesen.

### `log.md`

Append-only-Protokoll. Jede relevante Aktion erhält einen Eintrag, zum Beispiel:

```md
## [2026-05-13] ingest | 37C3-Session: Rückkanal bei der Podcasterei

- Quelle: `raw/events/37c3-rueckkanal-fediverse.md`
- Erstellt: `wiki/events/37c3-rueckkanal-fediverse.md`
- Aktualisiert: `wiki/topics/fediverse.md`, `wiki/topics/community-rueckkanal.md`
- Offene Fragen: Welche späteren Diskussionen griffen das Thema erneut auf?
```

## Workflow: Quelle aufnehmen

1. Lege die Quelle in `raw/` ab.
   Beispiele: Markdown-Export, Transkript, PDF, Linkliste, Notizen, Audio-Metadaten.

2. Bitte einen LLM-Agenten, die Quelle zu ingestieren.
   Beispiel:

   ```text
   Ingest `raw/events/37c3-rueckkanal-fediverse.md` in das Wiki.
   Aktualisiere passende Personen-, Themen-, Event- und Projektseiten.
   Ergänze `index.md` und `log.md`.
   Markiere Unsicherheiten und offene Fragen.
   ```

3. Prüfe die Änderungen.
   Achte besonders auf Quellenbezug, erfundene Details, falsch gesetzte Links und zu starke Zusammenfassungen.

4. Committe Rohquelle und Wiki-Änderungen gemeinsam.

## Workflow: Frage an das Wiki stellen

Beispiel:

```text
Beantworte aus dem Wiki: Welche wiederkehrenden Probleme bei Podcast-Distribution wurden bisher dokumentiert?
Lies zuerst `index.md`, dann relevante Seiten. Antworte mit Quellenhinweisen.
Wenn die Antwort eine dauerhafte Synthese enthält, schlage eine neue Seite unter `wiki/questions/` oder `wiki/topics/` vor.
```

Gute Antworten können anschließend zurück ins Wiki übernommen werden, etwa als:

- neue Themenseite
- Vergleichstabelle
- aktualisierte Übersicht
- offene Forschungsfrage
- Entscheidungsnotiz

## Workflow: Wiki pflegen

Regelmäßig sollte ein LLM-Agent einen Lint-Durchlauf machen:

```text
Lint das Wiki.
Suche nach verwaisten Seiten, fehlenden Rücklinks, widersprüchlichen Aussagen, unbelegten Behauptungen, veralteten Informationen und wichtigen Begriffen ohne eigene Seite.
Schlage konkrete Änderungen vor und aktualisiere `log.md`.
```

Typische Prüfungen:

- Gibt es Seiten ohne Eintrag in `index.md`?
- Gibt es Quellen in `raw/`, die noch keine Wiki-Seite haben?
- Sind zentrale Begriffe mehrfach, aber uneinheitlich beschrieben?
- Gibt es Aussagen ohne Quelle?
- Gibt es Widersprüche zwischen älteren und neueren Quellen?
- Fehlen Querverweise zwischen offensichtlich verwandten Seiten?

## Schreibkonventionen

Wiki-Seiten sollten möglichst diese Form haben:

```md
---
title: Beispielthema
type: topic
status: draft
sources:
  - raw/...
updated: 2026-05-13
---

# Beispielthema

## Kurzfassung

Ein bis drei Absätze, die den aktuellen Wissensstand zusammenfassen.

## Details

Strukturierte Darstellung mit Links auf verwandte Seiten.

## Quellen

- `raw/...`

## Offene Fragen

- ...

## Siehe auch

- [[Verwandtes Thema]]
```

Empfohlene Seitentypen:

- `source` – Zusammenfassung einer einzelnen Quelle
- `event` – Veranstaltung, Session, Workshop, Treffen
- `person` – Person mit belegten Rollen und Beiträgen
- `project` – Projekt, Podcast, Tool oder Initiative
- `topic` – Begriff, wiederkehrendes Thema oder Konzept
- `question` – ausgearbeitete Antwort auf eine wiederkehrende Frage
- `synthesis` – übergreifende Analyse mehrerer Quellen

## Umgang mit Unsicherheit

Ein LLM darf keine Details erfinden. Wenn etwas unklar ist:

- explizit als `Unklar`, `Nicht belegt` oder `Zu prüfen` markieren
- keine Rollen, Daten oder Zusammenhänge ergänzen, die nicht aus Quellen hervorgehen
- lieber eine offene Frage anlegen als eine plausible Behauptung formulieren
- bei widersprüchlichen Quellen beide Aussagen mit Herkunft dokumentieren

## Arbeiten mit Obsidian oder anderen Markdown-Editoren

Das Wiki ist normales Markdown und kann mit Obsidian, VS Code, Zettlr oder jedem anderen Editor genutzt werden. Obsidian ist besonders hilfreich für:

- Backlinks
- Graph View
- schnelle Navigation über `[[Wiki-Links]]`
- Dataview-Tabellen, falls YAML-Frontmatter konsequent gepflegt wird

## Git-Konventionen

Empfohlene Commit-Messages:

```text
ingest: add 37c3 fediverse discussion
wiki: update podcast distribution topic
lint: fix orphan pages and missing index entries
schema: clarify source page format
```

Rohquellen und daraus abgeleitete Wiki-Änderungen sollten möglichst im selben Commit landen, damit die Entstehung nachvollziehbar bleibt.

## Lizenz und Rechte

Bitte nur Material ablegen, das hier gespeichert werden darf. Bei externen Quellen reicht oft eine Notiz mit Link, Metadaten und eigener Zusammenfassung statt einer vollständigen Kopie. Für Transkripte, Bilder, Audio und Folien müssen die jeweiligen Rechte beachtet werden.

Falls dieses Repository eine konkrete Lizenz hat, sollte sie hier ergänzt werden.

## Status

Dieses README beschreibt die beabsichtigte Arbeitsweise als LLM Wiki. Die konkrete Ordnerstruktur und die Agentenregeln sollten im Repository weiterentwickelt werden, sobald reale Quellen, Arbeitsroutinen und Review-Erfahrungen hinzukommen.
