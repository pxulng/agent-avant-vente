# Grille de notation

Chaque fiche (une par brief) est notée de 1 à 4 sur cinq critères, par un juge IA (Sonnet 5.5, avec la clé de réponse du brief) puis, sur un échantillon, par une personne à l'aveugle (sans savoir quelle méthode a produit la fiche). Le juge IA et l'humain utilisent la même grille.

| Note | Sens général |
|---|---|
| 4 | Juste et complet, utilisable tel quel par l'avant-vente |
| 3 | Juste, avec un manque ou une imprécision mineurs |
| 2 | Une erreur ou un manque qui obligerait l'avant-vente à reprendre la réponse |
| 1 | Erreur grave : fonction inventée, promesse fausse, ou ignorance d'une limite qui change la réponse |

## Les cinq critères

1. **Exactitude (bloquant).** Les statuts (couvert, partiel, non_couvert, non_documente) correspondent à la clé. Aucune fonction, aucun chiffre, aucune date inventés. Une fonction inventée, ou une absence de documentation présentée comme une disponibilité, donne 1 d'office.
2. **Signalement des limites.** L'offre minimale est correcte ; les seuils (nombre minimal ou maximal d'utilisateurs, quotas) sont repérés ; `non_documente` est bien distingué de `non_couvert` ; les calculs de prix sont justes.
3. **Sources.** Chaque besoin renvoie à la bonne page de documentation, et le passage cité contient vraiment l'information.
4. **Questions de clarification.** Des questions pertinentes quand le brief est vague (et pas de recommandation d'offre dans ce cas) ; pas de questions inutiles quand le brief est clair.
5. **Utilité de l'esquisse.** L'avant-vente pourrait s'en servir : recommandation d'offre cohérente, ce qui reste à confirmer, risques réels et non génériques.

## Mesures automatiques complémentaires
- Statut donné contre statut attendu, par besoin.
- Fonctions inventées : besoin attendu `non_couvert` ou `non_documente` mais présenté `couvert` ou `partiel`.
- JSON invalide ou tronqué.
- Jetons et coût par brief ; pour l'agent : nombre d'itérations et d'appels d'outils, briefs qui atteignent la limite de 10.

## Limites connues de la méthode
- Un juge IA a tendance à mieux noter ses propres réponses : le contrôle humain à l'aveugle sert à le vérifier, et l'écart est publié.
- Une seule passe par version et par modèle : les modèles ne répondent pas exactement pareil deux fois ; on ne publie donc pas de différence de 1 ou 2 points comme une preuve.
- Briefs fictifs et courts (31 mots en moyenne), documentation fictive de 15 pages : les résultats ne disent rien de ce qui se passerait avec une documentation de plusieurs centaines de pages.
