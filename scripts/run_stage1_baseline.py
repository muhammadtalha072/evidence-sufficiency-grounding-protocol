"""Reproducible Stage-1 Pre-Agent Structural Evidence Sufficiency Baseline."""

from __future__ import annotations

import json
from pathlib import Path

from pgrag_inspector.sample_data import get_default_chunks
from pgrag_inspector.scanner import scan_chunks_health


def main() -> None:
    fixture_path = Path(__file__).resolve().parent.parent / "data" / "ajf_evidence_regimes_fixture.json"
    cases = json.loads(fixture_path.read_text(encoding="utf-8"))
    base_chunk = get_default_chunks()[0]

    print("=== Stage-1 Evidence Sufficiency Audit (pgRAG-Inspector) ===")
    for case in cases:
        print(f"\nCase: {case['case_id']} | Query: {case['query']}")
        for regime_name, rdata in case["regimes"].items():
            chunk = base_chunk.model_copy(
                update={"id": rdata["chunk_id"], "doc_id": rdata["doc_id"], "content": rdata["content"]}
            )
            flags = [f.issue_type for f in scan_chunks_health([chunk])]
            print(f"  - {regime_name:<35} -> flags={flags} | sufficient={rdata['stage1_evidence_sufficient']}")


if __name__ == "__main__":
    main()
