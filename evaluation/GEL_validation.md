# Gel avant le jeu de validation (3 nov. 2026, 16 h 35 heure de Paris)

Le jeu de validation (V01 à V12) n'a jamais été lancé. À partir de maintenant, plus aucun changement de prompt, d'outil, de réglage ni de clé. Chaque méthode passe une seule fois sur les 12 briefs.

## Ce qui est gelé (empreintes SHA-256)
- Prompt agent v3 : prompts/agent_prompt_systeme.txt — 54de85247f6f43f2459f521f016a6087e7a58e591d43da57f17afba1bda867e8
- Prompt référence 2 : prompts/reference2_prompt_systeme.txt — f6330f4b1fb4713254477d4038020d89294845afad021e0544dbb7692a9c288a (règles communes v1, jamais itérées sur le jeu de test)
- Règles communes v1 : prompts/regles_communes.md — 5d9b0d080db07b50643b9485a1c90b4d4b2ff05db38be65c7b938ec14b3ea0a0
- Briefs de validation : workflow/n8n_briefs_validation.js — 17b3fc500d2825c26fd5a54b10022b2460c176b2cc1d6e2241c32a03dbd7fb1d
- Clé : evaluation/cle_briefs_validation.csv

## Configurations
- Agent : AI Agent n8n v3.1, 3 outils Code Tool (search_docs, get_plan_limits, check_integration), 10 itérations, un brief à la fois (boucle), 16 000 jetons de sortie. Haiku 5.5 : réflexion désactivée. Sonnet 5.5 : réflexion adaptive, effort low (Sonnet refuse « désactivée »).
- Référence 2 : un seul prompt avec toute la documentation, 16 000 jetons de sortie.
- 4 passes : référence 2 Haiku, référence 2 Sonnet, agent Haiku, agent Sonnet. Aucune relance, même si un brief échoue ; les sorties invalides sont comptées comme échecs et non réparées.

## Asymétrie connue (à publier)
Le prompt de l'agent a été amélioré en deux versions (v2, v3) sur le jeu de test. Le prompt de la référence 2 ne l'a pas été. Cela favorise l'agent sur le jeu de test ; le jeu de validation, jamais vu, corrige ce biais.
