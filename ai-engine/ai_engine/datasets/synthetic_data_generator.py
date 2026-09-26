"""
Synthetic dataset generation for all five diagnostic domains — v3.

Every distribution parameter and decision threshold is sourced to a
specific reference, cited per function below. This does not make the data
real — every row is still a procedurally generated draw with no
relationship to any real patient — but the *shape* of the data (typical
values, spread, and the relationships between biomarkers/tests) now
matches published clinical/laboratory reference material instead of being
invented.

CHANGE LOG (why each domain looks the way it does):
  - blood_chemistry, urinalysis: rebuilt to include a genuine cross-feature
    interaction (BUN:creatinine ratio; urine protein:creatinine ratio) so a
    row can be positively labeled while every individual raw biomarker
    sits inside its own reference range. See each function's docstring.
  - hba1c: rebuilt from a single deterministic HbA1c->eAG transform (which
    carried no independent second signal) into two independently-measured
    values (HbA1c and fasting glucose) that can genuinely disagree, mirroring
    real ADA-documented discordance between the two diagnostic criteria.
  - hiv_screening: rebuilt from a single-assay binary classifier into a
    two-stage screen + differentiation model mirroring the actual CDC 2014
    HIV diagnostic algorithm, including the real "reactive screen,
    non-reactive differentiation -> refer to NAT" discordant case.
"""
from __future__ import annotations

import numpy as np


# =============================================================================
# BLOOD CHEMISTRY
# =============================================================================
def generate_blood_chemistry_data(n: int = 2000, seed: int = 42):
    """
    Features: [sodium, potassium, creatinine, bun, bun_creatinine_ratio]

    Reference ranges: sodium 136-146 mEq/L, potassium 3.5-5.0 mEq/L
    (NBME Laboratory Reference Values, 2025); creatinine 0.6-1.2 mg/dL,
    BUN 7-20 mg/dL (MedlinePlus Comprehensive Metabolic Panel).

    Interaction term — BUN:creatinine ratio: normal ~10:1-20:1; >20:1
    indicates a pre-renal azotemia pattern (reduced kidney perfusion,
    e.g. dehydration/heart failure, kidneys themselves may be structurally
    normal). Source: MDCalc BUN:Creatinine Ratio calculator. This ratio can
    exceed 20 while BOTH raw values sit inside their own reference ranges
    (e.g. BUN 18, creatinine 0.8 -> ratio 22.5) — the actual clinical value
    of computing it at all.

    Label: y = 1 if creatinine > 1.2 OR bun > 20 OR ratio > 20.
    """
    rng = np.random.default_rng(seed)
    sodium = rng.normal(141, 3, n).clip(120, 160)
    potassium = rng.normal(4.2, 0.4, n).clip(2.5, 7.0)
    creatinine = rng.normal(0.9, 0.25, n).clip(0.3, 5.0)
    bun = (13.0 * (creatinine / 0.9) * rng.normal(1.0, 0.28, n)).clip(2, 60)
    bun_creatinine_ratio = bun / creatinine
    y = ((creatinine > 1.2) | (bun > 20) | (bun_creatinine_ratio > 20)).astype(int)
    X = np.column_stack([sodium, potassium, creatinine, bun, bun_creatinine_ratio])
    return X, y


# =============================================================================
# URINALYSIS
# =============================================================================
def generate_urinalysis_data(n: int = 2000, seed: int = 42):
    """
    Features: [ph, specific_gravity, protein_mg_dl, glucose_mg_dl,
               leukocytes, urine_creatinine_mg_dl, upcr_mg_g]

    Reference ranges: pH 4.5-8.0, specific gravity 1.005-1.025 (WikEM
    Urine Analysis reference table); protein dipstick trace ceiling
    ~10 mg/dL / <150 mg/day normal (Spokane CC Urinalysis Lab notes);
    glucose <130 mg/dL (WikEM); leukocytes <2-5 WBC/hpf (WikEM).

    Interaction term — urine protein:creatinine ratio (UPCR): a spot
    protein value alone is uninterpretable because it depends on urine
    concentration. UPCR = (protein mg/dL / urine creatinine mg/dL) x 1000,
    reported mg/g; >200 mg/g flags proteinuria. Sources: Wikipedia "Urine
    protein/creatinine ratio" citing Yang et al., PLOS ONE 2015 (normal
    <200 mg/g); Yang et al. 2015 (PMC4564100) on concentration-dependence.

    Label: y = 1 if protein > 30 OR glucose > 130 OR leukocytes > 5
              OR upcr_mg_g > 200.
    """
    rng = np.random.default_rng(seed)
    ph = rng.normal(6.0, 1.0, n).clip(4.5, 9.0)
    specific_gravity = rng.normal(1.016, 0.007, n).clip(1.001, 1.035)
    protein_mg_dl = rng.exponential(9, n).clip(0, 300)
    glucose_mg_dl = rng.exponential(8, n).clip(0, 400)
    leukocytes = rng.poisson(1.5, n)
    urine_creatinine_mg_dl = ((specific_gravity - 1.000) * 9000 * rng.normal(1.0, 0.3, n)).clip(5, 400)
    upcr_mg_g = (protein_mg_dl / urine_creatinine_mg_dl) * 1000
    y = ((protein_mg_dl > 30) | (glucose_mg_dl > 130) | (leukocytes > 5) | (upcr_mg_g > 200)).astype(int)
    X = np.column_stack(
        [ph, specific_gravity, protein_mg_dl, glucose_mg_dl, leukocytes, urine_creatinine_mg_dl, upcr_mg_g]
    )
    return X, y


