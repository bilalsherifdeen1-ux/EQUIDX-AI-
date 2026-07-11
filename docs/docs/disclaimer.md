# Disclaimer

**EQUIDX AI is a research and prototype software platform. It is not a
medical device.**

- No component of this system has been reviewed, cleared, or approved by
  the U.S. FDA, a notified body under the EU IVDR, or any other regulatory
  authority.
- All patient records, biosensor signals, and diagnostic outputs shipped
  with or produced by this repository are **synthetic** — generated
  procedurally (see `ai-engine/ai_engine/datasets/synthetic_data_generator.py`
  and `backend/app/infrastructure/db/seed.py`) and carry no relationship to
  real individuals.
- Every AI model in `ai-engine/` is explicitly a **placeholder**: simple
  classical ML / small neural-network models trained on synthetic data to
  demonstrate the shape of a real diagnostic-AI pipeline (preprocessing,
  training, inference, evaluation), not to produce clinically valid output.
- Nothing produced by EQUIDX AI — including any "diagnostic report," risk
  band, flag, or confidence score — may be used to diagnose, treat, or make
  real clinical decisions about a real person.
- The clinical decision-support interface in the dashboard is explicitly
  labeled "Research Prototype" throughout the product for this reason.

If you are experiencing a medical concern, please consult a licensed
healthcare professional. If this is a medical emergency, contact your
local emergency services.

## For contributors and deployers

If you fork this repository to build toward an actual clinical product,
you are responsible for:

- Replacing all placeholder models with validated, clinically tested
  models developed under an appropriate quality system (e.g. ISO 13485).
- Pursuing the relevant regulatory pathway (e.g. FDA 510(k)/De Novo/PMA,
  EU IVDR conformity assessment) before any clinical use.
- Independent clinical validation studies appropriate to your intended use.
- Full compliance with applicable data protection and health-information
  regulations (e.g. HIPAA, GDPR) if real patient data is ever introduced.

None of the above is included in or implied by this repository.
