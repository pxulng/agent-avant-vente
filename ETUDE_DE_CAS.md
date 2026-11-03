# Un agent IA d'avant-vente : faut-il vraiment un agent ?

Étude de cas · Brevaro (éditeur fictif) · n8n + Claude · données synthétiques · [English version](CASE_STUDY.md)

## En bref

Un avant-vente reçoit le brief d'un client et doit répondre à trois questions : ce que le produit fait, sur quelle offre, et ce que la documentation ne dit pas. J'ai construit un assistant qui prépare cette fiche, puis j'ai mesuré s'il valait mieux un **agent** (qui cherche lui-même dans la documentation avec 3 outils) ou un **prompt unique** (toute la documentation dans une seule requête).

Résultat : sur ce corpus de 15 pages, **le prompt unique fait mieux ou aussi bien que l'agent**, avec les deux modèles testés, sur un jeu de test de 30 briefs et sur un jeu de validation de 12 briefs jamais vu pendant la mise au point. Aucune des quatre configurations n'invente de fonction. Le modèle qui atteint tous les seuils sur la validation est **Sonnet 5.5 avec le prompt unique** (35 statuts sur 35). Haiku 5.5 coûte environ 16 fois moins, mais reste entre 85 et 89 % : utilisable avec une relecture attentive.

L'intérêt d'un agent pour un corpus beaucoup plus grand reste une hypothèse. Je ne l'ai pas testée.

## Le cas

Brevaro est un logiciel de devis et de suivi commercial pour PME, inventé pour ce projet. Sa documentation fait 15 pages (environ 2 200 mots) : devis, catalogue, facturation, intégrations, sécurité, offres et prix, etc. Elle contient des pièges voulus : fonctions réservées à une offre, limites chiffrées, fonctions absentes, et sujets que la documentation ne traite pas du tout.

Pour chaque brief, l'assistant produit une fiche JSON relue ensuite par l'avant-vente : besoins découpés, un statut par besoin (`couvert`, `partiel`, `non_couvert`, `non_documente`), l'offre minimale, les sources (DOC-xx), le calcul du prix, les questions à poser, une esquisse de solution et les risques. L'erreur qui coûte le plus cher en avant-vente est de promettre une fonction qui n'existe pas. C'est donc la mesure bloquante.

## La méthode

Les règles ont été écrites et figées le 3 novembre 2026, avant de lancer le moindre modèle (`evaluation/seuils_de_reussite.md`).

- **Référence 1** : recherche par mots-clés, sans IA. Elle sert de plancher.
- **Référence 2** : un seul prompt contenant toute la documentation.
- **Agent** : n8n AI Agent avec 3 outils (`search_docs`, `get_plan_limits`, `check_integration`), 10 itérations maximum, un brief à la fois.
- **Deux modèles** : Haiku 5.5 et Sonnet 5.5.
- **Jeu de test** (T01 à T30, 30 briefs) : sert à améliorer le prompt de l'agent, version après version.
- **Jeu de validation** (V01 à V12, 12 briefs) : lancé **une seule fois** par méthode, prompts et réglages gelés (empreintes SHA-256 dans `evaluation/GEL_validation.md`). Ce sont les chiffres retenus.
- **Notation** : statuts comparés à une clé écrite à l'avance (79 fonctionnalités au test, 35 à la validation), puis juge IA (note de 1 à 4 sur 5 critères) et contrôle humain à l'aveugle.
- **Règle de décision** : l'agent n'est retenu que s'il a au plus autant de fonctions inventées que la référence 2, puis une exactitude de statuts au moins égale.
- **Journal d'erreurs** : tout est consigné, y compris les passes ratées.

## Résultats

### Jeu de validation (12 briefs, une passe, prompts gelés)

| Méthode | Statuts justes (sur 35) | Fonctions inventées (sur 15 attendues non couvertes ou non documentées) | JSON valides |
|---|---|---|---|
| Référence 2, Sonnet 5.5 | **35 (100 %)** | 0 | 12/12 |
| Agent, Sonnet 5.5 | 34 (97,1 %) | 0 | 12/12 |
| Référence 2, Haiku 5.5 | 31 (88,6 %) | 0 | 12/12 |
| Agent, Haiku 5.5 | 28 (80,0 %) | 0 | 12/12 |

