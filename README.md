# TechTransferDocumentation: Process Development Documentation Consolidation

Consolidates documentation for **3 distinct manufacturing processes** -
a mammalian-cell mAb process, a microbial recombinant-enzyme process, and a
plasmid DNA downstream process - into comprehensive process description
documents, structured batch record templates, and SOPs, in preparation for
technology transfer from development/pilot scale to a commercial
manufacturing site. A real cross-source data-integrity pipeline validates
completeness, consistency, and cross-referencing across the documentation
and generates a Process Understanding Report summarizing tech-transfer
readiness.

> **Disclaimer:** This is a portfolio/demo project. All process parameters,
> unit operations, specifications, and batch data are **synthetically
> simulated** by `simulate_process_data.py`, built from general, published
> bioprocessing knowledge (typical CHO fed-batch, microbial fermentation,
> and plasmid DNA downstream unit operations). No real molecule, program,
> or employer data is used.

## Differentiation from the sibling `TechTransfer-Digitization-Workflows` project

This repo and `TechTransfer-Digitization-Workflows` both relate to tech
transfer but solve different problems and should not be confused:

| | This project (`TechTransferDocumentation`) | `TechTransfer-Digitization-Workflows` |
|---|---|---|
| Focus | **Documentation content**: process descriptions, batch record templates, SOPs, data-integrity review | **Software**: a React/Flask dashboard application |
| Deliverable | Markdown documents + an integrity/process-understanding report | A running web app (frontend + backend) |
| Problem solved | Is the tech-transfer documentation package complete, internally consistent, and ready to hand to a commercial site? | How does a user interact with digitized workflow data through a UI? |

## The 3 processes

| Process ID | Process | Modality | Dev/pilot scale | Target commercial scale |
|---|---|---|---|---|
| mAb-01 | Anti-TNF IgG1 mAb | Mammalian (CHO) fed-batch, Protein A capture + AEX/CEX polish | 200 L bioreactor | 2000 L |
| ENZ-02 | Recombinant industrial lipase | Microbial (E. coli), IPTG induction, IEX/HIC purification | 150 L fermenter | 3000 L |
| VAX-03 | Plasmid DNA drug substance | E. coli fermentation, alkaline lysis, AEX capture | 100 L fermenter | 1500 L |

Each process has its own distinct unit-operation sequence (9-10 steps),
critical process parameters, in-process controls, and release
specifications - these are not copies of a single template.

## What it does

1. **`simulate_process_data.py`** generates 10 dev-scale batch records per
   process plus a structured process description (unit operations, CPPs,
   release specs) per process, written to `data/raw/`. Two realistic
   documentation defects are deliberately left in (a release spec with no
   matching batch-record column on VAX-03; a unit operation missing its
   `equipment` field on mAb-01) so the integrity pipeline has something
   real to catch.

2. **`consolidate.py`** runs 3 categories of automated checks across all 3
   processes' documentation sources:
   - **Completeness** - every unit-op record has all required fields;
     every release spec has a limit and a unit.
   - **Consistency** - every batch record's measured value is checked
     against its process's own release specification (parsed from spec
     strings like `>=98.0`, `6.0-6.4`, `<=50`).
   - **Cross-reference** - every release spec maps to a batch-record data
     column, and every lot ID/process_id tag is internally consistent.

   Writes the full result, including every failing check, to
   `output/integrity_report.json`.

3. **`generate_documents.py`** generates, per process, a process
   description document, a structured fillable batch record template, and
   an SOP - all populated from the real simulated process data - into
   `output/documentation/`.

4. **`process_understanding_report.py`** generates the consolidated
   `output/process_understanding_report.md` summarizing the consolidation
   effort, the integrity findings, and tech-transfer readiness.

5. **`run_all.py`** runs the whole pipeline.

## How to run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run_all.py
pytest -q
```

## Results

_All numbers below are copied directly from an actual run of `python
run_all.py` - nothing is hardcoded. Fixed random seed makes them
reproducible._

- **490 automated checks** run across completeness, consistency, and
  cross-reference categories, spanning all 3 processes (29 unit operations,
  24 release specifications, 30 dev-scale batch records in total).
- **Overall data integrity: 99.388%** (487 of 490 checks passed), in line
  with the ~99.5% target for a tech-transfer-ready documentation package.
- Per process: mAb-01 163/164 (99.39%), ENZ-02 158/159 (99.371%),
  VAX-03 166/167 (99.401%).
- **3 failing checks identified**, exactly as expected for an honestly-run
  review rather than a package rounded up to 100%:
  1. mAb-01 Step 5 (Low pH Viral Inactivation) is missing its `equipment`
     field (completeness) - a deliberately-injected documentation defect.
  2. VAX-03's `residual_antibiotic_ppm` release spec has no corresponding
     batch-record column (cross-reference) - a deliberately-injected
     documentation defect from a downstream assay change that never made
     it into the batch record template.
  3. ENZ-02 lot `ENZ02-DEV-007`'s HCP result does not meet the `<=100 ppm`
     spec (consistency) - a naturally-occurring out-of-spec result from
     the simulated batch-to-batch variability, not an injected defect.
- `pytest -q` - **6 passed**, including a sanity check that the injected
  cross-reference and completeness defects are actually caught by
  `consolidate.py`, and a second, independent check that injecting a fresh
  fabricated release spec into a process description is also detected.
- 9 documentation files generated in `output/documentation/` (process
  description, batch record template, and SOP for each of the 3
  processes), plus `output/process_understanding_report.md` and
  `output/integrity_report.json`.
