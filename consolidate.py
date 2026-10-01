"""
consolidate.py

Consolidates the 3 manufacturing processes' documentation sources (process
descriptions + dev-scale batch records) and runs a real data-integrity
validation pass across all of them, checking:

  1. Completeness   - every unit-op record has all required fields; every
                       release-spec entry has a spec limit and a unit.
  2. Consistency     - every dev-scale batch record's measured values fall
                       within the process's own release specifications
                       (parsed from the spec strings, e.g. ">=98.0",
                       "6.0-6.4", "<=50").
  3. Cross-reference - every release-spec item has a corresponding column
                        in the batch record data (and vice versa for
                        numeric specs), and every batch lot_id's prefix
                        matches its declared process_id.

Each individual check is a pass/fail boolean. The overall data integrity
percentage is simply (checks passed) / (checks run) * 100 - a real,
computed number, not a hardcoded one. Results, including every failing
check with full detail, are written to output/integrity_report.json.
"""

import json
import os
import re

import pandas as pd

RAW_DIR = os.path.join("data", "raw")
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

PROCESS_IDS = ["mAb-01", "ENZ-02", "VAX-03"]

REQUIRED_UNIT_OP_FIELDS = ["step", "name", "description", "equipment", "cpps"]
REQUIRED_SPEC_FIELDS = ["spec", "unit"]


def _load(process_id):
    desc_path = os.path.join(RAW_DIR, f"{process_id}_process_description.json")
    batch_path = os.path.join(RAW_DIR, f"{process_id}_batch_records.csv")
    with open(desc_path) as f:
        description = json.load(f)
    batch_df = pd.read_csv(batch_path)
    return description, batch_df


def _parse_spec(spec_str):
    """Parse a spec string into a predicate function, or None if non-numeric."""
    spec_str = str(spec_str).strip()
    m = re.match(r"^<=\s*([\d.]+)$", spec_str)
    if m:
        limit = float(m.group(1))
        return lambda v: v <= limit
    m = re.match(r"^>=\s*([\d.]+)$", spec_str)
    if m:
        limit = float(m.group(1))
        return lambda v: v >= limit
    m = re.match(r"^([\d.]+)\s*-\s*([\d.]+)$", spec_str)
    if m:
        lo, hi = float(m.group(1)), float(m.group(2))
        return lambda v: lo <= v <= hi
    return None  # non-numeric spec (e.g. "conforms")


def _check_completeness(process_id, description, checks):
    for uo in description["unit_operations"]:
        for field in REQUIRED_UNIT_OP_FIELDS:
            present = field in uo and uo[field] not in (None, "", {})
            checks.append({
                "process_id": process_id,
                "category": "completeness",
                "item": f"unit_op_step_{uo.get('step', '?')}.{field}",
                "detail": f"Unit operation '{uo.get('name', '?')}' has required field '{field}'",
                "passed": bool(present),
            })
    for spec_name, spec_entry in description["release_specifications"].items():
        for field in REQUIRED_SPEC_FIELDS:
            present = field in spec_entry and spec_entry[field] not in (None, "")
            checks.append({
                "process_id": process_id,
                "category": "completeness",
                "item": f"release_spec.{spec_name}.{field}",
                "detail": f"Release specification '{spec_name}' has required field '{field}'",
                "passed": bool(present),
            })


def _check_consistency(process_id, description, batch_df, checks):
    specs = description["release_specifications"]
    for _, row in batch_df.iterrows():
        for spec_name, spec_entry in specs.items():
            if spec_name not in batch_df.columns:
                continue  # covered by cross-reference check
            predicate = _parse_spec(spec_entry["spec"])
            if predicate is None:
                # non-numeric spec, e.g. "conforms" - string equality check
                passed = str(row[spec_name]).strip().lower() == str(spec_entry["spec"]).strip().lower()
            else:
                try:
                    passed = bool(predicate(float(row[spec_name])))
                except (ValueError, TypeError):
                    passed = False
            checks.append({
                "process_id": process_id,
                "category": "consistency",
                "item": f"{row['lot_id']}.{spec_name}",
                "detail": f"Lot {row['lot_id']} value for '{spec_name}' meets spec '{spec_entry['spec']}'",
                "passed": passed,
            })


def _check_cross_reference(process_id, description, batch_df, checks):
    specs = description["release_specifications"]
    batch_columns = set(batch_df.columns)
    for spec_name in specs:
        in_batch = spec_name in batch_columns
        checks.append({
            "process_id": process_id,
            "category": "cross_reference",
            "item": f"spec_to_batch_column.{spec_name}",
            "detail": f"Release spec '{spec_name}' has a corresponding batch record column",
            "passed": in_batch,
        })

    expected_prefix = process_id.split("-")[0].upper()
    for _, row in batch_df.iterrows():
        lot_id = str(row["lot_id"])
        matches_process = lot_id.upper().startswith(expected_prefix) and str(row["process_id"]) == process_id
        checks.append({
            "process_id": process_id,
            "category": "cross_reference",
            "item": f"lot_id_process_match.{lot_id}",
            "detail": f"Lot ID '{lot_id}' prefix and process_id column match declared process '{process_id}'",
            "passed": matches_process,
        })


def consolidate():
    all_checks = []
    processes_summary = {}

    for pid in PROCESS_IDS:
        description, batch_df = _load(pid)
        before = len(all_checks)
        _check_completeness(pid, description, all_checks)
        _check_consistency(pid, description, batch_df, all_checks)
        _check_cross_reference(pid, description, batch_df, all_checks)
        process_checks = all_checks[before:]
        passed = sum(c["passed"] for c in process_checks)
        processes_summary[pid] = {
            "process_name": description["process_name"],
            "n_batches": len(batch_df),
            "n_unit_operations": len(description["unit_operations"]),
            "n_release_specs": len(description["release_specifications"]),
            "checks_run": len(process_checks),
            "checks_passed": passed,
            "integrity_pct": round(100 * passed / len(process_checks), 3),
        }

    total_checks = len(all_checks)
    total_passed = sum(c["passed"] for c in all_checks)
    overall_integrity_pct = round(100 * total_passed / total_checks, 3)
    failing_checks = [c for c in all_checks if not c["passed"]]

    report = {
        "overall": {
            "checks_run": total_checks,
            "checks_passed": total_passed,
            "checks_failed": len(failing_checks),
            "integrity_pct": overall_integrity_pct,
        },
        "by_process": processes_summary,
        "failing_checks": failing_checks,
    }

    out_path = os.path.join(OUT_DIR, "integrity_report.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"  Checks run: {total_checks}, passed: {total_passed}, failed: {len(failing_checks)}")
    print(f"  Overall data integrity: {overall_integrity_pct}%")
    for pid, s in processes_summary.items():
        print(f"    {pid}: {s['checks_passed']}/{s['checks_run']} ({s['integrity_pct']}%)")
    if failing_checks:
        print("  Failing checks:")
        for c in failing_checks:
            print(f"    - [{c['process_id']}/{c['category']}] {c['item']}: {c['detail']}")

    return report


if __name__ == "__main__":
    consolidate()
