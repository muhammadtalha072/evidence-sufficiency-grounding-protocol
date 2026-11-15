# Evidence Sufficiency & Grounding Protocol (v0.1)

**Co-Leads:**
- **Samir Baladi** ([@gitdeeper15](https://github.com/gitdeeper15)) — Creator of [Agent-Judge-Framework (AJF)](https://github.com/gitdeeper15/ajf)
- **Muhammad Talha** — Creator of [pgRAG-Inspector (`pgrag-eval-lite`)](https://pypi.org/project/pgrag-eval-lite/)

A collaborative research benchmark and two-stage evaluation protocol investigating how **pre-agent structural evidence defects** interact with **post-agent LLM-as-a-Judge grounding reliability** in Retrieval-Augmented Generation (RAG) systems.

---

## Core Taxonomy

1. **Evidence-Induced Misattribution (Causal Phenomenon):** Structurally incomplete, truncated, or sibling-confounded retrieved evidence (e.g., Markdown/PDF table rows detached from column/unit headers, or high-overlap sibling error codes) induces an agent to synthesize an unfaithful or misattributed claim.
2. **Conditionally Grounded Hallucination (Evaluation Phenomenon):** An LLM-as-a-Judge evaluates the agent response conditioned solely on the retrieved evidence chunk and scores it as *faithful/grounded* due to surface lexical overlap, failing to detect that the retrieved evidence itself is structurally insufficient to justify the claim.

---

## Two-Stage Protocol Architecture

* **Stage 1 — Pre-Agent Structural Evidence Sufficiency ([`pgRAG-Inspector`](https://pypi.org/project/pgrag-eval-lite/)):** Deterministic pre-evaluation of retrieved chunks for structural defects. Natively outputs `structural_flags` (`BROKEN_MARKDOWN_TABLE`, `MID_SENTENCE_CUTOFF`, `HIGH_TOKEN_OVERLAP`).
* **Stage 2 — Post-Agent Grounding & Judge Calibration ([`Agent-Judge-Framework (AJF)`](https://github.com/gitdeeper15/ajf)):** Evaluation of agent synthesis and judge grounding decisions across three controlled evidence regimes:
  * **Regime A (Control):** Structurally Intact Evidence
  * **Regime B (Structural Degradation):** Incomplete or truncated evidence.
  * **Regime C (Sibling Distractor):** Semantically related but query-mismatched evidence.

Each of the 36 evidence items is evaluated under two judge conditions:
- **2A — Blind/Standard Judge:** Receives the query, retrieved evidence, and actual agent response, without Stage 1 diagnostics.
- **2B — Stage-1-Informed Judge:** Receives the same underlying evidence and agent response, plus the Stage 1 `structural_flags` diagnostic block.

This produces **72 planned judge evaluations** (36 evidence items × 2 conditions). Agent responses and judge results remain pending until experimental execution.

### Separation of Measurement Layers

| Layer | What It Measures | Evaluated Against |
|---|---|---|
| **Evidence Sufficiency** | Is the retrieved evidence sufficient to answer the query? | Independent reference (query + evidence only) |
| **Agent Grounding** | Does the agent response rely on the retrieved evidence? | Independent reference + actual agent response |
| **Judge Reliability** | Does the judge correctly accept/reject the agent response? | Independent reference + actual judge decision |

These layers are recorded separately. Agent grounding is `null` until an actual agent response exists. Judge reliability is `null` until an actual judge evaluation exists.

---

## Repository Structure

* `PROTOCOL_v0.1.md` — Formal experimental design and two-stage evaluation specification.
* `docs/STAGE2_EXPERIMENTAL_DESIGN_v0.1.md` — Stage 2 experimental design (DRAFT).
* `docs/STAGE2_EVALUATION_CRITERIA.md` — Stage 2 evaluation criteria (DRAFT), including the procedural completeness requirement (Section 3.4).
* `schemas/stage2_output_schema.json` — JSON Schema for a single Stage 2 evaluation record.
* `templates/case_template.json` — Unified case template for the 12 cases.
* `examples/EXP-*.json` — 12 cases (6 C1 + 6 C2), 36 evidence items total.
* `data/ajf_evidence_regimes_fixture.json` — Stage 1 baseline fixture.
* `results/STAGE1_COLAB_BASELINE.md` — Stage 1 execution report.
* `scripts/run_stage1_baseline.py` — Stage 1 structural sufficiency verifier.
* `scripts/validate_cases.py` — Schema validation for all 12 cases.
* `scripts/migrate_to_v03.py` — Migration script (historical).

---

## Case Set

| Case ID | Subtype | Domain |
|---|---|---|
| `EXP-TABLE-01` | C1: Contextual/Metadata Divergence | SEC 10-K segment revenue |
| `EXP-TABLE-02` | C1 | Financial statement period shift |
| `EXP-TABLE-03` | C1 | Infrastructure pricing units |
| `EXP-TABLE-04` | C1 | SLA percentile table |
| `EXP-TABLE-05` | C1 | Hardware telemetry matrix |
| `EXP-TABLE-06` | C1 | Compliance control schedule |
| `EXP-RUNBOOK-01` | C2: Sibling Identifier Confusion | ERR-PG-9042-WAL vs ERR-PG-7710-LOCK |
| `EXP-RUNBOOK-02` | C2 | CVE-2026-48219 vs CVE-2026-48291 |
| `EXP-RUNBOOK-03` | C2 | Meridian API v2 vs v3 deprecation |
| `EXP-RUNBOOK-04` | C2 | ERR-PG-9042 vs ERR-PG-9043 |
| `EXP-RUNBOOK-05` | C2 | max_connections vs max_locks_per_transaction |
| `EXP-RUNBOOK-06` | C2 | hnsw.iterative_scan vs ivfflat.iterative_scan |

Synthetic error codes, CVE identifiers, and API examples in C2 are illustrative and are not claims about real-world advisories or incidents. The PostgreSQL and pgvector configuration parameter names used in RUNBOOK-05 and RUNBOOK-06 refer to documented parameters.

---

## Quickstart

### Reproduce Stage 1 Baseline

```bash
pip install pgrag-eval-lite
python scripts/run_stage1_baseline.py
```

### Validate All Cases

```bash
pip install jsonschema
python scripts/validate_cases.py
```

Expected output: `ALL PASSED` with 12 cases.

---

## Status

- **Stage 1:** executed and documented (results/STAGE1_COLAB_BASELINE.md).
- **Stage 2:** 12 cases completed (6 TABLE / C1 and 6 RUNBOOK / C2), comprising 36 evidence items. All 12 cases passed JSON Schema validation and completed technical review. The 72 planned judge evaluations and agent evaluations are pending execution.
- **Ratification:** pending review by Muhammad Talha.

---

## Citation

Baladi, S. & Talha, M. (2026). Evidence Sufficiency & Grounding Protocol (v0.1) [Research benchmark and evaluation protocol]. GitHub. https://github.com/muhammadtalha072/evidence-sufficiency-grounding-protocol
