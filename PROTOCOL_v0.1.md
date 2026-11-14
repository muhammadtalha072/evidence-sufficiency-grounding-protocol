# Two-Stage Evidence Sufficiency & Grounding Protocol (v0.1)

**Co-Leads:**
- **Samir Baladi** ([`gitdeeper15`](https://github.com/gitdeeper15) — [Agent-Judge-Framework (`ajf`)](https://github.com/gitdeeper15/ajf))
- **Muhammad Talha** ([`pgrag-eval-lite`](https://pypi.org/project/pgrag-eval-lite/) — `pgRAG-Inspector`)

## 1. Core Taxonomy
1. **Evidence-Induced Misattribution (Causal Phenomenon):** Structurally incomplete, truncated, or sibling-confounded retrieved evidence induces an agent to synthesize an unfaithful or misattributed claim.
2. **Conditionally Grounded Hallucination (Evaluation Phenomenon):** A post-hoc Judge evaluates the agent's claim conditioned solely on the retrieved chunk and scores it as *faithful/grounded* because lexical tokens match, failing to detect that the evidence itself lacked the structural schema or identifier parity required to justify the interpretation.

## 2. Two-Stage Protocol Architecture
- **Stage 1 — Pre-Agent Structural Evidence Sufficiency (`pgRAG-Inspector`):** Deterministically audits retrieved candidate chunks for `BROKEN_MARKDOWN_TABLE` (orphaned rows / detached column headers), `MID_SENTENCE_CUTOFF`, `HIGH_TOKEN_OVERLAP`, and exact alphanumeric identifier parity (`simple` + `english` dual `tsvector` + RRF margin) before conditioning the agent or judge.
- **Stage 2 — Post-Agent Grounding & Judge Reliability ([`gitdeeper15/ajf`](https://github.com/gitdeeper15/ajf)):** Evaluates agent outputs and LLM-Judge false-positive grounding rates across three controlled evidence regimes:
  - **Regime A:** Structurally Intact Evidence (Control)
  - **Regime B:** Semantically Relevant / Structurally Incomplete Evidence (Orphaned Table Row / Truncated Clause)
  - **Regime C:** High-Overlap Sibling Distractor (`ERR-PG-9042-WAL` vs. `ERR-PG-7710-LOCK`)
