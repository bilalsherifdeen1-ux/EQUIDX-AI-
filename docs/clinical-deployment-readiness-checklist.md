# EQUIDX AI Clinical Deployment Readiness and Compliance Checklist

**Document status:** Working go/no-go checklist — not evidence of compliance, certification, regulatory clearance, or clinical safety.

**Repository:** `bilalsherifdeen1-ux/EQUIDX-AI-`

**Prepared:** 2026-09-26

## How to use this checklist

Complete this checklist against a defined product version, intended use, jurisdiction, deployment environment, and responsible legal entity. Each unchecked item is a release blocker unless a qualified regulatory, clinical, quality, privacy, or security owner documents an approved rationale and alternative control.

The words **must** and **required** refer to a legal or regulatory obligation only when the stated jurisdictional and product-scope conditions apply. Standards and guidance are not automatically law. Obtain qualified regulatory and privacy advice before using this checklist for a real deployment.

## Current repository disposition

- [x] The product and UI clearly identify the system as a research prototype using synthetic data and placeholder models.
- [x] The repository contains a research-use disclaimer stating that it is not a medical device and not for clinical use.
- [x] Core automated service tests pass locally: backend 10, AI engine 24, biosensor simulator 7, analytics 1, mobile API 1, and cross-domain tests 8.
- [x] The frontend passes ESLint, TypeScript checking, npm audit, and a production build on Next.js 16.3.6.
- [ ] Clinical deployment is **not approved**. The models are trained on synthetic data and have not been clinically validated, cleared, approved, or assessed under a medical-device quality system.
- [ ] Live Docker/Kubernetes deployment, database migrations, service-to-service networking, TLS, backups, restore, observability, and production failover have not been verified in this sandbox.
- [ ] Browser E2E tests remain skipped because Playwright and a running full stack were unavailable.
- [ ] No evidence package exists yet for intended use, regulatory classification, clinical validation, QMS, cybersecurity, privacy, usability, post-market surveillance, or release approval.

**Current go/no-go decision: NO-GO for real patient data, clinical decisions, diagnosis, treatment, or regulated commercial distribution.**

## 1. Intended use, claims, scope, and accountability

- [ ] Approve a controlled intended-use statement covering the condition(s), diagnostic purpose, patient population, specimen/device inputs, users, care setting, output, clinical role, autonomy, operating environment, and exclusions.
- [ ] Create an intended-use and claims matrix mapping every website statement, UI label, API field, report finding, confidence score, model output, and sales statement to an approved claim or explicitly prohibited claim.
- [ ] Define whether the output is informational, screening, diagnostic, triage, monitoring, treatment-support, or another clinical function. Do not let a “research prototype” label coexist with clinical claims.
- [ ] Identify the legal manufacturer, developer, deployer, importer, distributor, healthcare customer, data controller, processor, covered entity, and business associate roles for every target market.
- [ ] Define the supported users, required qualifications, training, supervision, and escalation path.
- [ ] Define the supported hardware, biosensor cartridges, operating systems, browsers, networks, cloud services, integrations, and data formats.
- [ ] Define foreseeable misuse, off-label use, unsupported inputs, missing/invalid readings, unavailable services, downtime, incorrect patient/specimen association, and human override behavior.
- [ ] Freeze the intended purpose before clinical evidence, classification, and conformity work. Assess every later claim or feature change through formal change control.
- [ ] Establish accountable owners for clinical safety, regulatory affairs, quality, privacy, cybersecurity, model risk, data governance, support, incident response, and final release approval.

## 2. Regulatory qualification and classification

### United States

