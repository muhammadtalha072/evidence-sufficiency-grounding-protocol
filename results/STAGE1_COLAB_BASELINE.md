# Stage 1 Baseline — Execution Report

**Date:** 14 November 2026
**Executed by:** Samir Baladi
**Environment:** Google Colab, Python 3.13
**Package:** pgrag-eval-lite 0.2.1
**Script:** scripts/run_stage1_baseline.py
**Data:** data/ajf_evidence_regimes_fixture.json

---

## 1. Purpose

This report documents the execution of the Stage 1 baseline.

---

## 2. Environment

| Component | Value |
|---|---|
| Platform | Google Colab |
| Python | 3.13 |
| pgrag-eval-lite | 0.2.1 |
| polars | 1.35.2 |
| pydantic | 2.14.2 |

---

## 3. Execution

Commands executed in Google Colab:

    git clone https://github.com/muhammadtalha072/evidence-sufficiency-grounding-protocol.git
    cd evidence-sufficiency-grounding-protocol
    pip install pgrag-eval-lite
    python scripts/run_stage1_baseline.py

No errors occurred.

---

## 4. Observed Results

    === Stage-1 Evidence Sufficiency Audit ===

    EXP-TABLE-01 / regime_a_intact: flags=[] sufficient=True
    EXP-TABLE-01 / regime_b_structurally_incomplete: flags=[BROKEN_MARKDOWN_TABLE, MID_SENTENCE_CUTOFF] sufficient=False
    EXP-TABLE-01 / regime_c_sibling_distractor: flags=[] sufficient=False
    EXP-RUNBOOK-01 / regime_a_intact: flags=[] sufficient=True
    EXP-RUNBOOK-01 / regime_b_structurally_incomplete: flags=[MID_SENTENCE_CUTOFF] sufficient=False
    EXP-RUNBOOK-01 / regime_c_sibling_distractor: flags=[] sufficient=False

---

## 5. Tabulated Results

Sufficiency values are read directly from the fixture; they are not computed by the scanner.

| Case | Regime | Structural Flags | Sufficiency (fixture-declared) |
|---|---|---|---|
| EXP-TABLE-01 | A - Intact | none | True |
| EXP-TABLE-01 | B - Structurally incomplete | BROKEN_MARKDOWN_TABLE, MID_SENTENCE_CUTOFF | False |
| EXP-TABLE-01 | C - Sibling distractor | none | False |
| EXP-RUNBOOK-01 | A - Intact | none | True |
| EXP-RUNBOOK-01 | B - Structurally incomplete | MID_SENTENCE_CUTOFF | False |
| EXP-RUNBOOK-01 | C - Sibling distractor | none | False |

---

## 6. Observations (descriptive only)

1. Regime A produced no structural flags and was declared sufficient=True in the fixture.
2. Regime B produced at least one structural flag and was declared sufficient=False in the fixture.
3. Regime C produced no structural flags and was declared sufficient=False in the fixture.

Observation 3: the current Stage 1 scanner does not assign structural flags to Regime C. The fixture nonetheless declares Regime C insufficient. Implications for Stage 2 are outside this report.

---

## 7. Scope and Limitations

- Only the two cases in data/ajf_evidence_regimes_fixture.json were executed.
- The script does not run any LLM agent or judge.
- The script does not compute sufficiency; it reads declared values from the fixture.
- The execution procedure is reproducible using the same script, fixture, and package version.

---

## 8. Artifact Locations

| Artifact | Path |
|---|---|
| Fixture | data/ajf_evidence_regimes_fixture.json |
| Script | scripts/run_stage1_baseline.py |
| This report | results/STAGE1_COLAB_BASELINE.md |
