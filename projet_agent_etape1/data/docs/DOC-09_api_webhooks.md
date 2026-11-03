# [DOC-09] API et webhooks

## API
- API REST au format JSON, documentée publiquement (spécification OpenAPI).
- Authentification par clé d'API ou par OAuth 2.0.
- Objets disponibles : contacts, entreprises, opportunités, devis, factures, produits.
- Limites d'appels par jour : aucun accès (Essentiel), 1 000 (Équipe), 20 000 (Entreprise).
- Environnement de test (bac à sable) : offre Entreprise uniquement.

## Webhooks
- Offres Équipe et Entreprise.
- 20 types d'événements disponibles.

## Ce qui n'est pas inclus
- Pas de SDK officiel (bibliothèque prête à l'emploi).
- Pas d'API GraphQL.
- Pas d'accès direct à la base de données.

## Export des données
Un administrateur peut demander un export complet des données au format CSV.
