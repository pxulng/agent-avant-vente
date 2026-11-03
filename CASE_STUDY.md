# A pre-sales AI agent: do you actually need an agent?

Case study · Brevaro (fictional vendor) · n8n + Claude · synthetic data · [Version française](ETUDE_DE_CAS.md)

## Summary

A pre-sales engineer receives a client brief and has to answer three questions: what the product does, on which plan, and what the documentation does not say. I built an assistant that prepares that sheet, then measured whether an **agent** (which searches the documentation itself with 3 tools) beats a **single prompt** (the whole documentation in one request).

Result: on this 15-page corpus, **the single prompt does at least as well as the agent**, with both models tested, on a 30-brief test set and on a 12-brief validation set that was never seen during tuning. None of the four configurations invents a feature. The model that reaches every target on validation is **Sonnet 5.5 with the single prompt** (35 statuses out of 35). Haiku 5.5 costs about 16 times less but stays between 85 and 89 %: usable with careful review.

Whether an agent pays off on a much larger corpus is a hypothesis. I did not test it.

## The case

Brevaro is quote and sales-tracking software for small and mid-sized businesses, invented for this project. Its documentation is 15 pages (about 2,200 words): quotes, catalogue, invoicing, integrations, security, plans and prices, and so on. It contains deliberate traps: features limited to one plan, numeric limits, missing features, and topics the documentation does not cover at all.

For each brief the assistant produces a JSON sheet that a pre-sales engineer then reviews: needs split out, one status per need (`couvert`, `partiel`, `non_couvert`, `non_documente`, i.e. covered, partial, not covered, not documented), minimum plan, sources (DOC-xx), price calculation, questions to ask, a solution sketch and risks. The costliest pre-sales mistake is promising a feature that does not exist, so that is the blocking measure.

## Method

The rules were written and frozen on 3 November 2026, before any model was run (`evaluation/seuils_de_reussite.md`).

- **Reference 1**: keyword search, no AI. It is the floor.
- **Reference 2**: one prompt containing the whole documentation.
- **Agent**: n8n AI Agent with 3 tools (`search_docs`, `get_plan_limits`, `check_integration`), 10 iterations at most, one brief at a time.
- **Two models**: Haiku 5.5 and Sonnet 5.5.
- **Test set** (T01 to T30, 30 briefs): used to improve the agent prompt, version after version.
- **Validation set** (V01 to V12, 12 briefs): run **once** per method, with prompts and settings frozen (SHA-256 hashes in `evaluation/GEL_validation.md`). These are the numbers that count.
- **Scoring**: statuses compared with a key written in advance (79 features on test, 35 on validation), then an AI judge (1 to 4 on 5 criteria) and a blind human check.
- **Decision rule**: the agent is kept only if it has no more invented features than reference 2 and then at least equal status accuracy.
- **Error log**: everything is recorded, including failed runs.

## Results

### Validation set (12 briefs, one run, frozen prompts)

| Method | Correct statuses (out of 35) | Invented features (out of 15 expected not covered or not documented) | Valid JSON |
|---|---|---|---|
| Reference 2, Sonnet 5.5 | **35 (100 %)** | 0 | 12/12 |
| Agent, Sonnet 5.5 | 34 (97.1 %) | 0 | 12/12 |
| Reference 2, Haiku 5.5 | 31 (88.6 %) | 0 | 12/12 |
| Agent, Haiku 5.5 | 28 (80.0 %) | 0 | 12/12 |

All four methods flag the 4 undocumented points correctly (V10: RGAA accessibility, client references, maximum attachment size, API response time) without inventing a figure. The two vague briefs (V11, V12) get questions and neither a plan nor a price. No method recommended the Essentiel plan for 150 quotes a month, or claimed that a three-level approval workflow exists.

One difference shows on V12 ("customer relations"). Both reference-2 runs state that Brevaro does not handle support tickets. Both agents ask questions without saying so.

The Haiku agent's errors: over-cautious statuses ("partial" instead of "covered" for Factur-X, mobile, training), and two "covered" where "partial" was expected for Make and per-client price lists, which require the Équipe plan.

### Test set (30 briefs)

| Method | Correct statuses (out of 79) | Invented features (out of 28) | Invalid JSON |
|---|---|---|---|
| Reference 2, Sonnet 5.5 | 72 (91.1 %) | 0 | 0 |
| Agent, Sonnet 5.5 (prompt v3) | 67/70 = 95.7 % on 27 valid sheets; 84.8 % if the 3 invalid ones count as wrong | 0 | 3 |
| Reference 2, Haiku 5.5 | 67 (84.8 %) | 0 | 0 |
| Agent, Haiku 5.5 (prompt v3) | 65 (82.3 %) | 0 | 0 |

The agent prompt went through three versions on this set: v1 and v2 failed for configuration reasons (see below), v2 had 24 wrong statuses, v3 has 14. Reference 2 was not improved. The Sonnet agent's 3 invalid outputs are two empty outputs (T05, T19) and one JSON followed by a paragraph of text (T04). I did not check the cause; the model's adaptive thinking is a hypothesis. None was repaired by hand.

Reference 1 (keywords) finds the right page for 67 of 75 needs (89 %), but produces no status, plan, calculation or question. Finding the page is the easy part. Judgment is the real work.

### AI judge and human check (test set)