- [ ] Determine whether each software function is a medical-device software function under the FD&C Act and document the reasoning.
- [ ] Assess the FDA clinical decision-support exclusion criteria individually. Do not assume that displaying information or supporting a clinician removes the function from FDA oversight. [1] [2]
- [ ] Select and document the applicable FDA pathway: exemption, 510(k), De Novo, PMA, HDE, or another applicable route.
- [ ] Confirm that intended use, labeling, architecture, clinical evidence, model behavior, cybersecurity controls, and post-market commitments match the authorized use.
- [ ] Determine whether the product is a “cyber device” under FD&C Act Section 524B. If so, prepare the required vulnerability/exploit monitoring and coordinated-disclosure plan, secure development and maintenance processes, patch/update process, and software bill of materials for a covered premarket submission. [3] [4]
- [ ] Determine establishment registration, device listing, UDI, labeling, complaint, correction/removal, and reporting obligations for the responsible entity.
- [ ] Confirm whether any third-party model, cloud, biosensor, or data provider creates additional regulatory or contractual obligations.

### European Union

- [ ] Determine whether the product is an MDR medical-device software function, an IVDR in-vitro diagnostic device/software function, an accessory/component, or out of scope.
- [ ] Document the device boundary and intended-purpose rationale. Cloud-hosted, mobile, or connected delivery does not by itself remove MDR/IVDR applicability.
- [ ] Apply and document the applicable classification rule. For MDR software, assess Annex VIII Rule 11. For IVDR software, assess the relevant Annex VIII rule and the exact diagnostic purpose. [5] [6] [7]
- [ ] Determine whether a notified body is required and select a notified body whose scope covers the product and intended use.
- [ ] Complete the applicable conformity-assessment route before placing the device on the market or putting it into service.
- [ ] Prepare the EU Declaration of Conformity, CE marking, notified-body number where required, UDI, EUDAMED/economic-operator registrations, and Member-State language requirements.
- [ ] For applicable Class C/D IVDs, complete additional performance, notified-body, reference-laboratory, companion-diagnostic, and Summary of Safety and Performance obligations as applicable.
- [ ] Assess the EU AI Act classification and obligations separately. Do not assume that MDR/IVDR conformity automatically resolves every AI Act obligation or transition-date issue. [8]

## 3. Quality management system and controlled lifecycle

- [ ] Establish a documented QMS appropriate to the product and markets. For US device manufacturers subject to QMSR, operate the applicable requirements of 21 CFR Part 820, including ISO 13485:2016 as incorporated by reference. [9] [10]
- [ ] Define document control, records control, training, competence, management review, internal audit, supplier control, nonconformance, CAPA, complaint handling, change control, and release approval procedures.
- [ ] Define design and development planning, inputs, outputs, reviews, verification, validation, transfer, maintenance, and retirement.
- [ ] Maintain traceability from user and regulatory needs through system requirements, software requirements, architecture, implementation, risk controls, tests, release configuration, labeling, and post-release changes.
- [ ] Control third-party, open-source, cloud, AI, data, biosensor, and infrastructure suppliers. Record versions, licenses, support status, security posture, quality agreements, and change notifications.
- [ ] Establish a controlled training record for developers, reviewers, clinicians, operators, support personnel, quality staff, and incident responders.
- [ ] Define objective release criteria, independent review requirements, segregation of duties, approval signatures, and retention periods.
- [ ] Establish a controlled design-history/technical-file structure for each released product and market.
- [ ] Do not treat ISO 13485 certification as a substitute for statutory compliance, regulatory authorization, or evidence of clinical safety.

## 4. Risk management and safety engineering

- [ ] Create an ISO 14971-aligned risk-management plan and risk-management file covering the full lifecycle, including decommissioning.
- [ ] Define objective risk acceptability criteria and benefit-risk decision rules.
- [ ] Identify hazards, hazardous situations, foreseeable misuse, severity, probability, detectability where used, risk controls, residual risk, and production/post-production feedback.
- [ ] Include risks from wrong patient/specimen matching, incorrect sample type, missing channels, unit conversion, bad calibration, sensor drift, stale data, duplicate reports, delayed results, unavailable downstream services, corrupted files, model failure, data leakage, bias, automation bias, UI misunderstanding, and false confidence.
- [ ] Include cybersecurity threats that could alter, suppress, delay, expose, or misroute a clinical result.
- [ ] Link every risk control to an approved requirement, implementation, verification test, validation evidence, labeling/training control, and residual-risk decision.
- [ ] Verify fail-safe behavior, invalid-result behavior, manual fallback, downtime behavior, rollback, emergency changes, and recovery after partial service failure.
- [ ] Review the risk file after every material model, data, workflow, infrastructure, integration, dependency, security, or intended-use change.

