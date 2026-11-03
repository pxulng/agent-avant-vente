# Contrôle humain à l'aveugle — série 2 (agent Haiku v3, 12 fiches tirées au hasard)

Fiches : T02, T07, T17, T09, T20, T25, T06, T05, T03, T21, T28, T29 (mélangées). Notes humaines : feuille_de_notes_remplie.csv. Notes du juge IA : juge_ia_agent_haiku_v3_test.json.

## Accord humain / juge IA (60 notes : 12 fiches × 5 critères)
- Accord exact : 41/60 = 68,3 % (cible ≥ 65 % : atteint).
- À 1 point près : 56/60 = 93,3 % (cible ≥ 95 % : manqué ; acceptable ≥ 90 % : atteint).
- Série 1 (référence 2) : 71,7 % et 98,3 %.

| Critère | Accord exact | À 1 point | Moyenne humain | Moyenne juge (mêmes fiches) |
|---|---|---|---|---|
| Exactitude | 6/12 | 11/12 | 3,00 | 3,58 |
| Limites | 9/12 | 12/12 | 3,83 | 3,58 |
| Sources | 12/12 | 12/12 | 4,00 | 4,00 |
| Questions | 4/12 | 9/12 | 3,58 | 3,00 |
| Utilité | 10/12 | 12/12 | 3,58 | 3,58 |

## Où le juge et l'humain se séparent
- Exactitude : l'humain est plus sévère sur 5 fiches (T07, T17, T09, T06, T05 : 2 contre 3) et sur T28 (2 contre 4). Les statuts « partiel » à la place de « couvert » (pack d'accompagnement, relance des devis expirés, versions de devis, Factur-X) sont notés 2 par l'humain, 3 par le juge ; T28 (brief vague, CRM classé « partiel ») est noté 2 par l'humain. Le juge a été trop indulgent sur la prudence excessive.
- Questions : l'humain est plus indulgent sur 3 fiches (T25, T03, T21 : 4 contre 2). Le juge a pénalisé 5 questions sur un brief clair ; l'humain a jugé les questions utiles. La mesure des questions reste la plus subjective.
- Sources : accord total.

## Conséquence
Sur l'exactitude, la mesure humaine de l'agent v3 (3,00 sur 12 fiches) est sous la cible de 3,5 ; la note du juge (3,57 sur 30) est probablement un peu trop haute. Les deux notes se rejoignent sur le fait qu'il reste des statuts trop prudents. L'écart juge/humain sur l'exactitude est à publier tel quel.