| Criterion (1 to 4) | Haiku agent | Haiku ref. 2 | Sonnet agent (27 valid) | Sonnet ref. 2 |
|---|---|---|---|---|
| Accuracy | 3.57 | 3.53 | 3.89 | 3.77 |
| Limits | 3.73 | 3.93 | 4.00 | 3.97 |
| Sources | 3.97 | 3.93 | 4.00 | 4.00 |
| Questions | 2.93 | 2.93 | 3.67 | 3.03 |
| Usefulness | 3.63 | 3.80 | 3.85 | 3.93 |

The judge is Sonnet 5.5, which here scores sheets from the same model: a self-preference risk. The blind human check (12 sheets, one reviewer who knew the key) shows the judge is **too lenient on accuracy**: 3.00 for the human against 3.58 for the judge on the same Haiku agent sheets. Exact agreement is 68.3 % (target 65 %), within one point 93.3 % (target 95 %, missed). On the reference-2 series: 71.7 % and 98.3 %. I did not run the AI judge or the human check on the validation set.

### Cost (measured from the account balance, per 30-brief run)

| Method | Cost per run | Per brief |
|---|---|---|
| Haiku agent | about 0.06 | about 0.002 |
| Haiku reference 2 | about 0.09 | about 0.003 |
| Sonnet agent | 1.38 | about 0.046 |
| Sonnet reference 2 | about 1.41 | about 0.047 |

Unit: Anthropic console balance. n8n does not expose tokens for the agent, so there is no per-token cost. The full validation run (four methods, 12 briefs) cost 1.05 in total (3.12 → 2.07).

## What the decision rule says

1. **Invented features**: tie at 0, with both models, on test and on validation.
2. **Status accuracy**: reference 2 is better or equal, with both models, on validation (100 vs 97.1 % for Sonnet, 88.6 vs 80.0 % for Haiku). On test with Sonnet, the agent is better if its 3 invalid outputs are set aside (95.7 vs 91.1 %) and worse if they count (84.8 %). I count them, because an empty sheet is a lost sheet.

The agent is not cheaper with Sonnet (1.38 vs 1.41). Published conclusion: **at this documentation size, the single prompt is enough and the agent adds nothing**.

## Which model

The rule picks the cheapest model that reaches every "target" threshold on validation. Haiku does not get there on status accuracy (88.6 % against the 90 % required): its place is "usable with careful review". **Sonnet 5.5 with the single prompt** reaches the target on every measure taken on validation: invented features, statuses, undocumented points, vague briefs, calculations, valid JSON. The Sonnet agent is at the acceptable level on calculations (on V06 it marks "150 quotes a month" as `couvert` although the 100-quote limit exists on Essentiel; it still recommends the Équipe plan, so the price is right).

"Accurate sources", "AI judge" and "human check" were measured on the test set only. The model recommendation therefore rests on the status measures. In every case the tool produces a sheet that a human reviews before anything is sent to the client.

## Limits and biases

- **Small samples.** 12 briefs and 35 statuses on validation: one status is worth 2.9 points. The gap between agent and reference 2 is one status with Sonnet (34 vs 35) and three with Haiku (28 vs 31). These are trends, not proof.
- **Declared asymmetry.** The agent prompt was improved over three versions on the test set; the reference-2 prompt stayed at its first version. That favours the agent on test. Validation, never seen during tuning, corrects that bias, and the agent does not win there.
- **Different thinking settings.** Haiku runs without thinking; Sonnet refuses to disable it and runs with adaptive thinking at low effort. The Haiku vs Sonnet comparison therefore mixes the model and this setting.
- **Judge not independent.** The AI judge is Sonnet 5.5 and is lenient on accuracy (see above). One human reviewer, who knew the key.
- **Sources.** The share of accurate sources (measure 6) was not checked passage by passage: only consistency with the key.
- **Synthetic data.** Corpus, briefs and key were written for the study. A real corpus has contradictions and outdated pages that this one lacks.
- **Thresholds.** They were frozen before the measures and did not move. A 90 % threshold on statuses is strict for 35 statuses.
- **A shared pattern on test.** Three statuses (T15, T17, T18) are wrong for several methods at once: they may come from the key ("partial" for a feature missing in its useful form) rather than from the models.

## What went wrong (error log, summarised)

- **Reference 2**: output limit of 1,024 then 4,000 tokens, truncated JSON (11 then 15 out of 30). Raised to 16,000: 0 invalid.
- **Haiku agent**: run 1, 29 briefs out of 30 in "Bad request" (Haiku thinks by default and n8n sends the thinking blocks back, which the API rejects). Runs 2 and 3, 30 briefs out of 30 "Max iterations (10) reached": n8n ran the 30 briefs as one batch and applied the limit to the whole batch. Fixed with a loop, one brief at a time. The failed runs cost about 0.64 for nothing.
- **Sonnet agent**: "does not support disabling thinking", fixed with adaptive thinking.
- **Validation launch**: the 4 runs were launched once each from n8n, with no rerun, and 12 valid sheets out of 12 for each.

## Reproduce

Everything is in the repository: documentation (`data/docs/`), briefs and keys (`data/`, `evaluation/cle_briefs_*.csv`), prompts (`prompts/`), n8n nodes and notes (`workflow/`), thresholds, freeze record, scoring logs and raw sheets (`evaluation/`). The n8n workflows use an Anthropic credential that you need to set up yourself.
