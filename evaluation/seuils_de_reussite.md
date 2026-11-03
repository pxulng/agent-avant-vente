# Seuils de réussite (fixés le 3 novembre 2026, avant tout lancement d'un modèle)

Ces seuils sont écrits avant d'avoir vu un seul résultat de l'agent ou de la référence 2. Ils ne changent pas après. Si un seuil se révèle mal choisi, on le dit dans l'étude de cas, on ne le corrige pas en silence.

## Règles de la méthode
- Une seule passe par version et par modèle.
- Le jeu de test (30 briefs) sert à améliorer le prompt, version après version (v1, v2…), avec un journal des changements.
- Le jeu de validation (12 briefs) n'est lancé qu'une fois, avec le prompt gelé. Les chiffres de validation sont ceux qu'on retient.
- Toute erreur est consignée dans le journal d'erreurs, même quand elle est corrigée ensuite.

## Les seuils

Pour chaque mesure : **Cible** = on peut dire que c'est réussi ; **Acceptable** = utilisable avec relecture attentive ; en dessous = insuffisant.

| # | Mesure | Cible | Acceptable |
|---|---|---|---|
| 1 | **Fonctions inventées** : besoin attendu `non_couvert` ou `non_documente`, présenté `couvert` ou `partiel`. Test : 28 besoins ; validation : 15. **Bloquant.** | Validation : 0. Test : 0 | Test : 1 au plus |
| 2 | **Exactitude des statuts** sur les besoins rattachés à une fonction (test : 79 ; validation : 35) | 90 % ou plus | 80 à 89 % |
| 3 | **Absence de documentation signalée** : besoins attendus `non_documente` présentés `non_documente` (test : 6 ; validation : 4) | Test : 5 sur 6 ; validation : 4 sur 4 | Test : 4 sur 6 ; validation : 3 sur 4 |
| 4 | **Briefs vagues** : au moins 2 questions pertinentes, et ni offre recommandée ni prix total (test : 4 briefs ; validation : 2) | Test : 4 sur 4 ; validation : 2 sur 2 | Test : 3 sur 4 ; validation : 1 sur 2 |
| 5 | **Calculs et seuils d'offre** (besoins sans fonction, test : 7 ; validation : 3) | Test : 6 sur 7 ; validation : 3 sur 3 | Test : 5 sur 7 ; validation : 2 sur 3 |
| 6 | **Sources exactes** : part des sources citées qui contiennent bien l'information | 90 % ou plus | 80 à 89 % |
| 7 | **Notes du juge IA** (1 à 4), moyenne par critère | Exactitude ≥ 3,5 ; autres critères ≥ 3,0 | Exactitude ≥ 3,0 ; autres ≥ 2,5 |
| 8 | **Contrôle humain à l'aveugle** : 12 fiches tirées au hasard, notées sans savoir d'où elles viennent | Accord exact avec le juge IA ≥ 65 %, et à 1 point près ≥ 95 % | Accord à 1 point près ≥ 90 % |
| 9 | **JSON invalide ou tronqué** | 0 | 1 sur 30 au plus |
| 10 | **Agent seulement : itérations** | Moyenne ≤ 6 ; au plus 2 briefs sur 30 atteignent la limite de 10 | Moyenne ≤ 8 |

Le coût par brief est mesuré et publié (jetons × tarif du modèle) mais n'a pas de seuil : il sert à la décision ci-dessous.

## Règle de décision : l'agent contre la référence 2 (même modèle, mêmes briefs)

L'agent n'est retenu que s'il fait mieux ou aussi bien que le prompt unique sur les deux mesures qui comptent, dans cet ordre :

1. **Fonctions inventées** (mesure 1) : l'agent en a au plus autant que la référence 2.
2. **Exactitude des statuts** (mesure 2) : l'agent est au moins aussi bon que la référence 2.

| Résultat | Conclusion publiée |
|---|---|
| L'agent bat la référence 2 sur 1 ou 2 | L'agent est justifié, avec son coût supplémentaire. |
| Égalité, et l'agent coûte moins cher | L'agent est retenu pour le coût. |
| Égalité, et la référence 2 coûte moins cher | Le prompt unique suffit à ce volume de documentation. |
| La référence 2 fait mieux | Le prompt unique suffit et l'agent n'apporte rien ici. L'intérêt de l'agent resterait une hypothèse pour un corpus beaucoup plus grand, non testée. |

## Modèle recommandé
Le modèle le moins cher qui atteint tous les seuils « cible » sur le jeu de validation. Si aucun ne les atteint, on le dit et on recommande une relecture humaine systématique (ce qui est déjà le principe de l'outil).

## Référence 1 (recherche par mots-clés, sans IA)
Mesurée sur le jeu de test le 3 novembre 2026 : la bonne page figure parmi les 4 passages renvoyés pour **67 besoins sur 75 (89 %)**, avec une mesure indulgente (une seule page attendue suffit). Elle ne produit aucune réponse : pas de statut, pas d'offre, pas de calcul, pas de question, pas de signalement des limites. Ses notes sur les critères 1, 2, 4 et 5 sont donc nulles par construction ; elle ne sert qu'à montrer que retrouver la page est la partie facile et que l'essentiel du travail est le jugement.
