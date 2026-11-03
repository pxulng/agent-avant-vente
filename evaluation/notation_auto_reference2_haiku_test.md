# Référence 2 (prompt unique) — Haiku 5.5 — jeu de test — mesures automatiques (3 nov. 2026)

Fichier : resultats_reference2_haiku_v2.json (3e passe, limite de sortie 16 000 jetons). Statuts lus à la main contre cle_briefs_test.csv ; juge IA, sources et contrôle humain pas encore faits.

## Journal d'erreurs de lancement
- v0 : limite de sortie 1 024 jetons, 11/30 JSON coupés (resultats_reference2_haiku.json). Réglage, pas le modèle.
- v1 : limite 4 000 jetons, 15/30 coupés, tous à 4 000 (resultats_reference2_haiku_v1.json). Fiches longues.
- v2 : limite 16 000 jetons, 0/30 invalide, max 5 915 jetons de sortie. Seule passe notée.

## Mesures
| # | Mesure | Résultat | Seuil |
|---|---|---|---|
| 1 | Fonctions inventées (28 besoins nc/nd) | 0 relevée | cible |
| 2 | Exactitude des statuts | 67/79 = 84,8 % | acceptable (cible 90 %) |
| 3 | Absence de doc signalée | 4/6 par le statut (5/6 si T13, signalé dans le texte, compte) | acceptable / cible limite |
| 4 | Briefs vagues | 4/4 | cible |
| 5 | Calculs et seuils | 7/7 | cible |
| 9 | JSON invalide | 0 | cible |

## Les 12 statuts faux
9 couvert → partiel (T02 F36, T03 F12, T04 F51, T06 F68, T07 F04, T08 F12, T10 F30, T10 F66, T29 F36) : prudence excessive, pas d'invention.
3 autres : T15 F46 (partiel → non_couvert), T17 F69 (partiel → non_couvert), T18 F77 (partiel → non_documente).

## Points à surveiller
- T16 : dit que l'offre Équipe « n'est pas accessible » pour 2 utilisateurs ; la clé attend « à vérifier » (la doc ne tranche pas).
- T30 : donne un exemple chiffré « indicatif » (10 utilisateurs) alors que la clé interdit un total sans connaître l'effectif ; étiqueté comme exemple.

## Consommation (30 briefs)
209 354 jetons d'entrée, 117 627 jetons de sortie. Coût en euros non calculé (tarif à confirmer).

---
# Référence 2 — Sonnet 5.5 — jeu de test (3 nov. 2026) — une passe, 0 JSON invalide
Fichier : resultats_reference2_sonnet.json. Jetons : 209 354 entrée, 93 220 sortie (max 4 480). Solde : 1,73 → 0,32 (≈ 1,41), contre ≈ 0,09 pour Haiku.

| Mesure | Haiku 5.5 | Sonnet 5.5 |
|---|---|---|
| 1 Fonctions inventées (28) | 0 | 0 |
| 2 Exactitude des statuts | 67/79 = 84,8 % | 72/79 = 91,1 % |
| 3 Absence de doc signalée (par le statut) | 4/6 (5/6 en comptant T13) | 4/6 (6/6 sur le fond : T13 et T16 signalés « à confirmer ») |
| 4 Briefs vagues | 4/4 | 4/4 |
| 5 Calculs et seuils | 7/7 | 7/7 |
| 9 JSON invalide | 0 | 0 |
| 7 Juge IA : exactitude / limites / sources / questions / utilité | 3,53 / 3,93 / 3,93 / 2,93 / 3,80 | voir juge_ia_reference2_sonnet_test.json |

Même rigueur de lecture pour les deux modèles (T05 et T15 comptés faux pour Sonnet aussi). Juge = Sonnet 5.5 en session : pas indépendant du producteur pour la passe Sonnet (risque d'auto-préférence).
