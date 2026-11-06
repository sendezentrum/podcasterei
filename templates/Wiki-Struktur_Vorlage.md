---
type: Meta
name: Wiki-Struktur-Vorlage
status: reference
---

# Wiki-Struktur-Vorlage

Generalisierte Struktur dieses Vaults, abstrahiert für Aufbau eines neuen, thematisch ähnlichen LLM-Wikis. `[DOMÄNE]` = neues Thema (z.B. "Musikszene", "Gaming-Community", etc.) statt "Podcasterei".

## Grundprinzip

Folgt Muster [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):

1. **Rohquellen bleiben Rohquellen** — `.raw/` unverändert, nicht umgeschrieben.
2. **Wiki = kuratierte Arbeitsschicht** — Markdown-Seiten vom LLM gepflegt (Personen, Orgs, Events, Themen, Synthesen).
3. **Jede Änderung nachvollziehbar** — Commits verknüpfen Rohquelle + Wiki-Änderung.
4. **Wiki wächst durch Benutzung** — gute Antworten werden zu Seiten, nicht im Chat verloren.
5. **Quellen vor Behauptungen** — jede Aussage auf Rohquelle/externe Referenz rückführbar.

## Root-Dateien

| Datei | Zweck |
|---|---|
| `README.md` | Einstieg für Menschen — Zweck, Struktur, Workflows |
| `AGENTS.md` | Arbeitsvertrag für LLM-Agenten — Ordner, Frontmatter-Schema, Konventionen |
| `TODO.md` | Offene Tasks |
| `.obsidian/` | Obsidian-Konfiguration (dataview, templater, etc.) |

## Ordnerstruktur

Nummern-Präfix steuert Sortierung/Priorität in Obsidian-Dateibaum, nicht Hierarchie:

```
.
├── 01_[haupt-format-serien]/    # wiederkehrende Formate/Reihen der Domäne
├── 02_[netzwerke]/              # Netzwerke/Communities innerhalb Domäne
├── 03_[organisationen]/         # Firmen, Institutionen, Plattformen
├── 04_[projekte]/               # Tools, Initiativen
├── 05_[kern-entität]/           # zentrale wiederkehrende Einheit der Domäne
├── 10_[personen]/                # Personenprofile
├── 50_[erhebungen]/             # Umfragen/Interviewdaten (optional)
├── .raw/                        # unveränderte Rohquellen (Transkripte, Artikel)
├── templates/                   # Templater-Vorlagen, eine pro Entitätstyp
└── scripts/                     # Hilfsskripte (z.B. RSS-Import)
```

Lücken in Nummerierung (06–09, 11–49) bewusst offen für spätere Kategorien.

## Entitätstypen (schema.org-basiert)

Frontmatter-Feld `type` bestimmt Template. Custom Subtypes erlaubt als Verfeinerung, nicht strikt schema.org:

| Typ | Bedeutung | Custom Subtypes (Beispiel) |
|---|---|---|
| `Person` | Mensch mit Rolle/Beitrag in Domäne | — |
| `Organization` | Firma, Institution | `[Domänenspezifisches Netzwerk]`, `[Domänenspezifisches Label]` |
| `Project` | Tool, Initiative | — |
| `EventSeries` | Wiederkehrende Veranstaltungsreihe | — |
| `Event` | Einzelveranstaltung | `Talk` (Vortrag mit Aufzeichnung) |
| `[Kern-Entität-Serie]` | z.B. `PodcastSeries` — zentrale wiederkehrende Sache der Domäne | `[Kern-Entität-Episode]` |
| `Topic` | Begriff/wiederkehrendes Thema | — |
| `Question` | Ausgearbeitete Antwort auf wiederkehrende Frage | — |
| `Synthesis` | Übergreifende Analyse mehrerer Quellen | — |

## Frontmatter-Schema (gemeinsame Felder)

Jeder Typ hat eigenes Template unter `templates/`, aber gemeinsame Basis:

```yaml
---
type: <Entitätstyp>
name:
url:
<typ-spezifische Relationsfelder>:  # z.B. orgs, podcasts, events, topics — je als Liste
  -
topics:
  -
source: community
checked: false   # NIE von Agent auf true setzen — nur menschliche Review
---
```

Relationsfelder (`orgs`, `[kern-entität]`, `events`, etc.) nutzen `[[Wikilinks]]`. `topics` bleibt Klartext, keine Wikilinks.

## Note-Struktur (Body)

Pro Seite exakt vier Abschnitte, Prosa max. 6–8 Sätze gesamt, keine `---` Trenner zwischen Abschnitten:

```md
# <Name>

## Beschreibung
(2–3 Sätze)

## Verbindungen/Beteiligte
(2–3 Sätze, [[Wikilinks]])

## Bedeutung/Einordnung
(1–2 Sätze)

## Quellen / Hinweise
- 
```

## Konventionen

- Offizielle Namen verwenden, Duplikate vor Neuanlage prüfen
- Kein Markdown-Formatting in YAML-Werten
- Unsicherheiten explizit markieren (`Unklar`, `Nicht belegt`, `Zu prüfen`) statt erfinden
- Commit-Präfixe: `ingest:`, `wiki:`, `lint:`, `schema:`
- Rohquelle + abgeleitete Wiki-Änderung im selben Commit

## Neues Wiki aufsetzen — Checkliste

1. Ordnerstruktur mit domänenspezifischen Namen anlegen (Nummern-Präfixe beibehalten)
2. `README.md` + `AGENTS.md` aus diesem Vault kopieren, domänenspezifisch anpassen
3. `templates/` — ein `*_Vorlage.md` pro Entitätstyp, Frontmatter-Schema oben als Basis
4. Entitätstypen-Tabelle auf Domäne zuschneiden (Kern-Entität ersetzen, z.B. `PodcastSeries` → `[Domänen-Kernentität]`)
5. `.raw/` + `.gitignore` einrichten
6. Erste 3–5 Seiten von Hand/Agent anlegen zum Kalibrieren von Prosalänge/Ton
