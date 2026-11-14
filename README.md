# Evidence Sufficiency & Grounding Protocol (v0.1)

**Co-Leads:**
- **Samir Baladi** ([@gitdeeper15](https://github.com/gitdeeper15)) — Creator of [Agent-Judge-Framework (AJF)](https://github.com/gitdeeper15/ajf)
- **Muhammad Talha** — Creator of [pgRAG-Inspector (`pgrag-eval-lite`)](https://pypi.org/project/pgrag-eval-lite/)

A collaborative research benchmark and two-stage evaluation protocol investigating how **pre-agent structural evidence defects** interact with **post-agent LLM-as-a-Judge grounding reliability** in Retrieval-Augmented Generation (RAG) systems.

---

## Core Taxonomy

1. **Evidence-Induced Misattribution (Causal Phenomenon):** Structurally incomplete, truncated, or sibling-confounded retrieved evidence (e.g., Markdown/PDF table rows detached from column/unit headers, or high-overlap sibling error codes) induces an agent to synthesize an unfaithful or misattributed claim.
2. **Conditionally Grounded Hallucination (Evaluation Phenomenon):** An LLM-as-a-Judge evaluates the agent's response conditioned solely on the retrieved evidence chunk and scores it as *faithful/grounded* due to surface lexical overlap, failing to detect that the retrieved evidence itself is structurally insufficient to justify the claim.

---

## Two-Stage Protocol Architecture

* **Stage 1 — Pre-Agent Structural Evidence Sufficiency ([`pgRAG-Inspector`](https://pypi.org/project/pgrag-eval-lite/)):** Deterministic pre-evaluation of retrieved chunks for `BROKEN_MARKDOWN_TABLE`, `MID_SENTENCE_CUTOFF`, `HIGH_TOKEN_OVERLAP (>80%)`, and exact identifier rank margins (`raw_cosine_distance`, `raw_fts_rank`, `rrf_score`).
* **Stage 2 — Post-Agent Grounding & Judge Calibration ([`Agent-Judge-Framework (AJF)`](https://github.com/gitdeeper15/ajf)):** Evaluation of agent synthesis and multi-judge false-positive grounding rates across three controlled evidence regimes:
  * **Regime A (Control):** Structurally Intact Evidence (`Docling HybridChunker + contextualize()`)
  * **Regime B (Structural Degradation):** Orphaned Table Rows & Mid-Clause Truncations
  * **Regime C (Sibling Distractor):** High-Overlap Sibling Entities (`ERR-PG-9042-WAL` vs. `ERR-PG-7710-LOCK`)

---

## Repository Structure

* `PROTOCOL_v0.1.md` — Formal experimental design, hypotheses, and two-stage evaluation specification.
* `data/ajf_evidence_regimes_fixture.json` — Controlled 3-regime evidence benchmark dataset with Stage-1 deterministic structural flags.
* `scripts/run_stage1_baseline.py` — Reproducible Stage-1 structural sufficiency verifier.

## Quickstart (Reproduce Stage-1 Baseline)

    pip install pgrag-eval-lite
    python scripts/run_stage1_baseline.py