## 5. Software lifecycle, configuration, and release engineering

- [ ] Establish an IEC 62304-aligned software lifecycle covering planning, requirements, architecture, implementation, verification, release, maintenance, problem resolution, configuration management, and retirement. IEC 62304 does not itself replace final product validation or release approval. [11]
- [ ] Assign and justify software safety classification and the corresponding lifecycle rigor.
- [ ] Baseline requirements and architecture for each release.
- [ ] Maintain reproducible builds, pinned dependencies, source revision, compiler/runtime versions, model artifacts, training code, data versions, configuration, infrastructure manifests, and deployment image digests.
- [ ] Generate and retain an SBOM for every releasable service image and frontend artifact. Include commercial, open-source, and off-the-shelf components.
- [ ] Scan source, dependencies, containers, images, infrastructure-as-code, and runtime configuration on every release and on a defined schedule.
- [ ] Define vulnerability severity, remediation, exception, compensating-control, disclosure, and emergency-patch SLAs.
- [ ] Require signed commits or protected branches, code review, CI status checks, release tags, artifact signing, provenance, and deployment approvals.
- [ ] Add CI that runs backend, AI, simulator, analytics, mobile, cross-service, frontend lint, type checking, build, audit, SBOM, migration, and security checks.
- [ ] Replace skipped browser E2E tests with a controlled Playwright suite against an isolated full stack.
- [ ] Add live-stack integration tests covering authentication, RBAC, patient/sample/report lifecycle, AI-engine failure, simulator failure, database migration, retry/idempotency, and rollback.
- [ ] Add negative tests for unauthorized access, inactive users, cross-patient access, invalid readings, malformed uploads, oversized inputs, expired tokens, refresh-token misuse, and privilege changes.
- [ ] Define data retention and deletion behavior for logs, raw signals, reports, backups, exports, and temporary files.

## 6. Clinical and analytical validation

- [ ] Replace synthetic placeholder data/models with fit-for-purpose clinical data collected and used under documented permissions, contracts, ethics approvals, and privacy controls.
- [ ] Define the clinical reference standard, comparator, ground-truth process, adjudication, label quality, and disagreement handling.
- [ ] Build a clinical-evidence matrix linking every claim and output to scientific validity/clinical association, analytical/technical performance, and clinical performance evidence. [12]
- [ ] Predefine protocol, endpoints, acceptance criteria, sample-size/statistical rationale, missing-data rules, invalid-result rules, confidence intervals, and stopping rules.
- [ ] Keep training, tuning, validation, and test sets independent. Prevent patient, site, device, specimen, time, and acquisition leakage.
- [ ] Validate on the intended population, prevalence, care setting, specimen types, devices, operators, and workflow.
- [ ] Report clinically meaningful sensitivity, specificity, PPV, NPV, calibration, invalid/error rate, agreement, confidence intervals, and comparator performance as appropriate.
- [ ] Evaluate clinically important subgroups, including age, sex, race/ethnicity, geography, disease severity, comorbidity, pregnancy status where relevant, device/site, and socioeconomic or access-related factors.
- [ ] Evaluate false positives, false negatives, discordance, borderline values, out-of-distribution inputs, sensor noise, missing channels, and adversarial or corrupted inputs.
- [ ] Perform prospective, external, multi-site, or real-world validation proportionate to intended risk and claims.
- [ ] Validate the complete human-AI team and workflow, not only the model in isolation.
- [ ] Document limitations, uncertainty, generalizability boundaries, and conditions in which results must not be used.

## 7. Human factors, usability, and clinical workflow

