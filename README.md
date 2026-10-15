# Cartes de visite Amya Group

Fiches contact façon iPhone, une par personne, accessibles par QR code (salon SIAL).

- Fiches : `https://avistar-info.github.io/amya-cartes/<prenom>/`
- Page équipe : `https://avistar-info.github.io/amya-cartes/`
- QR codes prêts à imprimer : dossier `qr/` (PNG haute définition + SVG), planche A4 dans `qr/planche.html`

## Modifier une info (ou ajouter le lien du site)

1. Modifier `contacts.json` (le lien du site est le champ `site`).
2. `pip install segno` puis `python3 build.py`
3. Commit + push : le site se met à jour en ~1 min. **Les QR codes imprimés ne changent pas.**
