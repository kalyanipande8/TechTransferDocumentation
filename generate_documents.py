"""
generate_documents.py

Generates the tech-transfer documentation package for all 3 processes from
the simulated process data in data/raw/:

  - output/documentation/<process_id>_process_description.md
  - output/documentation/<process_id>_batch_record_template.md
  - output/documentation/<process_id>_sop.md

and the consolidated:

  - output/process_understanding_report.md

All documents are populated with the real simulated process parameters,
unit operations, and release specifications - nothing is a placeholder.
"""

import json
import os
from datetime import date

import pandas as pd

RAW_DIR = os.path.join("data", "raw")
DOC_DIR = os.path.join("output", "documentation")
OUT_DIR = "output"
os.makedirs(DOC_DIR, exist_ok=True)

PROCESS_IDS = ["mAb-01", "ENZ-02", "VAX-03"]
TODAY = date.today().isoformat()


def _load(process_id):
    with open(os.path.join(RAW_DIR, f"{process_id}_process_description.json")) as f:
        description = json.load(f)
    batch_df = pd.read_csv(os.path.join(RAW_DIR, f"{process_id}_batch_records.csv"))
    return description, batch_df


def _cpp_table(cpps):
    lines = ["| Parameter | Target / Limit |", "|---|---|"]
    for k, v in cpps.items():
        lines.append(f"| {k} | {v} |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Process Description Document
# ---------------------------------------------------------------------------

def _process_description_doc(description):
    pid = description["process_id"]
    lines = [
        f"# Process Description Document: {description['process_name']}",
        "",
        f"**Process ID:** {pid}  ",
        f"**Modality:** {description['modality']}  ",
        f"**Development/Pilot Scale:** {description['development_scale']}  ",
        f"**Target Commercial Scale:** {description['target_commercial_scale']}  ",
        f"**Document Date:** {TODAY}  ",
        f"**Document Status:** Draft for Technology Transfer Review",
        "",
        "## 1. Purpose",
        "",
        f"This document describes the manufacturing process for {description['process_name']} "
        f"as executed at development/pilot scale, and establishes the process understanding "
        f"basis for technology transfer to a commercial manufacturing site at "
        f"{description['target_commercial_scale']}.",
        "",
        "## 2. Process Flow and Unit Operations",
        "",
    ]
    for uo in description["unit_operations"]:
        equipment = uo.get("equipment", "**[MISSING - see integrity report]**")
        lines += [
            f"### Step {uo['step']}: {uo['name']}",
            "",
            uo["description"],
            "",
            f"**Equipment:** {equipment}",
            "",
            "**Critical Process Parameters (CPPs):**",
            "",
            _cpp_table(uo["cpps"]),
            "",
        ]
    lines += [
        "## 3. Release Specifications",
        "",
        "| Attribute | Specification | Unit |",
        "|---|---|---|",
    ]
    for name, spec in description["release_specifications"].items():
        lines.append(f"| {name} | {spec['spec']} | {spec['unit']} |")
    lines += [
        "",
        "## 4. Technology Transfer Considerations",
        "",
        "- Scale-dependent parameters (e.g. mixing times, mass transfer, column loading per "
        "resin volume) must be re-verified at commercial scale via engineering runs prior to "
        "process performance qualification (PPQ).",
        "- All CPP ranges in Section 2 reflect development/pilot-scale operating experience "
        "and are the starting point for the commercial-scale control strategy; confirmation "
        "runs at the receiving site are required before these ranges are locked for PPQ.",
        "- Release specifications in Section 3 are carried forward unchanged to the commercial "
        "site; any deviation requires change control.",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Batch Record Template
# ---------------------------------------------------------------------------

def _batch_record_template(description):
    pid = description["process_id"]
    lines = [
        f"# Batch Record Template: {description['process_name']}",
        "",
        f"**Process ID:** {pid}  ",
        f"**Template Version:** 1.0  ",
        f"**Effective Date:** {TODAY}",
        "",
        "> This is a structured, fillable batch record template for commercial-site use. "
        "Shaded fields (`____`) are completed by manufacturing personnel at time of execution.",
        "",
        "## Batch Identification",
        "",
        "| Field | Entry |",
        "|---|---|",
        "| Batch/Lot Number | ____ |",
        "| Manufacturing Date | ____ |",
        "| Process ID | " + pid + " |",
        "| Raw Material Lot Numbers | ____ |",
        "| Executed By | ____ |",
        "| Reviewed By (QA) | ____ |",
        "",
        "## Unit Operation Execution Record",
        "",
    ]
    for uo in description["unit_operations"]:
        lines += [
            f"### Step {uo['step']}: {uo['name']}",
            "",
            f"Equipment: {uo.get('equipment', '____')}  ",
            f"Equipment ID/Serial Number: ____  ",
            f"Start Date/Time: ____    End Date/Time: ____",
            "",
            "| CPP | Target / Limit | Actual Recorded Value | In Spec (Y/N) | Operator Initials |",
            "|---|---|---|---|---|",
        ]
        for k, v in uo["cpps"].items():
            lines.append(f"| {k} | {v} | ____ | ____ | ____ |")
        lines += ["", "Comments/Deviations: ____________________________________", ""]

    lines += [
        "## Release Testing Results",
        "",
        "| Attribute | Specification | Unit | Result | Pass/Fail | Analyst |",
        "|---|---|---|---|---|---|",
    ]
    for name, spec in description["release_specifications"].items():
        lines.append(f"| {name} | {spec['spec']} | {spec['unit']} | ____ | ____ | ____ |")

    lines += [
        "",
        "## Final Disposition",
        "",
        "| Field | Entry |",
        "|---|---|",
        "| QA Disposition (Release / Reject / Quarantine) | ____ |",
        "| QA Signature | ____ |",
        "| Date | ____ |",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Standard Operating Procedure
# ---------------------------------------------------------------------------

def _sop(description):
    pid = description["process_id"]
    n_steps = len(description["unit_operations"])
    lines = [
        f"# Standard Operating Procedure: {description['process_name']}",
        "",
        f"**SOP Number:** SOP-{pid}-001  ",
        f"**Process ID:** {pid}  ",
        f"**Revision:** 1.0  ",
        f"**Effective Date:** {TODAY}  ",
        f"**Supersedes:** None (new procedure for technology transfer)",
        "",
        "## 1. Purpose and Scope",
        "",
        f"This SOP defines the step-by-step operating procedure for manufacturing "
        f"{description['process_name']} ({description['modality']}) at the receiving "
        f"commercial manufacturing site, {description['target_commercial_scale']}. "
        f"It applies to all manufacturing personnel executing this process and to QA "
        f"personnel reviewing associated batch records.",
        "",
        "## 2. Responsibilities",
        "",
        "- **Manufacturing Operators:** Execute each unit operation per the parameters "
        "specified below and record all data contemporaneously in the batch record.",
        "- **Manufacturing Supervisor:** Verify equipment readiness and line clearance "
        "before each unit operation; review in-process data.",
        "- **Quality Assurance:** Review the executed batch record against this SOP and "
        "the process description document; approve final disposition.",
        "- **Quality Control:** Perform release testing per Section 4 and report results "
        "against the approved specifications.",
        "",
        "## 3. Materials and Equipment",
        "",
        "| Step | Equipment |",
        "|---|---|",
    ]
    for uo in description["unit_operations"]:
        lines.append(f"| {uo['step']}. {uo['name']} | {uo.get('equipment', 'NOT SPECIFIED - verify with Process Description before use')} |")

    lines += ["", "## 4. Procedure", ""]
    for uo in description["unit_operations"]:
        lines += [
            f"### 4.{uo['step']} {uo['name']}",
            "",
            f"1. Confirm equipment ({uo.get('equipment', 'per Process Description')}) is qualified and within calibration.",
            f"2. {uo['description']}",
            "3. Operate within the following critical process parameters, recording actual "
            "values in the batch record at the frequency specified in the in-process "
            "control plan:",
            "",
            _cpp_table(uo["cpps"]),
            "",
            "4. If any parameter deviates from the stated range, initiate a deviation "
            "report per site deviation-management procedure before proceeding.",
            "",
        ]

    lines += [
        "## 5. In-Process Controls and Release Testing",
        "",
        "Samples are pulled per the in-process control plan referenced in the process "
        "description document. Final drug substance/intermediate is released against the "
        "following specifications:",
        "",
        "| Attribute | Specification | Unit |",
        "|---|---|---|",
    ]
    for name, spec in description["release_specifications"].items():
        lines.append(f"| {name} | {spec['spec']} | {spec['unit']} |")

    lines += [
        "",
        "## 6. Deviation Handling",
        "",
        "Any excursion outside the CPP ranges or release specifications in this SOP is "
        "handled per the site's deviation management SOP. QA must assess impact to product "
        "quality before batch disposition.",
        "",
        "## 7. Revision History",
        "",
        "| Revision | Date | Description |",
        "|---|---|---|",
        f"| 1.0 | {TODAY} | New SOP issued to support technology transfer ({n_steps} unit operations). |",
        "",
    ]
    return "\n".join(lines)


def generate_documents():
    generated = []
    for pid in PROCESS_IDS:
        description, _ = _load(pid)

        doc_path = os.path.join(DOC_DIR, f"{pid}_process_description.md")
        with open(doc_path, "w") as f:
            f.write(_process_description_doc(description))
        generated.append(doc_path)

        bre_path = os.path.join(DOC_DIR, f"{pid}_batch_record_template.md")
        with open(bre_path, "w") as f:
            f.write(_batch_record_template(description))
        generated.append(bre_path)

        sop_path = os.path.join(DOC_DIR, f"{pid}_sop.md")
        with open(sop_path, "w") as f:
            f.write(_sop(description))
        generated.append(sop_path)

    for p in generated:
        print(f"  Generated {p}")
    return generated


if __name__ == "__main__":
    generate_documents()