- [ ] Establish a usability-engineering plan aligned to IEC 62366-1 and link use-related hazards to the risk file.
- [ ] Identify intended users, critical tasks, use environments, workflow dependencies, and foreseeable use errors.
- [ ] Test patient/specimen selection, barcode/MRN handling, sample-type selection, result review, report generation, invalid results, repeat testing, warnings, overrides, manual review, downtime, and escalation.
- [ ] Use representative users and realistic clinical environments for formative and summative evaluations.
- [ ] Test automation bias, alert fatigue, over-reliance on confidence scores, ambiguous flags, discordant findings, and confirmation bias.
- [ ] Ensure the UI clearly communicates intended use, limitations, uncertainty, invalid results, model/version, data source, review state, and required clinician action.
- [ ] Ensure no interface implies a diagnosis, treatment instruction, or clinical authorization beyond the approved intended use.
- [ ] Train and assess users before access to clinical workflows.
- [ ] Maintain controlled labeling, instructions for use, support procedures, training materials, and change notices.

## 8. Privacy and healthcare data protection

- [ ] Inventory all personal data, health data, genetic data, identifiers, biosensor signals, reports, logs, telemetry, exports, backups, support data, and third-party transfers.
- [ ] Determine controller/processor, covered-entity/business-associate, and subcontractor roles for each deployment.
- [ ] For GDPR scope, document an Article 6 lawful basis and Article 9 condition for health/genetic data; define purpose limitation, minimization, accuracy, retention, transparency, rights handling, and transfer safeguards. [13]
- [ ] Complete and approve a DPIA before processing likely to create high risk, including relevant large-scale health-data processing, systematic monitoring, or automated evaluation.
- [ ] Determine whether any output is solely automated decision-making with legal or similarly significant effects and implement applicable Article 22 safeguards where required.
- [ ] Put compliant processor, subprocessor, data-processing, confidentiality, security, deletion/return, assistance, and audit terms in place.
- [ ] For HIPAA scope, execute required business-associate agreements and perform a documented, accurate, thorough risk analysis and risk-management process. [14]
- [ ] Implement HIPAA administrative, physical, and technical safeguards, including unique user identification, authentication, role-based access, audit controls, integrity controls, transmission security, incident procedures, contingency planning, backups, and restore testing.
- [ ] Define consent/authorization, notice, access, correction, deletion/retention, export, restriction, and objection procedures as applicable.
- [ ] Apply privacy by design/default. Do not store real PHI in development, test, demo, analytics, logs, error reports, or support channels unless explicitly approved and protected.
- [ ] Define de-identification or pseudonymization methods, re-identification controls, key separation, and residual-risk assessment.
- [ ] Define breach detection, evidence preservation, notification, communications, and regulator/customer escalation timelines.

## 9. Cybersecurity and operational resilience

- [ ] Maintain a system/data-flow/asset inventory covering web, backend, AI engine, simulator, analytics, mobile API, database, Redis, object storage, observability, CI/CD, cloud, vendor, and support paths.
- [ ] Maintain a threat model covering authentication, authorization, tenant/patient isolation, APIs, uploads, GraphQL, service-to-service calls, model inputs/outputs, secrets, logs, backups, dependencies, containers, and update paths.
- [ ] Apply least privilege, strong authentication, MFA for administrative/high-risk access, short-lived privileged access, role review, and prompt deprovisioning.
- [ ] Replace development secrets and seeded demo credentials before any non-local deployment. Keep production secrets outside source control and rotate them.
- [ ] Enforce TLS for external and internal sensitive traffic; configure secure cookies, CSRF protections where cookie sessions are used, HSTS, secure headers, and a restrictive CORS policy.
- [ ] Encrypt data at rest and in transit with managed key rotation and separation of duties.
- [ ] Protect raw signals, reports, logs, backups, and exports from unauthorized read, alteration, deletion, and replay.
- [ ] Centralize tamper-resistant audit logs for authentication, privilege changes, patient-record access, exports, report creation/review, configuration, updates, and security events.
- [ ] Add rate limiting, brute-force protection, account lockout or equivalent controls, abuse monitoring, request-size limits, timeout/retry budgets, and idempotency controls.
- [ ] Apply container hardening, non-root execution, image provenance/signing, network isolation, secret injection, read-only filesystems where possible, and resource limits.
- [ ] Maintain vulnerability disclosure, triage, patch, emergency-response, and customer-notification procedures.
- [ ] Test backups and restoration. Define and approve RTO/RPO, downtime procedures, manual fallback, disaster recovery, regional failure, database corruption, and ransomware scenarios.
- [ ] Exercise incident response and clinical-safety escalation with the healthcare customer.
- [ ] Use NIST CSF 2.0 and/or NIST AI RMF to structure governance, identification, protection, detection, response, recovery, and AI risk management; these frameworks are voluntary and do not replace applicable law. [15] [16]

