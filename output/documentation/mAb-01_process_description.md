# Process Description Document: Anti-TNF IgG1 Monoclonal Antibody - CHO Fed-Batch Process

**Process ID:** mAb-01  
**Modality:** Monoclonal antibody (IgG1)  
**Development/Pilot Scale:** 5 L (seed) / 200 L (production bioreactor)  
**Target Commercial Scale:** 2000 L production bioreactor  
**Document Date:** 2026-09-30  
**Document Status:** Draft for Technology Transfer Review

## 1. Purpose

This document describes the manufacturing process for Anti-TNF IgG1 Monoclonal Antibody - CHO Fed-Batch Process as executed at development/pilot scale, and establishes the process understanding basis for technology transfer to a commercial manufacturing site at 2000 L production bioreactor.

## 2. Process Flow and Unit Operations

### Step 1: Cell Thaw & Seed Train Expansion

Thaw WCB vial, expand through shake flasks and seed bioreactors (N-2, N-1) over 10-12 days to reach inoculation density.

**Equipment:** Shake flasks, 5 L single-use bioreactor

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| culture_duration_days | 10-12 |
| seed_viability_pct | >=95 |
| inoculation_vcd_e6_per_ml | 0.3-0.5 |

### Step 2: Production Bioreactor (Fed-Batch)

200 L fed-batch culture with daily glucose-controlled feed, 14-day run, temperature shift on day 7 to extend productivity.

**Equipment:** 200 L stainless steel bioreactor

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| temperature_c_phase1 | 37.0 +/- 0.5 |
| temperature_c_phase2 | 33.0 +/- 0.5 |
| ph_setpoint | 7.00 +/- 0.10 |
| do_pct | 40 +/- 10 |
| culture_duration_days | 14 |

### Step 3: Harvest Clarification

Depth filtration followed by 0.2 um sterile filtration to remove cells and debris.

**Equipment:** Depth filter train + 0.2 um PES filter

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| flux_lmh | 50-150 |
| max_turbidity_ntu_post | <=20 |

### Step 4: Protein A Capture Chromatography

MabSelect SuRe resin, bind-elute mode, low pH elution.

**Equipment:** Protein A column, 20 cm bed height

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| load_g_per_l_resin | <=35 |
| elution_ph | 3.5 +/- 0.2 |
| residence_time_min | 4-6 |

### Step 5: Low pH Viral Inactivation

Hold Protein A eluate at low pH for 60 min to inactivate enveloped viruses, then neutralize.

**Equipment:** **[MISSING - see integrity report]**

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| hold_ph | 3.6 +/- 0.1 |
| hold_time_min | >=60 |
| hold_temperature_c | 18-25 |

### Step 6: Anion Exchange Polish (Flow-Through)

AEX membrane/resin flow-through mode to remove HCP, DNA, and aggregates.

**Equipment:** Q membrane adsorber

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| load_g_per_l_resin | <=100 |
| conductivity_ms_cm | <=8 |

### Step 7: Cation Exchange Polish (Bind-Elute)

CEX bind-elute step to further remove HCP, leached Protein A, and charge variants.

**Equipment:** CEX resin column

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| load_g_per_l_resin | <=40 |
| gradient_nacl_mm | 0-300 |

### Step 8: Viral Filtration

Nanofiltration (20 nm pore) for robust parvovirus clearance.

**Equipment:** Virosart / Planova-type filter

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| max_flux_lmh | <=10 |
| max_pressure_bar | <=2.8 |

### Step 9: UF/DF Formulation

Ultrafiltration/diafiltration to target concentration and final formulation buffer.

**Equipment:** Tangential flow filtration, 30 kDa MWCO

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| target_concentration_mg_ml | 50 +/- 5 |
| diavolumes | >=8 |

### Step 10: Sterile Filtration & Fill

0.2 um sterile filtration into final bulk containers.

**Equipment:** 0.2 um PVDF sterile filter

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| bioburden_cfu_per_100ml | <=1 |

## 3. Release Specifications

| Attribute | Specification | Unit |
|---|---|---|
| titer_g_per_l | >=3.0 | g/L |
| purity_sec_pct_monomer | >=98.0 | % |
| hcp_ppm | <=50 | ppm |
| protein_a_ppm | <=5 | ppm |
| endotoxin_eu_per_mg | <=0.5 | EU/mg |
| bioburden_cfu_per_10ml | <=1 | CFU/10mL |
| ph_final | 6.0-6.4 | pH |
| osmolality_mosm_kg | 270-330 | mOsm/kg |

## 4. Technology Transfer Considerations

- Scale-dependent parameters (e.g. mixing times, mass transfer, column loading per resin volume) must be re-verified at commercial scale via engineering runs prior to process performance qualification (PPQ).
- All CPP ranges in Section 2 reflect development/pilot-scale operating experience and are the starting point for the commercial-scale control strategy; confirmation runs at the receiving site are required before these ranges are locked for PPQ.
- Release specifications in Section 3 are carried forward unchanged to the commercial site; any deviation requires change control.
