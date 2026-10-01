import copy
import json
import os
import sys

import pandas as pd
import pytest

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)

import simulate_process_data as sim  # noqa: E402
import consolidate  # noqa: E402
import generate_documents  # noqa: E402
import process_understanding_report as pur  # noqa: E402


@pytest.fixture(scope="module", autouse=True)
def ensure_pipeline_ran():
    sim.simulate()
    consolidate.consolidate()
    generate_documents.generate_documents()
    pur.generate_report()
    yield


def test_three_processes_present():
    assert set(sim.PROCESSES.keys()) == {"mAb-01", "ENZ-02", "VAX-03"}
    for pid in sim.PROCESSES:
        batch_path = os.path.join(sim.RAW_DIR, f"{pid}_batch_records.csv")
        desc_path = os.path.join(sim.RAW_DIR, f"{pid}_process_description.json")
        assert os.path.exists(batch_path)
        assert os.path.exists(desc_path)
        df = pd.read_csv(batch_path)
        assert len(df) == sim.N_BATCHES
        with open(desc_path) as f:
            desc = json.load(f)
        assert len(desc["unit_operations"]) >= 8
        assert len(desc["release_specifications"]) >= 7


def test_integrity_report_in_reasonable_band():
    with open(os.path.join("output", "integrity_report.json")) as f:
        report = json.load(f)
    overall_pct = report["overall"]["integrity_pct"]
    # Target is ~99.5%; allow a reasonable band around it since the pipeline
    # has 2 intentionally-injected documentation defects (see
    # simulate_process_data.py) plus whatever natural noise-driven
    # spec failures occur.
    assert 98.0 <= overall_pct <= 100.0
    assert report["overall"]["checks_run"] > 400
    assert report["overall"]["checks_failed"] >= 2  # the 2 injected defects, at minimum
    for pid in sim.PROCESSES:
        assert pid in report["by_process"]
        assert report["by_process"][pid]["checks_run"] > 0


def test_injected_defects_are_caught():
    """Sanity check: the deliberately-broken cross-reference (a release spec
    with no matching batch-record column) and the deliberately-broken
    completeness item (a unit-op missing its 'equipment' field) must both
    show up as failing checks, proving the integrity pipeline actually
    catches real inconsistencies rather than just reporting 100%."""
    with open(os.path.join("output", "integrity_report.json")) as f:
        report = json.load(f)
    failing_items = {c["item"] for c in report["failing_checks"]}
    assert "spec_to_batch_column.residual_antibiotic_ppm" in failing_items
    assert "unit_op_step_5.equipment" in failing_items


def test_deliberately_broken_cross_reference_is_detected_live():
    """Independent of the injected defects above, inject a fresh
    inconsistency into a copy of a process description (rename a release
    spec so it no longer matches any batch record column) and confirm
    consolidate.py's cross-reference check flags it as failing."""
    description, batch_df = consolidate._load("mAb-01")
    broken = copy.deepcopy(description)
    broken["release_specifications"]["totally_fabricated_attribute_xyz"] = {
        "spec": "<=1.0", "unit": "mg"
    }
    checks = []
    consolidate._check_cross_reference("mAb-01", broken, batch_df, checks)
    items = {c["item"]: c["passed"] for c in checks}
    assert items["spec_to_batch_column.totally_fabricated_attribute_xyz"] is False


def test_documents_generated_for_all_processes():
    for pid in sim.PROCESSES:
        for suffix in ["process_description", "batch_record_template", "sop"]:
            path = os.path.join("output", "documentation", f"{pid}_{suffix}.md")
            assert os.path.exists(path)
            with open(path) as f:
                content = f.read()
            assert len(content) > 500
            assert pid in content


def test_process_understanding_report_generated():
    path = os.path.join("output", "process_understanding_report.md")
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert "Process Understanding Report" in content
    assert "Data Integrity" in content
    for pid in sim.PROCESSES:
        assert pid in content
