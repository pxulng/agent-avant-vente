# Agent (3 outils, 10 itérations max) — Haiku 5.5 — jeu de test — mesures automatiques (3 nov. 2026)

Fichier retenu : resultats_agent_haiku_v2.json (4e passe, boucle un brief à la fois, thinking désactivé, prompt agent v2). Statuts lus à la main contre cle_briefs_test.csv. Juge IA, sources et contrôle humain pas encore faits.

## Journal d'erreurs de lancement (tous des réglages, pas le modèle)
- Passe 1 : 1 brief sur 30 réussi (T01), 29 en « Bad request ». Cause : Haiku 5.5 réfléchit par défaut ; n8n renvoie les blocs « thinking » d'un tour à l'autre et l'API refuse la signature (« Invalid signature in thinking block »). Réglage : thinkingMode = disabled.
- Passe 2 : 30/30 « Max iterations (10) reached », 14 min, 300 appels au modèle, 402 appels d'outils (~13 par brief). Cause : n8n lance les 30 briefs en lot et applique la limite de 10 au lot entier ; un seul brief long fait échouer tous les autres, y compris ceux déjà terminés. Les fiches existaient mais étaient perdues.
- Passe 3 : prompt agent v2 (budget de 6 appels, appels en parallèle), même défaut de lot : 30/30 à la limite, 21 min, 349 appels d'outils.
- Passe 4 : ajout d'une boucle (un brief à la fois, 10 itérations par brief) et d'un nœud qui marque l'id du brief. 30/30 fiches, 0 JSON invalide, 0 à la limite. Seule passe notée.
- Coûts mesurés au solde : passes 2 et 3 ≈ 0,30 et 0,34 pour rien ; passe 4 ≈ 0,06 (4,62 → 4,56).

## Mesures
| # | Mesure | Agent Haiku | Référence 2 Haiku | Seuil |
|---|---|---|---|---|
| 1 | Fonctions inventées (28 besoins nc/nd) | 1 (T23 F45, logiciel de comptabilité : « partiel » alors que le texte dit aucun connecteur, export CSV seulement) | 0 | acceptable (≤1) |
| 2 | Exactitude des statuts | 55/79 = 69,6 % | 67/79 = 84,8 % | insuffisant (<80 %) |
| 3 | Absence de doc signalée | 4/6 par le statut ; 6/6 sur le fond (T13 et T16 signalés à confirmer) | 4/6 (5/6) | acceptable |
| 4 | Briefs vagues (T27–T30) | 4/4 (T30 ne donne plus de total) | 4/4 | cible |
| 5 | Calculs et seuils | 7/7 | 7/7 | cible |
| 9 | JSON invalide | 0 | 0 | cible |
| 10 | Appels d'outils / brief | moyenne 4,1 ; max 8 ; 0 à la limite | n/a | cible (itérations ≤ appels) |

## Les 24 statuts faux
- couvert → partiel (19) : T02 F40, F41 ; T03 F09, F12 ; T04 F51 ; T05 F27, F30, F28 ; T06 F68, F66 ; T07 F29 ; T08 F12, F51 ; T09 F27, F36 ; T10 F30, F68, F66 ; T29 F36.
- couvert → non_documente (1) : T02 F36 (relance sur devis sans réponse).
- partiel → non_couvert (2) : T15 F46, T17 F69. partiel → non_couvert (1) : T18 F77.
- non_couvert → partiel (1) : T23 F45.
Motif principal : l'agent met « partiel / Essentiel » sur des besoins que la doc ne restreint pas par offre, en y mélangeant la limite du nombre d'utilisateurs (Essentiel 1 à 5). Même famille d'erreur que la référence 2 (9 couvert → partiel), en plus fréquente.

## Points à surveiller
- Besoins ajoutés non demandés par le brief (T01 relances de factures, T06 migration, T28 rôles) : exacts, mais ils allongent la fiche.
- Sources : formats « DOC-12#0 » (T05, T12, T17–T22) et un « get_plan_limits » cité comme source (T05) : à nettoyer avant la mesure 6.
- T16 : recommande Équipe pour 2 utilisateurs avec une mise en garde « minimum 3, à vérifier » ; T13 : ne recommande pas, signale le conflit 15 utilisateurs / Entreprise (20 minimum).

## Règle de décision (Haiku, jeu de test)
Mesure 1 : agent 1 contre 0, la référence 2 est meilleure. Mesure 2 : 69,6 % contre 84,8 %, la référence 2 est meilleure. Sur ce jeu et ce prompt, le prompt unique fait mieux. Coût mesuré au solde : agent ≈ 0,06, référence 2 ≈ 0,09 (la référence 2 écrit des fiches longues, 117 627 jetons de sortie).

