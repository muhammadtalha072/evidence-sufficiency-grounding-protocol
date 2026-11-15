#!/usr/bin/env python3
"""
Validate all Stage 2 case files against the unified case template.

Usage:
    python scripts/validate_cases.py

Exit code 0 if all cases pass, 1 otherwise.
"""

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def main() -> int:
    schema_path = Path("templates/case_template.json")
    cases_dir = Path("examples")

    if not schema_path.exists():
        print(f"ERROR: schema not found at {schema_path}")
        return 1

    if not cases_dir.exists():
        print(f"ERROR: cases directory not found at {cases_dir}")
        return 1

    with schema_path.open(encoding="utf-8") as f:
        schema = json.load(f)

    validator = Draft202012Validator(schema)
    case_files = sorted(cases_dir.glob("EXP-*.json"))

    if not case_files:
        print("ERROR: no case files found in examples/")
        return 1

    failed = False
    print("=" * 50)
    print("Stage 2 Case Validation")
    print(f"Schema: {schema_path}")
    print(f"Cases:  {cases_dir}")
    print("=" * 50)

    for path in case_files:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)

        errors = sorted(
            validator.iter_errors(data),
            key=lambda e: list(map(str, e.absolute_path)),
        )

        print(f"\n{path.name}")
        if errors:
            failed = True
            print("  SCHEMA VALIDATION: FAILED")
            for error in errors:
                location = "/".join(map(str, error.absolute_path)) or "<root>"
                print(f"    {location}: {error.message}")
        else:
            print("  SCHEMA VALIDATION: PASSED")

    print("\n" + "=" * 50)
    print("ALL PASSED" if not failed else "VALIDATION FAILED")
    print(f"Cases checked: {len(case_files)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
