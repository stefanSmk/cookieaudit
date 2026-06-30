# CookieAudit

Scanner **cookies et trackers** self-hosted pour contrôles RGPD/CNIL rapides.

Avant mise en prod : quels cookies à la première visite ? Google Analytics avant consentement ? Mention cookies dans la page ?

Outil heuristique — **pas** un audit juridique.

Complète [PrivaQuest](https://github.com/stefanSmk/privaquest) et [RopaDesk](https://github.com/stefanSmk/ropadesk).

## Installation

```bash
pip install -e .
```

## Utilisation

```bash
cookieaudit https://exemple.fr
cookieaudit https://exemple.fr --json
```

## Limites

- Pas d'exécution JavaScript
- Pas un conseil juridique

## Autres langues

- [English](./README.md)
- [Deutsch](./README.de.md)

## Licence

MIT
