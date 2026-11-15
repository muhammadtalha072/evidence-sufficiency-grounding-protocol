# Stage 2 — Evaluation Criteria (DRAFT v0.1)

> **Status:** Initial proposal, subject to joint review and revision.
> **Not a ratified protocol.** Criteria marked "Open" require agreement before implementation.

**Co-Leads:**
- Samir Baladi (Agent-Judge-Framework)
- Muhammad Talha (pgRAG-Inspector)

**Date:** 14 November 2026

---

## 1. Purpose

This document proposes evaluation criteria for Stage 2. It defines how the three outcomes introduced in STAGE2_EXPERIMENTAL_DESIGN_v0.1.md should be measured:

1. Agent response correctness.
2. Evidence sufficiency.
3. Judge reliability (acceptance and detection).

The criteria are intentionally separated. Agent correctness is evaluated against an independent reference. Evidence sufficiency is evaluated against a declared reference. Judge reliability is evaluated by comparing the judge decision to both.

No single score aggregates the three. Aggregation, if any, is deferred to a later decision.

---

## 2. Agent Correctness Criteria

Agent correctness asks a single question: does the agent response satisfy the task given the evidence available to it?

Correctness is measured on two independent axes: a correctness outcome and an error characterization. These axes are not collapsed into one label.

### 2.1 Correctness Outcome

| Label | Definition |
|---|---|
| Correct | The response matches the expected answer, or an acceptable alternative, as defined in the independent reference. |
| Partially correct | The response contains some correct elements but omits or misstates essential parts. |
| Incorrect | The response contradicts the expected answer or states an unsupported claim as fact. |
| Abstained | The agent declines to answer, or explicitly states that the evidence is insufficient. |

### 2.2 Error Characterization (applied when outcome is not Correct)

| Label | Definition |
|---|---|
| Misattributed | The response attributes a claim to the wrong identifier, year, standard, unit, or entity. |
| Unsupported | The response states a claim not grounded in the available evidence, even if the claim happens to be true. |
| Omitted | The response leaves out an essential element required by the query. |
| Contradictory | The response contradicts itself or the evidence. |

### 2.3 Notes

- A response may carry more than one error characterization. The primary characterization is recorded, and secondary ones are preserved in the record.
- Misattributed is a characterization of how a response fails, not a separate correctness outcome. A misattributed response is still Incorrect or Partially correct as an outcome.
- The independent reference defines what counts as acceptable alternative answers.
- The agent is not penalized for lacking information it was not given.
- The conditions under which abstention is the appropriate behavior are left open (see Section 6.1).

---

## 3. Evidence Sufficiency Criteria

Evidence sufficiency asks whether the retrieved evidence, as presented to the agent, was sufficient to justify the expected answer.

### 3.1 Proposed Categories

| Label | Definition |
|---|---|
| Sufficient | The evidence contains all structural and semantic elements needed to justify the expected answer. |
| Insufficient (structural) | The evidence is missing structural context required for interpretation (headers, units, boundaries). |
| Insufficient (semantic) | The evidence is structurally intact but refers to a different identifier, context, or entity than the one required by the query. |
| Ambiguous | The evidence could support more than one interpretation, and the reference does not resolve which is expected. |

### 3.2 Relation to Stage 1 Flags

Stage 1 flags (BROKEN_MARKDOWN_TABLE, MID_SENTENCE_CUTOFF, HIGH_TOKEN_OVERLAP) are structural indicators. They are not equivalent to evidence sufficiency.

- A chunk may have no structural flags and still be Insufficient (semantic) — as observed for Regime C in the Stage 1 baseline.
- A chunk may have a structural flag and still be Sufficient if the missing element is not required for the specific query.

Stage 1 flags are therefore treated as one input to the sufficiency judgment, not as the judgment itself.

### 3.3 Notes

- Sufficiency is query-conditioned. The same chunk may be Sufficient for one query and Insufficient for another.
- Sufficiency is evaluated against the independent reference, not against the agent response.
- The distinction between structural and semantic insufficiency is proposed for clarity; whether it should be formalized as two separate categories is left open (see Section 6.2).


### 3.4 Completeness Requirement for Procedural Evidence

Evidence sufficiency for procedural queries requires the retrieved evidence to specify a complete remediation action. Partial procedures, even when they identify most required steps, are classified as **Insufficient (structural)** when a necessary final operational step is missing.

A procedure is considered complete when the retrieved evidence provides all operational steps necessary to answer the query without requiring the agent to infer or supply a missing remediation step.

This requirement distinguishes evidence insufficiency from agent knowledge. An agent may be able to complete a procedure from prior knowledge, but the retrieved evidence itself remains insufficient if the missing step is not present in it.

---

## 4. Judge Reliability Criteria

Judge reliability asks whether the judge decision is consistent with the independent reference.

The judge produces two independent outputs, recorded separately:

1. A grounding decision (accept / reject / abstain).
2. A sufficiency detection flag (detects insufficiency / does not detect / not applicable).

These are not the same axis. A judge may accept a correct response while noting that the evidence was minimal. A judge may reject an incorrect response without recognizing that the root cause was insufficiency.

