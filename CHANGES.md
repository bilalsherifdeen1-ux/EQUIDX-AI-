# CHANGES — HbA1c/HIV rigor pass + biosensor simulator wiring

This picks up from the earlier delivered `equidx-ai-engine-rebuild.zip`
(blood_chemistry, urinalysis, metabolic_panel + the FittedScaler bug fix).
Two things happened in this pass, both requested together: "we are doing
both."

## Part 1 — HbA1c and HIV screening brought to the same rigor

Both domains previously carried a real gap the other three didn't:

**HbA1c** derived "estimated average glucose" *deterministically* from
HbA1c via the eAG formula — the two numbers were never independent, so
there was no real second signal, just one value transformed twice.
Rebuilt to generate fasting glucose as its own measurement (correlated
through the ADAG study relationship, r≈0.92, but with genuine independent
variation), producing a real 4-class output: concordant-normal,
concordant-prediabetic, concordant-diabetic, or **discordant — recommend
repeat test**, matching the actual ADA protocol for when the two
diagnostic criteria disagree (repeat the abnormal one — not average or
pick one, per ADA Standards of Care commentary).

Worth knowing: the ~35% discordance rate this generator produces is
**mostly structural, not noise-driven** — halving/doubling the injected
noise barely moves it. The eAG formula's central estimate crosses the
100 mg/dL fasting-glucose threshold at HbA1c≈5.11%, not at HbA1c's own
5.7% threshold, so a real band of "normal" HbA1c readings maps to
"prediabetic" glucose even before noise. This is documented in the
generator's docstring rather than tuned away, because it's the same real
tension the ADA guidance exists to handle — but the exact 35% figure is
an artifact of this generator, not a cited population rate.

**HIV screening** used a single immunoassay value and a binary label.
Rebuilt to a genuine two-stage model mirroring the real CDC 2014 HIV
testing algorithm: a 4th-gen Ag/Ab screen, reflexing to an antibody
differentiation assay. Output is now 3-class: non-reactive,
reactive-concordant, or **reactive but differentiation non-reactive →
refer to NAT** — the real, sourced discordant case (differentiation
assays don't detect the p24 antigen, so they can be non-reactive during
acute infection despite a correctly-reactive screen). Nigeria prevalence
updated to 1.4% (NAIIS 2018) from an earlier 3% placeholder.

Full citations are in each function's docstring in
`ai_engine/datasets/synthetic_data_generator.py`.

**Verified:** HbA1c end-to-end (data generation → FittedScaler → XGBoost
→ correct `discordant_recommend_repeat_test` output on a genuinely
discordant draw). HIV's data generation and FittedScaler logic verified
directly — I could not run the PyTorch model itself in this sandbox (see
Known Limitation below); the fix is the identical `FittedScaler` pattern
already proven correct on the other four domains.

## Part 2 — Biosensor simulator wired into real inference

This was the previously-flagged gap: `/api/v1/infer` always sampled a
fresh synthetic row internally, regardless of what sample was actually
being scored. The simulator and the AI engine were never connected.

**`biosensor-simulator/simulator/device_profiles.py`** — rebuilt from one
generic waveform per sample_type to one channel per RAW biomarker each
model actually consumes (e.g. blood_chemistry gets separate sodium,
potassium, creatinine, BUN channels — matching a real cartridge's
separate electrodes).

**Architectural trade-off, made explicit rather than hidden:** biosensor-
simulator and ai-engine are separate services with no shared code — that
separation is the point of splitting them. But the interaction terms this
whole rebuild is built around (BUN tracking creatinine, urine creatinine
tracking specific gravity) reflect one patient's physiology, and the
simulator has no access to ai-engine's generator to get that correlation
"for free." So `device_profiles.py` and `signal_generator.py` carry a
small, explicitly-documented duplicate of the same correlation formulas
used in `synthetic_data_generator.py`. If those formulas change on the
ai-engine side, this file needs a matching update — flagged in both
files' docstrings so it isn't silently missed. This is a real limitation
of the microservice split, not an oversight.

**`ai_engine/preprocessing/feature_extraction.py`** (new) — takes the
simulator's raw per-channel readings and computes the same derived
features (BUN:creatinine ratio, UPCR, corrected calcium) that training
used, so train-time and serve-time feature engineering can't drift apart.

**`ai_engine/pipeline.py` / `serve.py`** — `/api/v1/infer` now accepts a
`readings` field (raw channel values). When given, it's the actual signal
scored, routed through feature_extraction. When omitted, it falls back to
synthetic sampling (documented as a fallback, not the default) — the
response's new `used_real_readings` field tells the caller honestly which
path was taken.

**`biosensor-simulator/simulator/main.py`** — new `POST /api/v1/panel`
endpoint returning both the raw waveforms and the extracted readings.

**`backend_wiring/`** — `report_service.py` and `ai_engine_client.py`
showing the concrete wiring: fetch a panel, forward its readings to
ai-engine, store the raw readings alongside the report as an audit trail.
These are provided as reference implementations, not verified against the
live backend service — see Known Limitations.

**Verified end-to-end**, in-process, for blood_chemistry, urinalysis,
hba1c, and metabolic_panel: simulator generates a correlated multi-
channel panel → readings extracted → real trained model scores them →
correct findings, including a genuine urinalysis UPCR-only proteinuria
flag and a genuine HbA1c/glucose discordant flag, both arising from
actual simulated signal, not from replaying training data. Also verified
the simulator's FastAPI HTTP layer directly (`/health`, `/api/v1/panel`,
error handling on an unknown sample_type).

## Known limitations of this delivery

1. **PyTorch (hiv_screening) could not run in this sandbox** — disk
   constraints and a corrupted partial torch install blocked it. The
   `FittedScaler` fix and the data-generation logic were verified
   directly and are structurally identical to the four domains that did
   run; but the actual neural net forward pass on real vs. synthetic
   `readings` has not been executed. Run
   `tests/test_combination_flags.py::test_hiv_single_row_predict_not_zeroed`
   and a manual `run_inference("hiv_screening", readings=...)` call in
   your own environment (where `requirements.txt` already pins `torch`)
   to close this out.
2. **`backend_wiring/` is not a verified diff against the live backend**
   — the original `report_service.py`/`ai_engine_client.py` only exist in
   the earlier Phase 1 `equidx-ai.zip`, which this sandbox does not have
   (sandbox reset mid-project). These files show the correct wiring
   pattern and match the existing Clean Architecture layering, but you'll
   need to merge them into your actual `backend/app/` tree and adjust
   import paths / `settings` fields (`AI_ENGINE_BASE_URL`,
   `BIOSENSOR_SIMULATOR_BASE_URL`) to match what's really there.
3. **`analytics/`, `mobile-api/`, `web/`, `infrastructure/`, `docs/`** —
   untouched in this pass, same as the previous rebuild.