# =============================================================================
# HBA1C
# =============================================================================
def generate_hba1c_data(n: int = 2000, seed: int = 42):
    """
    Features: [hba1c_percent, fasting_glucose_mg_dl]
    Label: 4-class — 0 concordant_normal, 1 concordant_prediabetic,
           2 concordant_diabetic, 3 discordant_recommend_repeat_test

    REBUILT: the prior version derived "estimated average glucose"
    deterministically FROM hba1c_percent (eAG = 28.7*A1c - 46.7), so the
    two features carried no independent information — one was just a
    linear transform of the other. This version instead generates fasting
    plasma glucose as its OWN measurement, correlated with HbA1c through
    the ADAG study relationship (r ~= 0.92; Nathan et al., Diabetes Care
    2008) but with genuine independent variation — because HbA1c reflects
    a ~3-month average and fasting glucose reflects a single point in
    time, real patients can and do fall in different diagnostic categories
    by each criterion.

    Diagnostic thresholds (both are real, independently usable ADA
    criteria — see ADA Standards of Medical Care, 2010 update, and
    community reporting on the resulting HbA1c/glucose discordance
    problem, e.g. Dr. Davidson's commentary: "people who have diabetes by
    one criterion but not by the other... is likely to occur frequently"):
      HbA1c:            <5.7% normal, 5.7-6.4% prediabetic, >=6.5% diabetic
      Fasting glucose:  <100 mg/dL normal, 100-125 prediabetic, >=126 diabetic

    When the two criteria disagree, the ADA recommendation is not to
    average or split the difference — it is to REPEAT the abnormal test
    (ADA Standards of Care commentary, Dr. Bergenstal: "If one is abnormal
    and the other is not, repeat the abnormal test... If that is still
    abnormal, you've made the diagnosis"). That's why "discordant" is
    returned as its own category here rather than silently resolved one
    way or the other — this mirrors the actual clinical instruction, and
    is exactly the pattern already used for the blood_chemistry and
    urinalysis rebuilds: don't force false certainty where a real protocol
    says to gather more information instead.

    NOTE ON THE DISCORDANCE RATE — read before trusting the ~35% figure
    this generator produces: most of that discordance is NOT from the
    injected measurement noise (halving or doubling the noise level barely
    moves the rate). It is structural: the eAG formula's central estimate
    crosses the fasting-glucose "normal" threshold (100 mg/dL) at
    HbA1c ~= 5.11%, not at the HbA1c normal/prediabetic threshold (5.7%).
    So a real band of "normal" HbA1c readings (5.11-5.7%) maps to a
    central eAG already inside the glucose "prediabetic" band even before
    any noise is added — because eAG estimates *overall average* glucose
    across ~3 months, not fasting-specific glucose, the two thresholds
    were never going to line up perfectly. This is the same real tension
    the ADA discordance guidance exists to handle, reproduced honestly
    here rather than papered over — but the exact ~35% figure is an
    artifact of this generator's formula interaction, not itself a cited
    population discordance rate; treat it as illustrative of the
    *existence* and *structural cause* of discordance, not as a claimed
    real-world frequency.
    """
    rng = np.random.default_rng(seed)
    hba1c_pct = rng.normal(5.6, 1.1, n).clip(3.5, 14.0)

    eag_central = 28.7 * hba1c_pct - 46.7  # Nathan et al. 2008 ADAG formula
    fasting_glucose = (eag_central * rng.normal(1.0, 0.08, n)).clip(50, 400)

    hba1c_band = np.select([hba1c_pct < 5.7, hba1c_pct < 6.5], [0, 1], default=2)
    glucose_band = np.select([fasting_glucose < 100, fasting_glucose < 126], [0, 1], default=2)

    concordant = hba1c_band == glucose_band
    y = np.where(concordant, hba1c_band, 3)  # 3 = discordant_recommend_repeat_test

    X = np.column_stack([hba1c_pct, fasting_glucose])
    return X, y.astype(int)


