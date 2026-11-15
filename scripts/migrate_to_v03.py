#!/usr/bin/env python3
"""
Migrate existing Stage 2 cases to the v0.3 protocol.

Changes applied:
1. stage1_diagnostic_block: keep only structural_flags.
2. reference.claim_grounding_status -> null if agent.response is null.
3. reference.grounding_assessment_status -> "Pending agent response" if agent.response is null.
4. reference.grounding_error_characterization -> [] if agent.response is null.
5. expected_judge_behavior.reliability_outcome -> null if agent.response is null.
"""

import json
from pathlib import Path


def migrate_case(path: Path) -> bool:
    with path.open(encoding="utf-8") as f:
        case = json.load(f)

    changed = False

    for regime_name, regime in case["regimes"].items():
        agent_response = regime["agent"].get("response")
        is_pending = agent_response is None

        # 1. stage1_diagnostic_block: only structural_flags
        for eval_item in regime.get("judge_evaluations", []):
            block = eval_item.get("judge_input", {}).get("stage1_diagnostic_block")
            if isinstance(block, dict):
                new_block = {"structural_flags": block.get("structural_flags", [])}
                if block != new_block:
                    eval_item["judge_input"]["stage1_diagnostic_block"] = new_block
                    changed = True

        # 2-4. reference fields
        if is_pending:
            ref = regime.get("reference", {})
            if ref.get("claim_grounding_status") is not None:
                ref["claim_grounding_status"] = None
                changed = True
            if ref.get("grounding_error_characterization") != []:
                ref["grounding_error_characterization"] = []
                changed = True
            if ref.get("grounding_assessment_status") != "Pending agent response":
                ref["grounding_assessment_status"] = "Pending agent response"
                changed = True

        # 5. expected_judge_behavior.reliability_outcome
        if is_pending:
            ejb = regime.get("expected_judge_behavior", {})
            if ejb.get("reliability_outcome") is not None:
                ejb["reliability_outcome"] = None
                changed = True

    if changed:
        with path.open("w", encoding="utf-8") as f:
            json.dump(case, f, indent=2, ensure_ascii=False)
            f.write("\n")

    return changed


def main() -> None:
    cases_dir = Path("examples")
    files = sorted(cases_dir.glob("EXP-*.json"))

    print(f"Migrating {len(files)} cases to v0.3 protocol\n")

    for path in files:
        changed = migrate_case(path)
        status = "MIGRATED" if changed else "UNCHANGED"
        print(f"  {path.name}: {status}")


if __name__ == "__main__":
    main()
