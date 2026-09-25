# EQUIDX AI — ai-engine rebuild: sourced data + critical inference fix

Drop this `ai_engine/` folder into your repo at `ai-engine/ai_engine/`,
overwriting the existing files. Six files changed.

## 1. Critical bug fix — every prediction was ignoring its input

`ai_engine/preprocessing/signal_preprocessing.py` — `normalize()` used to
z-score a batch against *its own* mean/std. Since every real inference
call (`predict()`) passes exactly one row, that row's "mean" was always
itself, so every feature collapsed to `(x - x) / 1 = 0` — **every single
prediction the AI engine ever served was scored on an all-zero input**,
regardless of the actual sample values. This affected all five domains,
in both the original code and my first pass at the rebuild below — I only
caught it while testing the fix in item 2.

Fix: preprocessing is now stateful (`FittedScaler` — fit once on training
data in `train()`, reused via `self.scaler` at inference). Verified: a
model now gives *different* predictions for different single-row inputs,
and correctly classifies previously-mis-scored rows. See the "Verification"
section below for the actual test output.

**This fix alone is arguably more important than everything below it** —
without it, nothing else in this rebuild (or in the original repo) was
ever actually working at inference time.

## 2. Sourced synthetic data + real cross-feature interactions

`ai_engine/datasets/synthetic_data_generator.py` — every distribution
parameter and decision threshold is now cited to a specific reference
(NBME/MedlinePlus reference ranges, ADA diagnostic criteria, NAIIS 2018
Nigeria HIV prevalence, Payne 1973 corrected-calcium formula, Yang et al.
2015 UPCR). Full citations are in the module and per-function docstrings.

Two domains now have a genuine multivariate interaction term instead of
independent per-feature thresholds joined by OR:

- **Blood chemistry**: adds `bun_creatinine_ratio`. A ratio > 20:1 flags a
  pre-renal pattern even when creatinine and BUN are each individually
  in their own reference range.
- **Urinalysis**: adds `urine_creatinine_mg_dl` and `upcr_mg_g` (urine
  protein:creatinine ratio). UPCR > 200 mg/g flags proteinuria even when
  raw protein, glucose, and WBC are each individually normal.

Metabolic panel adds `corrected_calcium_mg_dl` (Payne formula,
albumin-corrected). HbA1c and HIV screening are updated only for the
stateful-scaler fix and citation comments — their existing structure
(eAG formula; overlapping-distribution classification for a low-prevalence
screen) was already legitimate.

## 3. Recall (sensitivity) added to every domain's evaluate()

Previously only accuracy/F1/ROC-AUC were reported — none of which
directly answer "how many real cases did we miss," which is the metric
that matters given screening tests should weight false negatives higher
than false positives. `recall_sensitivity` is now in every domain's
metrics dict.

## Verification (what I actually ran, not just claimed)

```
=== Blood chemistry ===
Rows where all 4 raw values (Na, K, Cr, BUN) are individually in-range: 2782 / 5000
Of those, flagged positive by the ratio alone: 169
Correctly flagged via single-row predict() (the real inference path): 49 / 50 sampled
evaluate(): {'accuracy': 0.998, 'f1': 0.9956, 'recall_sensitivity': 0.9913, 'roc_auc': 0.9956}

=== Urinalysis ===
Rows where protein/glucose/WBC are individually in-range: 4802 / 5000
Of those, flagged positive by UPCR alone: 440
Correctly flagged via single-row predict(): 50 / 50 sampled
evaluate(): {'accuracy': 1.0, 'f1': 1.0, 'recall_sensitivity': 1.0, 'roc_auc': 1.0}
```

Example single-row inference (the exact case that used to fail before the
scaler fix):
```
Input:  Na=142.4  K=4.34  Cr=0.70  BUN=14.47  ratio=20.77
        (all four raw values individually within reference range)
Output: flag = "prerenal_pattern_ratio_only", confidence = 1.0
```

## What did NOT change

`hba1c/model.py` and `hiv_screening/model.py` keep their original feature
sets (eAG formula was already correctly sourced; OD-ratio classification
was already the one legitimately non-threshold-reducible domain) — only
the scaler fix and citation comments were added.

## Honest caveat, unchanged from the rest of this conversation

This is still 100% synthetic, procedurally generated data — sourcing the
*parameters* to real reference ranges does not make the *rows* real
patient data, and none of this is clinically validated. See
`docs/docs/disclaimer.md` in the main repo.
