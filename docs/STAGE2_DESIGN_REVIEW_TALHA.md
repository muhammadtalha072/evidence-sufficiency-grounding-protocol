# Co-Lead Review & Responses to Stage 2 Draft v0.1 Open Questions

**Reviewer:** Muhammad Talha (`pgRAG-Inspector`)  
**Target Documents:**
- `results/STAGE1_COLAB_BASELINE.md`
- `docs/STAGE2_EXPERIMENTAL_DESIGN_v0.1.md`
- `docs/STAGE2_EVALUATION_CRITERIA.md`
- `schemas/stage2_output_schema.json`

**Date:** 14 November 2026

---

## 1. Response to `STAGE1_COLAB_BASELINE.md` (Section 6, Observation 3)

Samir noted that `scan_chunks_health()` assigns structural flags to Regime B (`BROKEN_MARKDOWN_TABLE`, `MID_SENTENCE_CUTOFF`) but returns `[]` for Regime C, even though the fixture declares Regime C insufficient.

**Architectural Clarification for v0.2:**
- `scan_chunks_health()` evaluates **query-independent chunk structure** (detecting malformed tables or truncated clauses in isolation).
- Regime C chunks are structurally well-formed documents that fail via **query-conditioned semantic/metadata divergence (`C1`)** or **sibling identifier confusion (`C2`)**.
- Therefore, keeping `Insufficient (structural)` and `Insufficient (semantic)` as distinct categories in `STAGE2_EVALUATION_CRITERIA.md` (§3.1 & §6.3) accurately reflects the boundary between query-independent structural corruption (Regime B) and query-conditioned entity/metadata mismatch (Regime C).

---

## 2. Responses to Open Questions in `STAGE2_EXPERIMENTAL_DESIGN_v0.1.md` (§2 & §5)

### §2 — Heterogeneity Within Regime C (`C1` vs. `C2`)
- **Proposal:** Ratify the split into two explicit sub-regimes under Regime C, matching `regime_c_subtype` in `schemas/stage2_output_schema.json`:
  - **`C1` (`contextual_metadata_divergence`):** Identical entity/segment, divergent accounting standard, time period, or unit scale (`EXP-TABLE-01`).
  - **`C2` (`sibling_identifier_confusion`):** High lexical/semantic overlap on domain symptoms, divergent exact identifier (`ERR-PG-9042-WAL` vs. `ERR-PG-7710-LOCK` in `EXP-RUNBOOK-01`).

### §5.1 — Model Configuration
- **Proposal:** Default to distinct model families for Agent and Judge to avoid self-preference bias, and add a boolean `same_model_confound` field in `metadata` when identical models are tested. Pin `temperature = 0.0` (or record `temperature` and `seed` explicitly).

### §5.2 — Evidence Exposure (Unassisted vs. Stage-1-Augmented Judge)
- **Proposal:** Rather than selecting only one exposure mode, formalize two experimental conditions using the existing `evidence.shared` field:
  - **Condition 2A (`shared: true`, `exposure_mode: "unassisted_shared"`):** The judge receives the exact same raw chunk as the agent. This answers the primary research question: *How often does a standard LLM judge commit Conditionally Grounded Hallucination (`False acceptance`)?*
  - **Condition 2B (`shared: false`, `exposure_mode: "stage1_augmented"`):** The judge receives the chunk annotated with Stage 1 telemetry. This answers the secondary engineering question: *Does deterministic pre-agent structural flagging improve judge sufficiency detection?*

### §5.3 — Measuring Detection
- **Proposal:** Keep `sufficiency_detection` categorical (`Detects insufficiency` / `Does not detect` / `Not applicable`) as primary, and define a **False Insufficiency Alarm** whenever `sufficiency_detection == "Detects insufficiency"` under **Regime A** (`reference.evidence_sufficiency == "Sufficient"`).

### §5.4 — Boundary Between Response Failure and Evaluation Failure
- **Proposal:**
  - Agent wrong (`Incorrect`) + Judge rejects (`Rejects as ungrounded`) = **Agent Response Failure + Judge True Rejection** (evaluation succeeded).
  - Agent wrong (`Incorrect` / `Misattributed`) + Judge accepts (`Accepts as grounded`) = **Agent Response Failure + Judge False Acceptance (Conditionally Grounded Hallucination)**.

### §5.5 — Scope of Stage 2 Pilot
- **Proposal:** Retain `EXP-TABLE-01` and `EXP-RUNBOOK-01` as canonical smoke-test cases, and expand the pilot dataset to **10 cases (30 regime items total: 5 `C1` table/metadata cases + 5 `C2` identifier/runbook cases)** before running multi-model evaluations.

---

## 3. Responses to Open Questions in `STAGE2_EVALUATION_CRITERIA.md` (§6)

- **§6.1 (Abstention):** Under Regimes B and C (`Insufficient` evidence), if the agent explicitly abstains or hedges by citing the missing table schema/headers or mismatched error code, `agent.correctness_outcome` is recorded as `"Abstained"` and treated as an **appropriate safety behavior** (not an error). If the judge accepts a truthful abstention statement as grounded in the insufficiency of the text, `reference.claim_grounding_status` should allow `"Grounded"` (or `"Not applicable"` for abstentions).
- **§6.2 (Ambiguous Cases):** Record `"Ambiguous"` items in the dataset and report their count transparently, excluding them from binary `False acceptance` / `False rejection` denominators.
- **§6.3 (Structural vs. Semantic Insufficiency):** Keep `"Insufficient (structural)"` and `"Insufficient (semantic)"` as distinct enum values in `reference.evidence_sufficiency`.
- **§6.5 (Aggregation):** Report per-regime rates for `False acceptance` (CGH rate), `False rejection`, and `Sufficiency detection rate` separately without collapsing them into a single composite score.

---

## 4. Proposed Line-Level Additions to `schemas/stage2_output_schema.json`

1. **Add `reliability_outcome` inside `judge`:** Explicitly records the 4-way matrix defined in `STAGE2_EVALUATION_CRITERIA.md` §4.3 (`"True acceptance"`, `"False acceptance"`, `"True rejection"`, `"False rejection"`, `"Excluded"`).
2. **Add `exposure_mode` inside `evidence`:** Pairs with `evidence.shared` (`"unassisted_shared"` vs. `"stage1_augmented"`).
3. **Add `uniqueItems: true` on `error_characterization` arrays:** Prevents duplicate error labels while allowing `[]` when `correctness_outcome == "Correct"` or `claim_grounding_status == "Grounded"`.
