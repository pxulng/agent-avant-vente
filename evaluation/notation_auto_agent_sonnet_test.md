# Agent (3 outils, 10 itérations max, prompt v3) — Sonnet 5.5 — jeu de test — mesures automatiques (3 nov. 2026)

Fichier : resultats_agent_sonnet_v3.json. Réflexion : adaptive, effort low (Sonnet 5.5 refuse thinkingMode = disabled ; Haiku tournait sans réflexion). Une seule passe notée. Statuts lus à la main contre cle_briefs_test.csv. Juge IA, sources et contrôle humain pas encore faits.

## Journal d'erreurs de lancement
- Essai 0 : « The model claude-sonnet-5-5 does not support disabling thinking » (réglage du workflow, rien de produit). Corrigé en adaptive / low.
- Passe notée : 30 briefs lancés, 27 JSON valides, 3 invalides (voir ci-dessous). Pas de relance : une passe par version et par modèle.

## JSON invalides : 3 sur 30 (seuil : 0 cible, 1 acceptable)
- T04 : l'agent a écrit un JSON complet puis ajouté un paragraphe de texte (« Une correction : l'offre recommandée est Équipe, pas Essentiel… »). Le JSON seul est lisible, mais il contenait lui-même l'erreur (offre_recommandee Essentiel pour 6 utilisateurs). Compté invalide.
- T05 : sortie vide, 0 appel d'outil.
- T19 : sortie vide après 3 appels d'outils.
Aucun réparé à la main.

## Mesures
| # | Mesure | Agent Sonnet | Référence 2 Sonnet | Agent Haiku v3 |
|---|---|---|---|---|
| 1 | Fonctions inventées (28) | 0 | 0 | 0 |
| 2 | Exactitude des statuts | 67/70 = 95,7 % sur les 27 fiches valides ; 67/79 = 84,8 % si les 3 fiches invalides comptent comme fausses | 72/79 = 91,1 % | 65/79 = 82,3 % |
| 3 | Absence de doc signalée | 4/6 par le statut ; 6/6 sur le fond (T13 : éligibilité Entreprise à 15 utilisateurs à confirmer ; T16 : minimum 3 utilisateurs à confirmer) | 4/6 (6/6 sur le fond) | 4/6 (6/6) |
| 4 | Briefs vagues (T27–T30) | 4/4 | 4/4 | 4/4 |
| 5 | Calculs et seuils | 7/7 | 7/7 | 7/7 |
| 9 | JSON invalide | 3/30 | 0 | 0 |
| 10 | Appels d'outils / brief | moyenne 3,9 ; max 7 ; 0 à la limite | n/a | 4,2 (max 8) |

## Les 3 statuts faux (sur 70 besoins des fiches valides)
T15 F46 (partiel → non_couvert), T17 F69 (partiel → non_couvert), T18 F77 (partiel → non_couvert). Les mêmes trois besoins sont faux pour l'agent Haiku : ils tiennent peut-être à la clé (« partiel » pour une fonction absente en version utile), à discuter dans l'étude. Plus aucun couvert → partiel.

## Coût mesuré au solde
Agent Sonnet (une passe) : 4,50 → 3,12 = 1,38. Référence 2 Sonnet : ≈ 1,41. Agent Haiku : ≈ 0,06 ; référence 2 Haiku : ≈ 0,09. L'agent Sonnet coûte à peu près autant que la référence 2 Sonnet et environ 23 fois l'agent Haiku.

## Juge IA (agent Sonnet, prompt v3) — juge_ia_agent_sonnet_v3_test.json
| Critère (1 à 4) | Agent Sonnet (27 fiches valides) | Agent Sonnet (30, invalides notées 1) | Référence 2 Sonnet (30) |
|---|---|---|---|
| Exactitude | 3,89 | 3,60 | 3,77 |
| Limites | 4,00 | 3,70 | 3,97 |
| Sources | 4,00 | 3,70 | 4,00 |
| Questions | 3,67 | 3,40 | 3,03 |
| Utilité | 3,85 | 3,57 | 3,93 |
Réserves : (1) le juge est Sonnet 5.5, qui note ici des fiches du même modèle : risque d'auto-préférence. (2) Le contrôle humain de la série 2 (agent Haiku) a montré que ce juge est trop indulgent sur l'exactitude (3,58 contre 3,00 pour l'humain sur les mêmes fiches) ; les notes d'exactitude et de limites de l'agent Sonnet sont à lire avec la même réserve. (3) Les sources sont jugées sur leur cohérence avec la clé, pas passage par passage. (4) Le critère « questions » favorise l'agent (2 à 4 questions par brief clair) par rapport à la référence 2 (souvent 5 ou plus), selon la règle du juge, que l'humain trouve plutôt sévère.
