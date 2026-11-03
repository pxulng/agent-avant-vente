# Les trois outils de l'agent (nœuds « Code Tool » n8n)

Chaque outil est un nœud **Code Tool** (langage JavaScript) relié au nœud **AI Agent**. Le code de chaque outil est dans `code_outils/` : il contient ses propres données (n8n Cloud ne lit pas de fichiers), donc il suffit de le coller tel quel.

| Outil | Nom à donner au nœud | Fichier de code |
|---|---|---|
| Recherche dans la documentation | `search_docs` | `code_outils/search_docs.js` |
| Offres, prix et limites | `get_plan_limits` | `code_outils/get_plan_limits.js` |
| Compatibilité avec un outil tiers | `check_integration` | `code_outils/check_integration.js` |

Le texte `query` reçu par chaque outil est la variable d'entrée fournie par n8n.

## Descriptions à copier dans le champ « Description » de chaque nœud

Ces textes sont lus par le modèle pour décider quel outil appeler. Ils font partie de la conception de l'agent.

**search_docs**
> Cherche dans la documentation produit de Brevaro. Entrée : quelques mots-clés en français (par exemple « signature électronique » ou « facture électronique »). Renvoie jusqu'à 4 passages avec leur identifiant (DOC-xx#n). La recherche porte sur les mots (pas sur le sens) : si rien d'utile ne sort, reformule avec d'autres mots avant de conclure. Les passages renvoyés peuvent être seulement voisins du sujet : lis-les avant d'affirmer quoi que ce soit. Si rien ne répond à la question après deux essais, le point n'est pas documenté.

**get_plan_limits**
> Donne le prix, les quotas et la disponibilité d'une fonction selon l'offre (Essentiel, Équipe, Entreprise). Entrée : un nom d'offre et/ou un sujet (par exemple « Équipe API », « signature », « support »). À utiliser pour toute question de prix, de limite ou de fonction qui dépend de l'offre.

**check_integration**
> Indique si Brevaro s'intègre à un outil tiers. Entrée : le nom de l'outil (par exemple « Salesforce » ou « Outlook »). Renvoie un statut : natif, via_api_ou_automatisation, migration_ponctuelle, non_disponible ou non_documente. Pour non_documente, ne présente pas l'outil comme disponible et n'affirme pas non plus que c'est impossible : à confirmer auprès de l'éditeur.

## Réglages du nœud AI Agent
- Type : Tools Agent.
- Modèle : Claude Haiku 5.5 d'abord, puis Sonnet 5.5 pour la comparaison.
- Nombre maximal d'itérations : 10 (un brief peut contenir 5 ou 6 besoins, donc plusieurs recherches ; la limite évite les boucles). On mesure le nombre d'itérations par brief et les cas où l'agent atteint la limite.
- Pas de mémoire entre deux briefs : chaque brief est traité seul.
- L'invite système (étape 5) et le format de sortie sont décrits plus tard.

## Comportements voulus des outils
- `search_docs` est une recherche par mots, pas une recherche sémantique : racines de 5 lettres (restaurer trouve restauration), pondération par rareté des mots, et un petit dictionnaire de synonymes rédigé à la main, appliqué à la requête. Le réglage `SMART = false` en tête du fichier le ramène à une correspondance de mots exacts : c'est la référence « recherche par mots-clés » de l'évaluation.
- Mesure de la recherche seule (passage attendu parmi les 4 renvoyés) : sur 16 paraphrases rédigées avant la correction, 9/16 sans le dictionnaire de synonymes, 15/16 avec (le dictionnaire a été construit à partir de ces échecs : ce chiffre est optimiste). Sur 16 autres paraphrases mises de côté, 11/16 sans, 16/16 avec. Ces tests mesurent l'outil, pas l'agent.
- Limite connue : le dictionnaire est écrit à la main. Une base vectorielle (recherche par le sens) serait plus souple, mais pour 69 passages (environ 20 Ko) elle ajouterait un service externe à héberger et à payer sans gain démontré ; le prompt unique avec toute la documentation (référence 2) joue déjà ce rôle.
- Les données (offres, intégrations, passages) sont des fichiers JSON dans `data/tools/` ; le code des outils les contient en dur parce que n8n Cloud ne lit pas de fichiers. Pour changer un tarif ou une compatibilité, on modifie `data/tools/offres.json` ou `integrations.json` (ce sont les sources), puis on relance `workflow/build_tools.py`, qui régénère le code des trois outils à coller dans n8n. C'est acceptable pour une démonstration et pas pour une production, où le nœud devrait interroger un tableau ou une base que des non-techniciens mettent à jour.
- Cet agent traite un brief à la fois et rend une fiche : il n'a pas de mémoire de conversation, parce qu'il prépare un travail pour l'avant-vente, il ne dialogue pas avec le client. Un mode conversationnel serait un autre produit.
- `get_plan_limits` répond « attribut non trouvé » avec la liste des attributs disponibles quand le sujet n'y est pas.
- `check_integration` répond `non_documente` pour tout outil absent de la liste : l'agent doit alors dire « non mentionné dans la documentation, à confirmer auprès de l'éditeur », sans le présenter comme disponible et sans affirmer que c'est impossible.
