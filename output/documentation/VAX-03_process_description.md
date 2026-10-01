# Process Description Document: Plasmid DNA Drug Substance - E. coli Fermentation & AEX Downstream Process

**Process ID:** VAX-03  
**Modality:** Plasmid DNA (pDNA) for gene therapy / vaccine applications  
**Development/Pilot Scale:** 5 L seed / 100 L production fermenter  
**Target Commercial Scale:** 1500 L production fermenter  
**Document Date:** 2026-09-30  
**Document Status:** Draft for Technology Transfer Review

## 1. Purpose

This document describes the manufacturing process for Plasmid DNA Drug Substance - E. coli Fermentation & AEX Downstream Process as executed at development/pilot scale, and establishes the process understanding basis for technology transfer to a commercial manufacturing site at 1500 L production fermenter.

## 2. Process Flow and Unit Operations

### Step 1: Seed Train Expansion

Glycerol stock to shake flask to 5 L seed fermenter, antibiotic-free selective medium.

**Equipment:** Shake flasks, 5 L stirred-tank fermenter

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| duration_hr | 12-14 |
| od600_target | 4-6 |
| temperature_c | 37.0 +/- 0.5 |

### Step 2: Production Fermentation (Fed-Batch)

100 L fed-batch fermentation to high cell density, non-antibiotic plasmid maintenance system.

**Equipment:** 100 L stainless steel fermenter

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| harvest_od600 | 80-100 |
| duration_hr | 16-18 |
| temperature_c | 37.0 +/- 0.5 |
| ph_setpoint | 7.00 +/- 0.10 |
| do_pct | 30 +/- 10 |

### Step 3: Cell Harvest (Centrifugation)

Continuous centrifugation to pellet cells for alkaline lysis.

**Equipment:** Disc-stack centrifuge

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| bowl_speed_rpm | 8000-10000 |

### Step 4: Alkaline Lysis & Neutralization

NaOH/SDS lysis followed by potassium acetate neutralization to precipitate genomic DNA and protein.

**Equipment:** In-line static mixer, hold tanks

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| lysis_time_min | 5 +/- 1 |
| neutralization_hold_time_min | 15-20 |
| lysate_temperature_c | 15-20 |

### Step 5: Clarification (Depth Filtration)

Depth filtration to remove precipitated gDNA/protein/cell debris flocs.

**Equipment:** Depth filter train

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| flux_lmh | 30-80 |
| max_turbidity_ntu_post | <=10 |

### Step 6: Endotoxin/RNA Reduction (Selective Precipitation)

Calcium chloride precipitation step to reduce residual RNA and endotoxin ahead of chromatography.

**Equipment:** Agitated precipitation vessel

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| cacl2_concentration_m | 0.3-0.5 |
| hold_time_min | 30-60 |

### Step 7: Anion Exchange Capture Chromatography

AEX bind-elute step, resolving supercoiled plasmid from open-circular/linear isoforms and RNA.

**Equipment:** Q resin column

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| load_mg_per_ml_resin | <=5 |
| gradient_nacl_m | 0.8-1.2 |

### Step 8: Size-Exclusion / Hydrophobic Polish

Polish step to further enrich supercoiled topology and remove residual HCP/endotoxin.

**Equipment:** SEC or HIC column

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| load_mg_per_ml_resin | <=3 |

### Step 9: Tangential Flow Filtration (Concentration/Diafiltration)

TFF to concentrate and exchange into final formulation buffer (TE or saline).

**Equipment:** Tangential flow filtration, 100-300 kDa MWCO

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| target_concentration_mg_ml | 2.0 +/- 0.2 |
| diavolumes | >=10 |

### Step 10: Sterile Filtration & Fill

0.2 um sterile filtration into final bulk containers.

**Equipment:** 0.2 um PES sterile filter

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| bioburden_cfu_per_100ml | <=1 |

## 3. Release Specifications

| Attribute | Specification | Unit |
|---|---|---|
| pct_supercoiled | >=85.0 | % |
| concentration_mg_ml | 1.8-2.2 | mg/mL |
| residual_gdna_pct | <=1.0 | % |
| residual_rna_pct | <=1.0 | % |
| residual_protein_ug_mg | <=2.0 | ug/mg |
| endotoxin_eu_per_mg | <=10.0 | EU/mg |
| bioburden_cfu_per_10ml | <=1 | CFU/10mL |
| identity_restriction_digest | conforms | pass/fail |
| residual_antibiotic_ppm | <=0.1 | ppm |

## 4. Technology Transfer Considerations

- Scale-dependent parameters (e.g. mixing times, mass transfer, column loading per resin volume) must be re-verified at commercial scale via engineering runs prior to process performance qualification (PPQ).
- All CPP ranges in Section 2 reflect development/pilot-scale operating experience and are the starting point for the commercial-scale control strategy; confirmation runs at the receiving site are required before these ranges are locked for PPQ.
- Release specifications in Section 3 are carried forward unchanged to the commercial site; any deviation requires change control.