---
# Agent Haiku 5.5 — prompt v3 — jeu de test (3 nov. 2026) — une passe, 0 JSON invalide
Fichier : resultats_agent_haiku_v3.json. Changements du prompt v3 (voir prompts/agent_prompt_systeme.txt ; l'ancien est dans agent_prompt_systeme_v2.txt) : le statut d'un besoin dépend de la fonction, jamais du nombre d'utilisateurs ; un contournement (CSV, API) laisse le besoin non_couvert ; sources en DOC-xx sans « # » ; pas de besoin non demandé. Même workflow (boucle un brief à la fois, thinking désactivé, 10 itérations).

| # | Mesure | Agent v2 | Agent v3 | Référence 2 Haiku |
|---|---|---|---|---|
| 1 | Fonctions inventées (28) | 1 | 0 | 0 |
| 2 | Exactitude des statuts | 55/79 = 69,6 % | 65/79 = 82,3 % | 67/79 = 84,8 % |
| 3 | Absence de doc signalée | 4/6 (6/6 sur le fond) | 4/6 (6/6 sur le fond) | 4/6 (5/6) |
| 4 | Briefs vagues | 4/4 | 4/4 | 4/4 |
| 5 | Calculs et seuils | 7/7 | 7/7 | 7/7 |
| 9 | JSON invalide | 0 | 0 | 0 |
| 10 | Appels d'outils / brief | 4,1 (max 8) | 4,2 (max 8), 0 à la limite | n/a |

## Les 14 statuts faux (v3)
- couvert → partiel (9) : T04 F51, T05 F30, T06 F66, T07 F04, T08 F12 et F51, T09 F36, T10 F30 et F68.
- partiel → couvert (2) : T12 F54 (SSO) et F56 (journal d'audit) : le statut dit « couvert » avec offre minimale null alors que l'explication dit « Entreprise uniquement ». Régression due à la règle v3 (la v2 les avait justes).
- partiel → non_couvert (2) : T15 F46, T17 F69. partiel → non_couvert (1) : T18 F77.

## Lecture
La v3 corrige l'erreur principale de la v2 (couvert → partiel de 19 à 9) et la fonction « inventée » de T23. Elle crée une régression sur T12. Reste 2 statuts sous la référence 2 (65 contre 67) : à ce niveau l'écart est dans le bruit d'un jeu de 79 besoins, mais la règle de décision est stricte (au moins aussi bon). Sources : 4 sources sur 137 gardent encore un suffixe « # » (T12).
Règle de décision (test, Haiku) : mesure 1 égalité (0 contre 0) ; mesure 2 référence 2 meilleure de 2 statuts. Conclusion provisoire : le prompt unique fait au moins aussi bien. Coût : à compléter avec le solde.

## Juge IA (agent Haiku, prompt v3) — juge_ia_agent_haiku_v3_test.json
| Critère (1 à 4) | Agent v3 | Référence 2 Haiku | Seuil cible |
|---|---|---|---|
| Exactitude | 3,57 | 3,53 | ≥ 3,5 : atteint |
| Limites | 3,73 | 3,93 | ≥ 3,0 : atteint |
| Sources | 3,97 | 3,93 | ≥ 3,0 : atteint |
| Questions | 2,93 | 2,93 | ≥ 3,0 : manqué de peu (acceptable ≥ 2,5) |
| Utilité | 3,63 | 3,80 | ≥ 3,0 : atteint |
Lecture : égalité pratique. L'agent est légèrement devant sur l'exactitude et les sources, derrière sur les limites (offre minimale mal attribuée sur T05, T06, T07, T09, T10, T12, T28) et l'utilité. Faiblesse commune : trop de questions sur des briefs clairs (5 à 6 sur T03, T05, T06, T10…). Le juge est Sonnet 5.5, qui note ici des fiches d'un autre modèle ; l'écart avec le contrôle humain reste à mesurer pour l'agent. Les sources ont été jugées sur leur cohérence avec la clé et les pages citées, pas vérifiées passage par passage (mesure 6 encore ouverte).

## Contrôle humain à l'aveugle (agent v3, 12 fiches) — controle_humain_agent/resultat_controle_humain.md
Accord exact avec le juge IA : 68,3 % (cible ≥ 65 %), à 1 point près : 93,3 % (acceptable ≥ 90 %, cible ≥ 95 % manquée). Exactitude : l'humain est plus sévère que le juge (3,00 contre 3,58 sur les mêmes 12 fiches) à cause des statuts « partiel » donnés à la place de « couvert ». Questions : l'humain est plus indulgent (3,58 contre 3,00).
Coût mesuré au solde : passe 4 (prompt v2) 4,62 → 4,56 = 0,06 ; passe 5 (prompt v3) 4,56 → 4,50 = 0,06 ; référence 2 Haiku ≈ 0,09.
