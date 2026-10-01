# Process Description Document: Recombinant Industrial Lipase - E. coli Fermentation Process

**Process ID:** ENZ-02  
**Modality:** Recombinant enzyme (microbial, intracellular inclusion-body-free)  
**Development/Pilot Scale:** 10 L seed fermenter / 150 L production fermenter  
**Target Commercial Scale:** 3000 L production fermenter  
**Document Date:** 2026-09-30  
**Document Status:** Draft for Technology Transfer Review

## 1. Purpose

This document describes the manufacturing process for Recombinant Industrial Lipase - E. coli Fermentation Process as executed at development/pilot scale, and establishes the process understanding basis for technology transfer to a commercial manufacturing site at 3000 L production fermenter.

## 2. Process Flow and Unit Operations

### Step 1: Seed Fermentation

Shake flask to 10 L seed fermenter expansion, 16-18 hr, OD600 target reached before transfer.

**Equipment:** Shake flasks, 10 L stirred-tank fermenter

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| duration_hr | 16-18 |
| od600_target | 8-12 |
| temperature_c | 37.0 +/- 0.5 |

### Step 2: Production Fermentation (Fed-Batch, IPTG Induction)

150 L fed-batch fermentation with glycerol feed; IPTG induction at mid-log phase for recombinant expression.

**Equipment:** 150 L stainless steel fermenter

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| induction_od600 | 40-60 |
| iptg_concentration_mm | 0.5 +/- 0.1 |
| post_induction_duration_hr | 18-20 |
| temperature_c_post_induction | 25.0 +/- 0.5 |
| do_pct | 30 +/- 10 |
| ph_setpoint | 6.80 +/- 0.10 |

### Step 3: Cell Harvest (Centrifugation)

Continuous centrifugation to pellet cells; resuspend in lysis buffer.

**Equipment:** Disc-stack centrifuge

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| bowl_speed_rpm | 8000-10000 |
| feed_flow_lpm | 5-10 |

### Step 4: High-Pressure Homogenization (Lysis)

Two passes through high-pressure homogenizer to lyse cells and release soluble enzyme.

**Equipment:** High-pressure homogenizer

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| pressure_bar | 800-1000 |
| passes | 2 |
| post_lysis_temperature_c | <=15 |

### Step 5: Clarification (Depth Filtration)

Depth filtration to remove cell debris from lysate.

**Equipment:** Depth filter train

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| flux_lmh | 40-120 |
| max_turbidity_ntu_post | <=15 |

### Step 6: Anion Exchange Capture

IEX bind-elute capture step exploiting target enzyme's acidic pI.

**Equipment:** Q Sepharose column

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| load_g_per_l_resin | <=25 |
| gradient_nacl_mm | 50-400 |

### Step 7: Hydrophobic Interaction Chromatography Polish

HIC step to remove host cell protein and aggregated species.

**Equipment:** Phenyl Sepharose column

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| load_ammonium_sulfate_m | 1.0-1.2 |
| load_g_per_l_resin | <=20 |

### Step 8: UF/DF Formulation

Ultrafiltration/diafiltration into final storage buffer with stabilizing excipients.

**Equipment:** Tangential flow filtration, 10 kDa MWCO

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| target_concentration_mg_ml | 20 +/- 2 |
| diavolumes | >=6 |

### Step 9: Sterile Filtration & Fill

0.2 um sterile filtration into final bulk containers.

**Equipment:** 0.2 um PES sterile filter

**Critical Process Parameters (CPPs):**

| Parameter | Target / Limit |
|---|---|
| bioburden_cfu_per_100ml | <=1 |

## 3. Release Specifications

| Attribute | Specification | Unit |
|---|---|---|
| specific_activity_u_per_mg | >=800 | U/mg |
| purity_sds_page_pct | >=95.0 | % |
| hcp_ppm | <=100 | ppm |
| residual_dna_pg_per_mg | <=10 | pg/mg |
| endotoxin_eu_per_mg | <=5.0 | EU/mg |
| bioburden_cfu_per_10ml | <=1 | CFU/10mL |
| ph_final | 7.0-7.4 | pH |
| moisture_content_pct | <=5.0 | % |

## 4. Technology Transfer Considerations

- Scale-dependent parameters (e.g. mixing times, mass transfer, column loading per resin volume) must be re-verified at commercial scale via engineering runs prior to process performance qualification (PPQ).
- All CPP ranges in Section 2 reflect development/pilot-scale operating experience and are the starting point for the commercial-scale control strategy; confirmation runs at the receiving site are required before these ranges are locked for PPQ.
- Release specifications in Section 3 are carried forward unchanged to the commercial site; any deviation requires change control.
