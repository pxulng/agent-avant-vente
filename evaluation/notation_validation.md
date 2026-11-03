# Jeu de validation (V01–V12) : notation automatique, une seule passe par méthode (3 nov. 2026)

Prompts, outils et réglages gelés (voir GEL_validation.md). Lancements faits par Claude via n8n, une fois chacun, aucune relance : exécutions 46 (agent Sonnet), 47 (réf. 2 Sonnet), 48 (réf. 2 Haiku), 49 (agent Haiku). 12 fiches JSON valides sur 12 pour les 4 passes, aucune limite d'itérations atteinte.

## Statuts de fonctionnalités (35 au total, clé cle_briefs_validation.csv)
| Brief | Att. | Agent Sonnet | Réf. 2 Sonnet | Agent Haiku | Réf. 2 Haiku |
|---|---|---|---|---|---|
| V01 (3) | couvert | 2 | 3 | 2 | 1 |
| V02 (4) | couvert | 4 | 4 | 2 | 2 |
| V03 (4) | couvert | 4 | 4 | 4 | 4 |
| V04 (4) | couvert | 4 | 4 | 3 | 4 |
| V05 (2) | partiel / non_couvert | 2 | 2 | 1 | 2 |
| V06 (2) | partiel | 2 | 2 | 0 | 2 |
| V07 (3) | partiel | 3 | 3 | 3 | 3 |
| V08 (4) | non_couvert | 4 | 4 | 4 | 4 |
| V09 (5) | non_couvert | 5 | 5 | 5 | 5 |
| V10 (4) | non_documente | 4 | 4 | 4 | 4 |
| **Total /35** | | **34 (97,1 %)** | **35 (100 %)** | **28 (80,0 %)** | **31 (88,6 %)** |

## Fonctions inventées (besoins non_couvert / non_documente présentés comme disponibles)
15 éléments attendus nc/nd (14 fonctionnalités + support client V12) : 0 fonction inventée pour les 4 méthodes. Les 4 non documentés de V10 sont bien non_documente partout, sans chiffre inventé (les 5/50/500 Go et 99,5 % cités par les références 2 sont de vrais chiffres de la doc, cités pour contexte).

## Erreurs de statut (sous-estimation ou sur-estimation)
- Agent Sonnet : V01 relance auto « non_documente » alors que DOC-07 la couvre (1).
- Agent Haiku : V01 relance « partiel » ; V02 Factur-X et mobile « partiel » ; V04 formation « partiel » ; V05 remise 15 % « couvert » (offre Équipe, mais sans limiter à une étape) ; V06 tarifs par client et Make « couvert » (partiel attendu, Équipe). 7 erreurs.
- Réf. 2 Haiku : V01 versions et relance « partiel » ; V02 Factur-X et mobile « partiel ». 4 erreurs.
- Réf. 2 Sonnet : aucune.

## Autres points
- Briefs vagues V11, V12 : les 4 méthodes posent des questions de clarification, ne recommandent aucune offre ni aucun prix (2/2).
- Erreurs graves à surveiller : aucune méthode ne recommande Essentiel pour V06 ; aucune n'affirme le circuit à 3 niveaux possible (V05) ; V07 : toutes passent à Entreprise (70 > 50).
- Calculs : V01 351 €, V03 624 €, V04 429 €, V06 312 € justes partout où ils sont donnés. Agent Sonnet V06 : « 150 devis » marqué couvert (la limite de 100 n'existe qu'en Essentiel), mais Équipe recommandée, donc le prix reste juste.
- Coût : solde 3,12 avant, 2,07 après les 4 passes, soit 1,05 au total (soldes mesurés globalement, pas par passe ; ordre de grandeur d’après le jeu de test : Sonnet ≈ 0,4 par passe, Haiku ≈ 0,03).

## Règle de décision (agent vs référence 2)
1. Moins de fonctions inventées : égalité (0 partout, Sonnet comme Haiku).
2. Statuts au moins aussi justes : la référence 2 gagne à chaque modèle (Sonnet 100 % contre 97,1 % ; Haiku 88,6 % contre 80,0 %).
Conclusion : confirmée sur le jeu de validation, l'agent n'apporte pas de gain à cette taille de documentation. Réserve : 12 briefs, 35 statuts, un écart d'une ou deux fiches. À lire comme une tendance, pas une preuve.
