# Workflow n8n

`agent_avant_vente_sonnet.json` : export du workflow de l'agent avant-vente (Sonnet 5.5), sans identifiants. Il contient le nœud Code « Briefs », la boucle (un brief à la fois), le nœud AI Agent avec ses trois outils (`search_docs`, `get_plan_limits`, `check_integration`, dont le code est aussi dans `code_outils/`), puis le nœud « Lecture » qui contrôle le JSON.

Pour l'utiliser : Workflows > Import from file, rattacher votre propre identifiant Anthropic au nœud « Claude Sonnet 5.5 », puis lancer.

Le montage de la référence 2 (prompt unique) est décrit dans `reference2_mode_emploi.md`.

---

**EN** : `agent_avant_vente_sonnet.json` is the export of the pre-sales agent workflow (Sonnet 5.5), without credentials: briefs, loop, AI Agent node with three code tools, JSON check. Import it in n8n and attach your own Anthropic credential. The single-prompt reference is described in `reference2_mode_emploi.md`.

`reference2_prompt_unique_haiku55.json` : workflow de la référence 2 (prompt unique avec toute la documentation, sans outils), sans identifiants. Pour Sonnet 5.5, changer le modèle dans « Message a model ».

Correction : le fichier exporté initialement contenait par erreur le modèle Haiku 5.5 sans réflexion (état du workflow au moment de l'export). Il est maintenant réglé sur Sonnet 5.5 avec réflexion adaptative. L'étude a utilisé un niveau d'effort bas ; ce réglage n'est pas dans le fichier, à ajuster dans le nœud si besoin.