Les quatre méthodes signalent correctement les 4 points non documentés (V10 : accessibilité RGAA, références clients, taille des pièces jointes, temps de réponse de l'API) sans inventer un chiffre. Les deux briefs vagues (V11, V12) donnent des questions et ni offre ni prix. Aucune n'a recommandé l'offre Essentiel pour 150 devis par mois, ni affirmé qu'un circuit de validation à trois niveaux existe.

Une différence se voit sur V12 (« relation client »). Les deux références 2 précisent que Brevaro ne gère pas les tickets de support. Les deux agents posent des questions sans le dire.

Les erreurs de l'agent Haiku : des statuts trop prudents (« partiel » au lieu de « couvert » pour Factur-X, le mobile, la formation), et deux « couvert » à la place de « partiel » pour Make et les tarifs par client, qui exigent l'offre Équipe.

### Jeu de test (30 briefs)

| Méthode | Statuts justes (sur 79) | Fonctions inventées (sur 28) | JSON invalides |
|---|---|---|---|
| Référence 2, Sonnet 5.5 | 72 (91,1 %) | 0 | 0 |
| Agent, Sonnet 5.5 (prompt v3) | 67/70 = 95,7 % sur 27 fiches valides ; 84,8 % si les 3 invalides comptent comme fausses | 0 | 3 |
| Référence 2, Haiku 5.5 | 67 (84,8 %) | 0 | 0 |
| Agent, Haiku 5.5 (prompt v3) | 65 (82,3 %) | 0 | 0 |

Le prompt de l'agent est passé par trois versions sur ce jeu : la v1 et la v2 ont échoué pour des raisons de réglage (voir plus bas), la v2 avait 24 statuts faux, la v3 en a 14. La référence 2 n'a pas été améliorée. Les 3 JSON invalides de l'agent Sonnet sont deux sorties vides (T05, T19) et un JSON suivi d'un paragraphe de texte (T04). Je n'ai pas vérifié la cause ; la réflexion adaptative du modèle est une hypothèse. Aucun n'a été réparé à la main.

La référence 1 (mots-clés) retrouve la bonne page pour 67 besoins sur 75 (89 %), mais ne produit ni statut, ni offre, ni calcul, ni question. Retrouver la page est la partie facile. Le jugement est le vrai travail.

### Juge IA et contrôle humain (jeu de test)

| Critère (1 à 4) | Agent Haiku | Réf. 2 Haiku | Agent Sonnet (27 valides) | Réf. 2 Sonnet |
|---|---|---|---|---|
| Exactitude | 3,57 | 3,53 | 3,89 | 3,77 |
| Limites | 3,73 | 3,93 | 4,00 | 3,97 |
| Sources | 3,97 | 3,93 | 4,00 | 4,00 |
| Questions | 2,93 | 2,93 | 3,67 | 3,03 |
| Utilité | 3,63 | 3,80 | 3,85 | 3,93 |

Le juge est Sonnet 5.5, qui note ici des fiches du même modèle : risque d'auto-préférence. Le contrôle humain à l'aveugle (12 fiches, un seul relecteur qui connaissait la clé) montre que ce juge est **trop indulgent sur l'exactitude** : 3,00 pour l'humain contre 3,58 pour le juge sur les mêmes fiches de l'agent Haiku. L'accord exact est de 68,3 % (cible 65 %), à un point près de 93,3 % (cible 95 %, manquée). Sur la série de la référence 2 : 71,7 % et 98,3 %. Je n'ai pas lancé le juge IA ni le contrôle humain sur le jeu de validation.

### Coût (mesuré au solde du compte, par passe de 30 briefs)

| Méthode | Coût par passe | Par brief |
|---|---|---|
| Agent Haiku | environ 0,06 | environ 0,002 |
| Référence 2 Haiku | environ 0,09 | environ 0,003 |
| Agent Sonnet | 1,38 | environ 0,046 |
| Référence 2 Sonnet | environ 1,41 | environ 0,047 |

Unité : solde de la console Anthropic. Les jetons ne sont pas exposés par n8n pour l'agent, donc je n'ai pas de coût par jeton. La passe de validation complète (quatre méthodes, 12 briefs) a coûté 1,05 au total (3,12 → 2,07).

## Ce que dit la règle de décision

1. **Fonctions inventées** : égalité à 0, avec les deux modèles, sur le test comme sur la validation.
2. **Exactitude des statuts** : la référence 2 est meilleure ou égale, avec les deux modèles, sur la validation (100 contre 97,1 % pour Sonnet, 88,6 contre 80,0 % pour Haiku). Sur le test, avec Sonnet, l'agent est meilleur si on écarte ses 3 sorties invalides (95,7 contre 91,1 %) et moins bon si on les compte (84,8 %). Je les compte, parce qu'une fiche vide est une fiche perdue.

L'agent ne coûte pas moins cher avec Sonnet (1,38 contre 1,41). Conclusion publiée : **à cette taille de documentation, le prompt unique suffit et l'agent n'apporte rien**.

## Quel modèle

La règle prévoit le modèle le moins cher qui atteint tous les seuils « cible » sur la validation. Haiku n'y arrive pas sur l'exactitude des statuts (88,6 % contre 90 % exigés) : sa place est « utilisable avec relecture attentive ». **Sonnet 5.5 avec le prompt unique** atteint la cible sur toutes les mesures faites sur la validation : fonctions inventées, statuts, non documenté, briefs vagues, calculs, JSON valide. L'agent Sonnet est au seuil acceptable sur les calculs (sur V06, il classe « 150 devis par mois » en `couvert` alors que la limite de 100 devis existe en Essentiel ; il recommande quand même l'offre Équipe, donc le prix est juste).

