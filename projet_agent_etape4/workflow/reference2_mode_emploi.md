# Référence 2 : un seul prompt avec toute la documentation (sans outils)

But : mesurer ce que donne Claude quand on lui met toute la documentation sous les yeux, sans agent ni outils. C'est la comparaison la plus dure pour l'agent.

## Construire le workflow n8n (4 nœuds)

1. **Manual Trigger**.
2. **Code**, nommé exactement `Briefs` : colle `n8n_briefs_test.js` (30 briefs). Mode « Run Once for All Items ».
3. **Message a model** (Anthropic) :
   - modèle : Claude Haiku 5.5 pour la première passe, Sonnet 5.5 pour la seconde (une passe par modèle, jamais deux sur le même jeu) ;
   - message système : tout le contenu de `../prompts/reference2_prompt_systeme.txt` ;
   - message utilisateur : `{{ $json.brief }}` ;
   - réglage des jetons de sortie : 2 000 au moins, pour que le JSON ne soit pas coupé.
4. **Code**, nommé `Lecture` : colle `n8n_lecture_fiches.js`. Mode « Run Once for All Items ».

## Lancer et récupérer
- Exécute le workflow une fois. Copie le champ `resultats` du nœud `Lecture` dans un fichier `resultats_reference2_haiku.json` (puis `_sonnet.json`).
- Note aussi `nb_json_invalides` : un JSON invalide est une erreur à consigner dans le journal d'erreurs, pas à corriger à la main.

## À ne pas faire
- Ne lance pas le jeu de validation : il est réservé à la fin, une seule fois, avec le prompt gelé.
- Ne modifie pas le prompt après avoir vu les résultats du jeu de test sans le noter dans le journal des versions (v1, v2…), comme pour tes deux premiers projets.
