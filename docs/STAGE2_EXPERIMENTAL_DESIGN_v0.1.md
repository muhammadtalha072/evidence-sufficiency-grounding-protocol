# Stage 2 — Experimental Design (DRAFT v0.1)

> **Status:** Initial proposal, subject to joint review and revision.
> **Not a ratified protocol.** Sections marked "Open" require agreement before any implementation.

**Co-Leads:**
- Samir Baladi (Agent-Judge-Framework)
- Muhammad Talha (pgRAG-Inspector)

**Date:** 14 November 2026

---

## 1. Purpose

Stage 1 (pgRAG-Inspector) has been executed and documented in results/STAGE1_COLAB_BASELINE.md. Stage 2 shifts the question from structural integrity of retrieved evidence to the reliability of agent synthesis and judge evaluation under degraded evidence.

The central question this draft proposes to investigate is:

> When retrieved evidence is structurally degraded or semantically confounded, does an LLM-as-a-Judge incorrectly accept an agent response as grounded?

Stage 2 therefore asks three separate questions, which must not be collapsed into one:

1. Does the agent produce an incorrect or misattributed answer under degraded evidence?
2. Does the judge incorrectly accept that answer as grounded?
3. Does the judge correctly detect that the retrieved evidence is insufficient to support the claim?

---

## 2. Three Evidence Regimes

The three regimes are carried forward from Stage 1 without modification.

### Regime A — Structurally Intact Evidence (Control)
Retrieved chunks preserve header-row relationships, units, identifiers, and structural boundaries.

### Regime B — Structurally Incomplete Evidence
Retrieved chunks contain relevant content but lack essential structural context (detached table headers, missing units, mid-clause truncation).

### Regime C — Sibling Distractor
Retrieved chunks contain high surface similarity to the correct evidence but refer to a different identifier, standard, year, or operational context.

**Note on heterogeneity within Regime C (open for discussion).**

The two cases currently grouped under Regime C do not exercise the same mechanism:

- The TABLE case tests contextual and metadata divergence: same segment name, different year, different accounting standard (GAAP vs Non-GAAP), different unit (millions vs thousands).
- The RUNBOOK case tests sibling identifier confusion: two distinct error codes (ERR-PG-9042-WAL vs ERR-PG-7710-LOCK) that share terminology and remediation vocabulary.

Both are retained under Regime C as a provisional grouping. Whether they should remain a single regime or be split into two sub-regimes (C1 — Contextual/Metadata Divergence; C2 — Sibling Identifier Confusion) is left open for joint decision.

---

## 3. Three Distinctions

Stage 2 is designed to separate three outcomes that are frequently conflated.

### 3.1 Agent Response Failure
The agent produces an answer that is incorrect, misattributed, or unsupported by the retrieved evidence.

### 3.2 Judge Evaluation Failure
The judge evaluates the agent response against the retrieved evidence and accepts it as grounded, although the evidence does not justify the claim. This is the phenomenon referred to in the taxonomy as Conditionally Grounded Hallucination.

### 3.3 Judge Detection Success
The judge recognizes that the retrieved evidence is insufficient to support the claim, even when the agent response is linguistically plausible or superficially aligned with the evidence tokens.

These three outcomes are independent. An experiment is only interpretable if they are recorded separately.

---

## 4. Experimental Flow

The proposed flow is:

    Stage 1 (pgRAG-Inspector)
        -> Evidence regime label (A / B / C)
        -> Structural flags
    Agent
        -> Agent response
    Judge (AJF)
        -> Judge decision
        -> Judge confidence (where available)
    Evaluation
        -> Agent correctness
        -> Judge acceptance (grounded / not grounded)
        -> Judge detection (detected insufficiency / did not detect)

### 4.1 Independent Evaluation Reference

Evaluation of both the agent and the judge must be anchored to a reference that is independent of either model. Without such a reference, it is not possible to distinguish agent failure from judge failure.

The independent reference includes:

    Gold answer / expected claims
        -> Used to evaluate agent correctness
    Evidence sufficiency reference
        -> Used to evaluate whether the retrieved evidence was sufficient
    Expected judge behavior per regime
        -> Used to evaluate judge acceptance and detection

This reference is used for post-hoc evaluation only. It is not automatically exposed to the agent or the judge. Whether the judge receives the reference, or Stage 1 flags, is an open design question (see Section 5.2).

Without an independent reference:

- A wrong answer accepted by the judge could be attributed to either the agent or the judge.
- A correct answer rejected by the judge could be misread as judge failure when it reflects a poorly specified rubric.
- Judge detection success could not be distinguished from judge agreement with the agent.

## 5. Open Questions

The following questions are deliberately left open. No implementation should begin before they are agreed in writing.

### 5.1 Model Configuration
- Will the agent and the judge use the same model, or two distinct models from independent families?
- What model version and provider will be recorded for reproducibility?
- How will provider-specific non-determinism be documented?

### 5.2 Evidence Exposure
- Will the judge receive exactly the evidence the agent received, or an augmented view that includes Stage 1 structural flags?
- If the judge receives Stage 1 flags, does that constitute a form of scaffolding that changes the research question?
- If the judge does not receive Stage 1 flags, how will detection be measured independently of structural cues?

### 5.3 Measuring Detection
- What counts as successful detection of insufficient evidence?
- Is detection a binary outcome, an ordinal rating, or a probability derived from the judge confidence?
- How will false positives (judge declares insufficiency when evidence is sufficient) be recorded?

### 5.4 Boundary Between Response Failure and Evaluation Failure
- When the agent answer is wrong and the judge rejects it, is that agent failure or correct judgment?
- When the agent answer is wrong and the judge accepts it, is that judge failure or expected behavior given the evidence?
- How will ambiguous cases be adjudicated and documented?

### 5.5 Scope of Stage 2
- Will Stage 2 reuse the two existing cases, or extend the fixture to additional cases?
- If extended, how many cases per regime are required for a meaningful pilot?
- Will human review be included, or is Stage 2 fully automated?

---

## 6. Status

This document is a draft. It records a proposed design, not an agreed protocol. It does not select a model provider, does not specify an implementation, and does not commit either collaborator to a particular execution path.

Changes to this document are expected after discussion with Muhammad Talha.