Les mesures « sources exactes », « juge IA » et « contrôle humain » n'ont été faites que sur le jeu de test. La recommandation de modèle repose donc sur les mesures de statuts. Dans tous les cas, l'outil produit une fiche qu'un humain relit avant d'envoyer quoi que ce soit au client.

## Limites et biais

- **Petits échantillons.** 12 briefs et 35 statuts à la validation : un statut vaut 2,9 points. L'écart entre l'agent et la référence 2 est d'un statut avec Sonnet (34 contre 35) et de trois avec Haiku (28 contre 31). Ce sont des tendances, pas des preuves.
- **Asymétrie assumée.** Le prompt de l'agent a été amélioré en trois versions sur le jeu de test ; celui de la référence 2 est resté à sa première version. Cela favorise l'agent sur le test. La validation, jamais vue pendant la mise au point, corrige ce biais, et l'agent n'y gagne pas.
- **Réglage de réflexion différent.** Haiku tourne sans réflexion ; Sonnet refuse de la désactiver et tourne en réflexion adaptative, effort faible. La comparaison Haiku contre Sonnet mélange donc le modèle et ce réglage.
- **Juge non indépendant.** Le juge IA est Sonnet 5.5, et il est indulgent sur l'exactitude (voir plus haut). Un seul relecteur humain, qui connaissait la clé.
- **Sources.** La part de sources exactes (mesure 6) n'a pas été vérifiée passage par passage : seulement leur cohérence avec la clé.
- **Données synthétiques.** Corpus, briefs et clé ont été écrits pour l'étude. Un vrai corpus a des contradictions et des pages obsolètes que celui-ci n'a pas.
- **Seuils.** Les seuils ont été figés avant les mesures et n'ont pas bougé. Le seuil de 90 % sur les statuts est strict pour 35 statuts.
- **Un point commun sur le test.** Trois statuts (T15, T17, T18) sont faux pour plusieurs méthodes à la fois : ils viennent peut-être de la clé (« partiel » pour une fonction absente dans sa version utile) plutôt que des modèles.

## Ce qui a mal tourné (journal d'erreurs, résumé)

- **Référence 2** : limite de sortie à 1 024 puis 4 000 jetons, JSON coupés (11 puis 15 sur 30). Passée à 16 000 : 0 invalide.
- **Agent Haiku** : passe 1, 29 briefs sur 30 en « Bad request » (Haiku réfléchit par défaut et n8n renvoie les blocs de réflexion, que l'API refuse). Passes 2 et 3, 30 briefs sur 30 « Max iterations (10) reached » : n8n lançait les 30 briefs en un lot et appliquait la limite au lot entier. Corrigé par une boucle, un brief à la fois. Les passes ratées ont coûté environ 0,64 pour rien.
- **Agent Sonnet** : « does not support disabling thinking », corrigé en réflexion adaptative.
- **Lancement de la validation** : les 4 passes ont été lancées une fois chacune depuis n8n, sans relance, avec 12 fiches valides sur 12 pour chacune.

## Reproduire

Tout est dans le dépôt : documentation (`data/docs/`), briefs et clés (`data/`, `evaluation/cle_briefs_*.csv`), prompts (`prompts/`), nœuds et notes n8n (`workflow/`), seuils, gel, journaux de notation et fiches brutes (`evaluation/`). Les workflows n8n utilisent un identifiant d'authentification Anthropic à renseigner.
