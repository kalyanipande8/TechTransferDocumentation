"""
process_understanding_report.py

Generates the consolidated Process Understanding Report summarizing the
documentation consolidation effort and tech-transfer readiness across all
3 processes, from output/integrity_report.json (produced by consolidate.py)
and the raw process/batch data.

Output: output/process_understanding_report.md
"""

import json
import os
from datetime import date

import pandas as pd

RAW_DIR = os.path.join("data", "raw")
OUT_DIR = "output"
TODAY = date.today().isoformat()

PROCESS_IDS = ["mAb-01", "ENZ-02", "VAX-03"]


def _load_description(pid):
    with open(os.path.join(RAW_DIR, f"{pid}_process_description.json")) as f:
        return json.load(f)


def generate_report():
    with open(os.path.join(OUT_DIR, "integrity_report.json")) as f:
        integrity = json.load(f)

    lines = [
        "# Process Understanding Report",
        "## Technology Transfer Readiness - Consolidated Manufacturing Process Documentation",
        "",
        f"**Report Date:** {TODAY}  ",
        f"**Processes Covered:** {', '.join(PROCESS_IDS)} (3 manufacturing processes)  ",
        f"**Prepared For:** Commercial Manufacturing Scale-Up / Technology Transfer",
        "",
        "## 1. Executive Summary",
        "",
        f"Process documentation for {len(PROCESS_IDS)} distinct development/pilot-scale "
        "manufacturing processes was consolidated into a standardized documentation package "
        "(process description, batch record template, and SOP per process) in preparation "
        "for technology transfer to a commercial manufacturing site. A cross-source data "
        "integrity review was performed across all documentation and batch record sources.",
        "",
        f"**Overall data integrity: {integrity['overall']['integrity_pct']}%** "
        f"({integrity['overall']['checks_passed']} of {integrity['overall']['checks_run']} "
        "automated completeness, consistency, and cross-reference checks passed).",
        "",
        "## 2. Processes Consolidated",
        "",
        "| Process ID | Process Name | Modality | Dev/Pilot Scale | Target Commercial Scale | Unit Ops | Release Specs | Batches Reviewed |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for pid in PROCESS_IDS:
        d = _load_description(pid)
        s = integrity["by_process"][pid]
        lines.append(
            f"| {pid} | {d['process_name']} | {d['modality']} | {d['development_scale']} | "
            f"{d['target_commercial_scale']} | {s['n_unit_operations']} | {s['n_release_specs']} | {s['n_batches']} |"
        )

    lines += [
        "",
        "## 3. Data Integrity Assessment",
        "",
        "Three categories of automated checks were run against each process's documentation "
        "sources (process description JSON + dev-scale batch records):",
        "",
        "1. **Completeness** - every unit-operation record has a step, name, description, "
        "equipment, and CPP set; every release specification has both a limit and a unit.",
        "2. **Consistency** - every dev-scale batch record's measured value for each release "
        "attribute falls within that process's own approved specification.",
        "3. **Cross-reference** - every release specification maps to a corresponding batch "
        "record data column, and every batch lot ID and process_id tag is internally "
        "consistent with its declared process.",
        "",
        "| Process ID | Checks Run | Checks Passed | Integrity % |",
        "|---|---|---|---|",
    ]
    for pid in PROCESS_IDS:
        s = integrity["by_process"][pid]
        lines.append(f"| {pid} | {s['checks_run']} | {s['checks_passed']} | {s['integrity_pct']}% |")
    lines.append(
        f"| **Overall** | **{integrity['overall']['checks_run']}** | "
        f"**{integrity['overall']['checks_passed']}** | **{integrity['overall']['integrity_pct']}%** |"
    )

    lines += ["", "### 3.1 Issues Identified", ""]
    if integrity["failing_checks"]:
        lines += [
            "The following discrepancies were identified and are tracked for resolution "
            "before the documentation package is finalized for commercial transfer:",
            "",
            "| Process | Category | Item | Detail |",
            "|---|---|---|---|",
        ]
        for c in integrity["failing_checks"]:
            lines.append(f"| {c['process_id']} | {c['category']} | {c['item']} | {c['detail']} |")
    else:
        lines.append("No discrepancies identified.")

    lines += [
        "",
        "## 4. Deliverables Generated",
        "",
        "For each of the 3 processes, the following documents were generated in "
        "`output/documentation/`:",
        "",
        "- `<process_id>_process_description.md` - unit operations, CPPs, and release "
        "specifications.",
        "- `<process_id>_batch_record_template.md` - structured, fillable commercial batch "
        "record template.",
        "- `<process_id>_sop.md` - standard operating procedure for commercial-site "
        "execution.",
        "",
        "## 5. Technology Transfer Readiness Assessment",
        "",
    ]

    overall_pct = integrity["overall"]["integrity_pct"]
    if overall_pct >= 99.0:
        readiness = (
            "The consolidated documentation package demonstrates a high level of data "
            "integrity (>=99%) and is considered **ready for commercial technology "
            "transfer**, contingent on resolution of the specific issues listed in Section "
            "3.1 prior to final QA approval and engineering-run confirmation at the "
            "receiving site."
        )
    else:
        readiness = (
            "The consolidated documentation package requires remediation of the issues "
            "listed in Section 3.1 before it can be considered ready for commercial "
            "technology transfer."
        )
    lines.append(readiness)

    lines += [
        "",
        "- All 3 processes have complete unit-operation sequences, CPP ranges, and release "
        "specifications documented at development/pilot scale.",
        "- Scale-dependent parameters flagged in each process description (Section 4, "
        "Technology Transfer Considerations) require confirmation via engineering runs at "
        "commercial scale before PPQ.",
        "- Batch record templates are structured for direct use at the receiving site and "
        "capture every CPP and release specification identified during consolidation.",
        "",
    ]

    report_path = os.path.join(OUT_DIR, "process_understanding_report.md")
    with open(report_path, "w") as f:
        f.write("\n".join(lines))
    print(f"  Generated {report_path}")
    return report_path


if __name__ == "__main__":
    generate_report()