### 4.1 Grounding Decision

| Label | Definition |
|---|---|
| Accepts as grounded | The judge evaluates the agent response as grounded in the retrieved evidence. |
| Rejects as ungrounded | The judge evaluates the agent response as not grounded in the retrieved evidence. |
| Abstains | The judge declines to evaluate, or returns an unclassifiable decision. |

### 4.2 Sufficiency Detection

| Label | Definition |
|---|---|
| Detects insufficiency | The judge explicitly states that the retrieved evidence is insufficient to support the claim, independent of whether the answer is correct. The specific reason (structural incompleteness, semantic mismatch, or general insufficiency) may be recorded in a rationale field, but does not constitute a separate detection category. |
| Does not detect | The judge does not raise insufficiency, regardless of grounding decision. |
| Not applicable | The judge was not asked to assess sufficiency, or the protocol version excludes detection. |

### 4.3 Reliability Comparison

Each grounding decision is compared against the reference grounding status (Section 5.2). The comparison produces one of four outcomes:

| Outcome | Meaning |
|---|---|
| True acceptance | Judge accepts a response marked Grounded. |
| False acceptance | Judge accepts a response marked Ungrounded. This is the phenomenon labeled Conditionally Grounded Hallucination. |
| True rejection | Judge rejects a response marked Ungrounded. |
| False rejection | Judge rejects a response marked Grounded. |

Responses marked Ambiguous are excluded from the binary comparison, or adjudicated according to a rule agreed later (see Section 6.2). Detection is recorded independently of this comparison and is not folded into the four outcomes above.

### 4.4 Notes

- Reliability is not a single number. False acceptance and false rejection are reported separately.
- Judge confidence is recorded where available, but is not used to weight the decision. Calibration analysis is deferred to a later decision.
- Judge rationale is preserved verbatim for later qualitative review.

---

## 5. Cross-Cutting Criteria

### 5.1 Recorded Inputs

For every evaluated item, the following are recorded:

- Case ID and regime label.
- Agent model, version, and provider.
- Judge model, version, and provider.
- Prompt versions used for the agent and the judge.
- The evidence presented to the agent.
- The evidence presented to the judge (which may differ).
- Agent response.
- Agent correctness outcome.
- Agent error characterization (when applicable).
- Judge grounding decision.
- Judge sufficiency detection flag.
- Judge confidence, where available.
- Independent reference values, recorded as separate fields:
  - answer_correctness (Correct / Partially correct / Incorrect / Abstained)
  - claim_grounding_status (Grounded / Ungrounded / Ambiguous)
  - grounding_error_characterization (Misattributed / Unsupported / Omitted / Contradictory / None)
  - evidence_sufficiency (Sufficient / Insufficient (structural) / Insufficient (semantic) / Ambiguous)
- Stage 1 structural flags.

### 5.2 Separation of Answer Correctness and Claim Grounding

Answer correctness and claim grounding are recorded as separate fields in the independent reference. They are not assumed to agree.

A response may be factually correct but not grounded in the retrieved evidence (for example, when the agent relies on prior knowledge while the retrieved evidence does not support the claim). A response may be grounded in the retrieved evidence but factually incorrect (for example, when the evidence itself is wrong).

Judge reliability is evaluated against claim_grounding_status, not against answer_correctness. This separation ensures that a correct answer is not automatically treated as evidence of correct grounding, and vice versa.

### 5.3 Separation of Models

Unless otherwise agreed, the agent and judge are distinct model instances. If the same model is used for both, this is recorded explicitly as a potential confound.

### 5.4 Reproducibility

Each evaluation item must be reproducible from the recorded inputs. Model non-determinism is acknowledged; identical outputs are not claimed.

---

## 6. Open Questions

The following criteria decisions are left open.

### 6.1 Abstention
- Under what conditions should agent abstention be considered an appropriate response, given the evidence sufficiency reference?
- Does judge abstention count as a reliability failure, a detection success, or neither?

### 6.2 Ambiguous Cases
- How should responses marked Ambiguous be handled in the reliability comparison?
- Are they excluded, adjudicated by a third party, or treated as a separate outcome?

### 6.3 Structural vs. Semantic Insufficiency
- Should Insufficient (structural) and Insufficient (semantic) remain distinct categories, or be merged into a single Insufficient label with a subtype field?

### 6.4 Acceptable Alternatives
- Who defines what counts as an acceptable alternative answer?
- How are alternatives adjudicated if the collaborators disagree?

### 6.5 Aggregation
- Are per-item outcomes ever aggregated into a per-regime score?
- If yes, how are false acceptance and false rejection weighted?
- If no, how are results reported to remain interpretable?

### 6.6 Human Review
- Is human review required for a subset of items?
- If yes, what proportion, and how is inter-rater agreement measured?

---

## 7. Status

This document is a draft. It proposes evaluation categories and procedures, not a ratified protocol. It does not specify an implementation and does not commit either collaborator to a particular measurement choice.

Changes to this document are expected after discussion with Muhammad Talha.