## 10. AI/model governance and monitoring

- [ ] Maintain a model inventory with model purpose, version, owner, training data, preprocessing, features, architecture, hyperparameters, thresholds, dependencies, limitations, and approval status.
- [ ] Record dataset provenance, permissions, inclusion/exclusion, demographics, label generation, quality checks, preprocessing, augmentation, leakage controls, and retention.
- [ ] Validate calibration, confidence semantics, uncertainty, abstention, out-of-distribution behavior, and invalid-output handling.
- [ ] Prohibit unreviewed online learning or silent retraining in clinical production.
- [ ] Define a predetermined change-control plan for model, data, threshold, feature, preprocessing, or output changes where applicable.
- [ ] Predefine monitoring thresholds for drift, calibration, subgroup degradation, false positives/negatives, invalid rates, overrides, near misses, downtime, latency, and cybersecurity events.
- [ ] Define alerting, investigation, quarantine, rollback, revalidation, CAPA, labeling, customer notification, and regulatory-reporting triggers.
- [ ] Provide users with appropriate information about intended use, training/test data, performance, limitations, uncertainty, update scope/timing, and the role of independent clinical judgment.
- [ ] Establish independent clinical and quality review of model changes and safety signals.

## 11. Post-market surveillance, complaints, and vigilance

- [ ] Establish complaint intake, categorization, investigation, escalation, evidence preservation, and closure procedures.
- [ ] Define reportability decision trees for FDA MDR, EU serious incidents, vigilance, field-safety corrective actions, GDPR breaches, HIPAA incidents, cybersecurity vulnerabilities, and clinical near misses.
- [ ] For FDA scope, assess 21 CFR Part 803 death, serious-injury, and reportable-malfunction obligations and retain required records. [17]
- [ ] For MDR/IVDR scope, operate PMS and vigilance processes, trend signals, update the risk file and clinical/performance evidence, and complete required reports, PSUR/PMS reports, and corrective actions.
- [ ] Maintain a post-market clinical/performance follow-up plan where applicable.
- [ ] Trend complaints, invalid results, delays, overrides, repeat tests, discordance, subgroup degradation, availability, security events, and support cases.
- [ ] Feed post-market findings into CAPA, risk management, labeling, training, validation, and controlled releases.
- [ ] Maintain regulator, notified-body, customer, DPO, security, and clinical escalation contacts and tested communications channels.

## 12. Deployment acceptance and release gate

Do not authorize clinical deployment until all applicable evidence is approved and the release package is complete:

- [ ] Intended-use, claims, jurisdictions, classification, and regulatory pathway approved.
- [ ] QMS procedures active; design, risk, software, usability, clinical/performance, privacy, cybersecurity, and supplier records complete.
- [ ] Regulatory authorization or conformity assessment complete, including notified-body and registration requirements where applicable.
- [ ] Clinical/performance validation meets prespecified acceptance criteria with subgroup and limitation analysis.
- [ ] Human-factors validation and user training complete.
- [ ] Security threat model, penetration/security testing, SBOM, vulnerability report, patch plan, incident response, and customer security documentation approved.
- [ ] Privacy assessment, DPIA, BAA/DPA, retention, deletion, access, transfer, and breach processes approved where applicable.
- [ ] Production infrastructure qualification, migrations, backups, restore, monitoring, alerting, access review, TLS, secrets, and disaster recovery tested.
- [ ] Model and data lineage, release manifest, reproducible artifact, deployment digest, rollback, and change-control record approved.
- [ ] Live-stack integration and browser E2E suites pass in a controlled environment.
- [ ] Complaints, vigilance, post-market, support, and clinical-safety escalation processes are staffed and tested.
- [ ] Final release decision signed by accountable quality, clinical, regulatory, security, privacy, and product owners.