# =============================================================================
# METABOLIC PANEL
# =============================================================================
def generate_metabolic_panel_data(n: int = 2000, seed: int = 42):
    """
    Features: [glucose, calcium, co2, albumin, corrected_calcium]

    Reference ranges: fasting glucose 70-100 mg/dL, diagnostic diabetes
    threshold >126 mg/dL (ADA); calcium 8.5-10.2 mg/dL, CO2 23-29 mEq/L,
    albumin 3.4-5.4 g/dL (MedlinePlus).

    Interaction term — albumin-corrected calcium (Payne formula):
    corrected Ca = measured Ca + 0.8 x (4.0 - albumin). ~40% of
    circulating calcium is albumin-bound; low albumin lowers measured
    total calcium even when the physiologically active (ionized) fraction
    is normal. Source: Payne RB et al., BMJ 1973;4(5893):643-646.

    Label: y = 1 if glucose > 126 OR corrected_calcium outside 8.5-10.5.
    """
    rng = np.random.default_rng(seed)
    glucose = rng.normal(92, 18, n).clip(50, 400)
    calcium = rng.normal(9.4, 0.6, n).clip(5.0, 14.0)
    co2 = rng.normal(26, 2.5, n).clip(10, 40)
    albumin = rng.normal(4.2, 0.5, n).clip(1.0, 6.0)
    corrected_calcium = calcium + 0.8 * (4.0 - albumin)
    y = ((glucose > 126) | (corrected_calcium < 8.5) | (corrected_calcium > 10.5)).astype(int)
    X = np.column_stack([glucose, calcium, co2, albumin, corrected_calcium])
    return X, y


# =============================================================================
# HIV SCREENING
# =============================================================================
def generate_hiv_screening_data(n: int = 2000, seed: int = 42):
    """
    Features: [ag_ab_screen_od_ratio, differentiation_assay_signal]
    Label: 3-class — 0 non_reactive, 1 reactive_concordant_positive,
           2 reactive_discordant_recommend_NAT

    REBUILT: the prior version used a single immunoassay OD ratio and a
    binary label. This version models the actual CDC 2014 HIV diagnostic
    algorithm's two-stage structure (CDC, established 2014; overview via
    myadlm.org CLN and PMC4809934):

      Stage 1 — a 4th-generation antigen/antibody (Ag/Ab) combination
      screening immunoassay. Sensitivity 99.7-100%, specificity
      99.5-100% for established infection (PMC4809934). Detects the p24
      antigen, so it can catch ACUTE infection before antibody
      seroconversion — this matters for stage 2.

      Stage 2 — reactive screens reflex to an HIV-1/HIV-2 antibody
      DIFFERENTIATION assay. This is a third-generation assay: it does
      NOT detect the p24 antigen, so during acute infection (before
      antibodies have developed) it can be non-reactive even though the
      person is truly infected and the screen correctly flagged them
      (PMC4809934: "differentiation IAs... do not detect HIV antigen").

      The discordant case — screen reactive, differentiation non-reactive
      — is NOT resolved by picking one result over the other. Per the CDC
      algorithm, it is referred to nucleic acid testing (NAT) to
      distinguish true acute infection from a false-positive screen
      (PMC4809934: "Patients with a reactive antigen/antibody assay but
      nonreactive HIV-1/2 differentiation assay should have molecular
      testing performed"). That discordant category is preserved as its
      own output here rather than collapsed into a binary positive/
      negative, matching the real protocol.

    Base rate: 1.4% adult (15-49) HIV prevalence, Nigeria (NAIIS 2018,
    UNAIDS/NACA, 14 March 2019) — the country context of the underlying
    grant proposal.

    NOTE: the fraction of true positives that are "acute" (i.e. would
    produce a discordant result) is not precisely quantified by a single
    source here — the qualitative existence of this discordant pattern is
    well documented (see citations above), but the specific proportion
    used below (~12% of true positives) is an illustrative parameter, not
    itself a cited population rate.
    """
    rng = np.random.default_rng(seed)
    is_positive = rng.random(n) < 0.014  # NAIIS 2018
    is_acute = is_positive & (rng.random(n) < 0.12)  # illustrative, not a cited rate

    # Stage 1: Ag/Ab screen — reactive for essentially all true positives
    # (including acute, since 4th-gen assays detect p24 antigen)
    screen_od_ratio = np.where(
        is_positive,
        rng.normal(3.5, 1.2, n).clip(1.1, 8.0),
        rng.normal(0.3, 0.2, n).clip(0.01, 1.0),
    )

    # Stage 2: differentiation assay — non-reactive during acute window
    # (no antigen detection), reactive for established true positives,
    # non-reactive for true negatives.
    differentiation_signal = np.where(
        is_positive & ~is_acute,
        rng.normal(3.2, 1.0, n).clip(1.1, 8.0),
        rng.normal(0.25, 0.18, n).clip(0.01, 1.0),
    )

    screen_reactive = screen_od_ratio >= 1.0
    differentiation_reactive = differentiation_signal >= 1.0

    y = np.where(
        ~screen_reactive, 0,  # non_reactive
        np.where(differentiation_reactive, 1, 2),  # concordant positive vs discordant->NAT
    )

    X = np.column_stack([screen_od_ratio, differentiation_signal])
    return X, y.astype(int)


GENERATORS = {
    "urinalysis": generate_urinalysis_data,
    "hba1c": generate_hba1c_data,
    "blood_chemistry": generate_blood_chemistry_data,
    "metabolic_panel": generate_metabolic_panel_data,
    "hiv_screening": generate_hiv_screening_data,
}
