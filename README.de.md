# CookieAudit

Self-hosted **Cookie- und Tracker-Scanner** für schnelle DSGVO/CNIL-Checks.

Vor Launch oder DPA: Welche Cookies fallen beim ersten Besuch? Lädt Google Analytics vor Consent? Steht überhaupt was zu Cookies auf der Seite?

Heuristisches CLI — **kein** Rechtsaudit. Findet offensichtliche rote Flaggen.

Ergänzt [PrivaQuest](https://github.com/stefanSmk/privaquest) und [RopaDesk](https://github.com/stefanSmk/ropadesk).

## Installation

```bash
pip install -e .
```

## Nutzung

```bash
cookieaudit https://beispiel.de
cookieaudit https://beispiel.de --json
```

## Grenzen

- Kein JavaScript-Rendering
- Kein Rechtsrat

## Weitere Sprachen

- [English](./README.md)
- [Français](./README.fr.md)

## Lizenz

MIT