## Repository-specific preclinical blockers

These items are specific to the current repository and must remain open until addressed:

- [ ] Replace all placeholder/synthetic diagnostic models with clinically validated models and real-world evidence appropriate to the claimed use.
- [ ] Establish the intended-use and regulatory classification before changing the product from research/demo labeling.
- [ ] Integrate the biosensor signal path into the production backend with verified persistence and auditability; the current `backend_wiring/` material is documented as reference wiring rather than a verified live-service integration.
- [ ] Add full-stack Docker/Kubernetes validation, migrations, TLS, secrets, backups, restore, service health, and failover tests.
- [ ] Add non-skipped Playwright browser tests and full live-stack integration tests to CI.
- [ ] Implement production-grade session/token storage, rotation/revocation, MFA/administrative controls, rate limiting, secure headers, and security monitoring before real data.
- [ ] Remove seeded demo credentials and development defaults from all non-local environments.
- [ ] Add SBOM generation, image/artifact signing, dependency/container scanning, vulnerability disclosure, and patch SLAs.
- [ ] Add formal model/data lineage, clinical validation, subgroup performance, calibration, drift, rollback, and post-market monitoring evidence.
- [ ] Complete privacy, HIPAA/GDPR, data-processing, retention, deletion, access, breach, and vendor assessments before any real PHI/ePHI is introduced.

## References

[1]: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/policy-device-software-functions-and-mobile-medical-applications "FDA Policy for Device Software Functions and Mobile Medical Applications"

[2]: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software "FDA Clinical Decision Support Software Guidance"

[3]: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-medical-devices-quality-management-system-considerations-and-content-premarket "FDA Cybersecurity in Medical Devices"

[4]: https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title21-section360n-2&num=0&edition=prelim "21 USC 360n-2, Ensuring Cybersecurity of Devices"

[5]: https://eur-lex.europa.eu/eli/reg/2017/745/oj/eng "Regulation (EU) 2017/745 on medical devices"

[6]: https://eur-lex.europa.eu/eli/reg/2017/746/oj/eng "Regulation (EU) 2017/746 on in vitro diagnostic medical devices"

[7]: https://health.ec.europa.eu/latest-updates/update-mdcg-2019-11-rev1-qualification-and-classification-software-regulation-eu-2017745-and-2025-06-17_en "MDCG 2019-11 rev.1 software qualification and classification"

[8]: https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng "Regulation (EU) 2024/1689, Artificial Intelligence Act"

[9]: https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-820 "21 CFR Part 820, Quality Management System Regulation"

[10]: https://www.fda.gov/medical-devices/postmarket-requirements-devices/quality-management-system-regulation-qmsr "FDA Quality Management System Regulation"

[11]: https://webstore.iec.ch/en/publication/6792 "IEC 62304 Medical device software — Software life cycle processes"

[12]: https://www.imdrf.org/sites/default/files/docs/imdrf/final/technical/imdrf-tech-170921-samd-n41-clinical-evaluation_1.pdf "IMDRF SaMD Clinical Evaluation"

[13]: https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng "Regulation (EU) 2016/679, General Data Protection Regulation"

[14]: https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html "HHS HIPAA Security Rule"

[15]: https://www.nist.gov/cyberframework "NIST Cybersecurity Framework 2.0"

[16]: https://www.nist.gov/itl/ai-risk-management-framework "NIST AI Risk Management Framework"

[17]: https://www.fda.gov/medical-devices/medical-device-safety/medical-device-reporting-mdr-how-report-medical-device-problems "FDA Medical Device Reporting"
