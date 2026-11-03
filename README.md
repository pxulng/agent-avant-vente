# Brevaro pre-sales agent · Agent IA d'avant-vente

**FR** — Un assistant n8n + Claude qui prépare la fiche d'avant-vente à partir du brief d'un client (statut de chaque besoin, offre, prix, questions, limites de la documentation), et une étude qui mesure si un **agent** vaut mieux qu'un **prompt unique**. Résultat : sur ce corpus de 15 pages, le prompt unique fait au moins aussi bien, avec les deux modèles testés. Données synthétiques (éditeur fictif).
→ [Étude de cas (FR)](ETUDE_DE_CAS.md)

**EN** — An n8n + Claude assistant that prepares the pre-sales sheet from a client brief (status of each need, plan, price, questions, documentation gaps), and a study measuring whether an **agent** beats a **single prompt**. Result: on this 15-page corpus, the single prompt does at least as well, with both models tested. Synthetic data (fictional vendor).
→ [Case study (EN)](CASE_STUDY.md)

## Résultat clé · Key result (validation, 12 briefs, one run)

| Method | Statuses correct / 35 | Invented features |
|---|---|---|
| Single prompt, Sonnet 5.5 | 35 (100 %) | 0 |
| Agent, Sonnet 5.5 | 34 (97.1 %) | 0 |
| Single prompt, Haiku 5.5 | 31 (88.6 %) | 0 |
| Agent, Haiku 5.5 | 28 (80.0 %) | 0 |

## Contenu · Contents

| Dossier | Contenu |
|---|---|
| `data/docs/` | Documentation fictive de Brevaro (15 pages) · fictional Brevaro documentation |
| `data/` | Briefs de test (30) et de validation (12) · test and validation briefs |
| `prompts/` | Prompts de l'agent (v2, v3) et de la référence 2 · agent and reference-2 prompts |
| `workflow/` | Nœuds n8n, outils, notes de montage · n8n nodes, tools, setup notes |
| `evaluation/` | Seuils, gel, clés, fiches brutes, notations, juge IA, contrôle humain · thresholds, freeze record, keys, raw sheets, scoring, AI judge, human check |

## Limites · Limits

Petits échantillons, juge IA indulgent sur l'exactitude, un seul relecteur humain, données synthétiques. Détails dans l'étude. · Small samples, an AI judge lenient on accuracy, one human reviewer, synthetic data. Details in the study.

## Contrôle humain à l'aveugle · Blind human check
Les fichiers de correspondance (fiche ↔ méthode) ne sont pas publiés, pour que le contrôle reste reproductible à l'aveugle. · The sheet-to-method mapping files are not published, so the blind check stays reproducible.
