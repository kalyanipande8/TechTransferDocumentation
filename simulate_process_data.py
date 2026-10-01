"""
simulate_process_data.py

Simulates development/pilot-scale manufacturing process records for 3
distinct biomanufacturing processes slated for technology transfer to a
commercial site. Each process has its own unit-operation sequence,
critical process parameters (CPPs), in-process controls (IPCs), and
release specifications, reflecting real differences in modality/process
type rather than copies of the same template.

Processes:
  1. mAb-01   - Mammalian cell culture (CHO) mAb process: seed train,
                production bioreactor, Protein A capture, viral
                inactivation, AEX/CEX polish, UF/DF, sterile filtration.
  2. ENZ-02   - Microbial (E. coli) recombinant enzyme process: fermentation,
                cell lysis, homogenization, IEX capture, HIC polish,
                UF/DF, sterile filtration.
  3. VAX-03   - Plasmid DNA / viral-vector-adjacent downstream process:
                seed train, production bioreactor (suspension HEK293),
                lysis, nuclease digestion, AEX capture, tangential flow
                filtration, sterile filtration.

All data is synthetically generated with a fixed random seed for
reproducibility. No real molecule, program, or employer data is used.

Output: data/raw/<process_id>_batch_records.csv  (N batches per process)
        data/raw/<process_id>_process_description.json (unit ops, CPPs, specs)
"""

import json
import os
import random

import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

RAW_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

N_BATCHES = 10


def _noisy(center, pct_sd, n=N_BATCHES, lo=None, hi=None):
    vals = np.random.normal(center, center * pct_sd, n)
    if lo is not None:
        vals = np.clip(vals, lo, None)
    if hi is not None:
        vals = np.clip(vals, None, hi)
    return vals


# ---------------------------------------------------------------------------
# Process 1: mAb-01 - CHO cell culture mAb process
# ---------------------------------------------------------------------------

MAB01_DESCRIPTION = {
    "process_id": "mAb-01",
    "process_name": "Anti-TNF IgG1 Monoclonal Antibody - CHO Fed-Batch Process",
    "modality": "Monoclonal antibody (IgG1)",
    "development_scale": "5 L (seed) / 200 L (production bioreactor)",
    "target_commercial_scale": "2000 L production bioreactor",
    "unit_operations": [
        {
            "step": 1, "name": "Cell Thaw & Seed Train Expansion",
            "description": "Thaw WCB vial, expand through shake flasks and seed bioreactors (N-2, N-1) over 10-12 days to reach inoculation density.",
            "equipment": "Shake flasks, 5 L single-use bioreactor",
            "cpps": {"culture_duration_days": "10-12", "seed_viability_pct": ">=95", "inoculation_vcd_e6_per_ml": "0.3-0.5"},
        },
        {
            "step": 2, "name": "Production Bioreactor (Fed-Batch)",
            "description": "200 L fed-batch culture with daily glucose-controlled feed, 14-day run, temperature shift on day 7 to extend productivity.",
            "equipment": "200 L stainless steel bioreactor",
            "cpps": {"temperature_c_phase1": "37.0 +/- 0.5", "temperature_c_phase2": "33.0 +/- 0.5",
                     "ph_setpoint": "7.00 +/- 0.10", "do_pct": "40 +/- 10", "culture_duration_days": 14},
        },
        {
            "step": 3, "name": "Harvest Clarification",
            "description": "Depth filtration followed by 0.2 um sterile filtration to remove cells and debris.",
            "equipment": "Depth filter train + 0.2 um PES filter",
            "cpps": {"flux_lmh": "50-150", "max_turbidity_ntu_post": "<=20"},
        },
        {
            "step": 4, "name": "Protein A Capture Chromatography",
            "description": "MabSelect SuRe resin, bind-elute mode, low pH elution.",
            "equipment": "Protein A column, 20 cm bed height",
            "cpps": {"load_g_per_l_resin": "<=35", "elution_ph": "3.5 +/- 0.2", "residence_time_min": "4-6"},
        },
        {
            # NOTE (intentional data-integrity defect, left in for the
            # consolidation pipeline's completeness check to catch): the
            # "equipment" field was dropped from this unit-op record during
            # the last process description revision.
            "step": 5, "name": "Low pH Viral Inactivation",
            "description": "Hold Protein A eluate at low pH for 60 min to inactivate enveloped viruses, then neutralize.",
            "cpps": {"hold_ph": "3.6 +/- 0.1", "hold_time_min": ">=60", "hold_temperature_c": "18-25"},
        },
        {
            "step": 6, "name": "Anion Exchange Polish (Flow-Through)",
            "description": "AEX membrane/resin flow-through mode to remove HCP, DNA, and aggregates.",
            "equipment": "Q membrane adsorber",
            "cpps": {"load_g_per_l_resin": "<=100", "conductivity_ms_cm": "<=8"},
        },
        {
            "step": 7, "name": "Cation Exchange Polish (Bind-Elute)",
            "description": "CEX bind-elute step to further remove HCP, leached Protein A, and charge variants.",
            "equipment": "CEX resin column",
            "cpps": {"load_g_per_l_resin": "<=40", "gradient_nacl_mm": "0-300"},
        },
        {
            "step": 8, "name": "Viral Filtration",
            "description": "Nanofiltration (20 nm pore) for robust parvovirus clearance.",
            "equipment": "Virosart / Planova-type filter",
            "cpps": {"max_flux_lmh": "<=10", "max_pressure_bar": "<=2.8"},
        },
        {
            "step": 9, "name": "UF/DF Formulation",
            "description": "Ultrafiltration/diafiltration to target concentration and final formulation buffer.",
            "equipment": "Tangential flow filtration, 30 kDa MWCO",
            "cpps": {"target_concentration_mg_ml": "50 +/- 5", "diavolumes": ">=8"},
        },
        {
            "step": 10, "name": "Sterile Filtration & Fill",
            "description": "0.2 um sterile filtration into final bulk containers.",
            "equipment": "0.2 um PVDF sterile filter",
            "cpps": {"bioburden_cfu_per_100ml": "<=1"},
        },
    ],
    "release_specifications": {
        "titer_g_per_l": {"spec": ">=3.0", "unit": "g/L"},
        "purity_sec_pct_monomer": {"spec": ">=98.0", "unit": "%"},
        "hcp_ppm": {"spec": "<=50", "unit": "ppm"},
        "protein_a_ppm": {"spec": "<=5", "unit": "ppm"},
        "endotoxin_eu_per_mg": {"spec": "<=0.5", "unit": "EU/mg"},
        "bioburden_cfu_per_10ml": {"spec": "<=1", "unit": "CFU/10mL"},
        "ph_final": {"spec": "6.0-6.4", "unit": "pH"},
        "osmolality_mosm_kg": {"spec": "270-330", "unit": "mOsm/kg"},
    },
}


def _simulate_mab01():
    lots = [f"mAb01-DEV-{i+1:03d}" for i in range(N_BATCHES)]
    df = pd.DataFrame({
        "lot_id": lots,
        "process_id": "mAb-01",
        "titer_g_per_l": np.round(_noisy(3.6, 0.08, lo=2.5), 2),
        "purity_sec_pct_monomer": np.round(_noisy(98.8, 0.004, hi=99.9), 2),
        "hcp_ppm": np.round(_noisy(28, 0.25, lo=1), 1),
        "protein_a_ppm": np.round(_noisy(2.1, 0.3, lo=0.1), 2),
        "endotoxin_eu_per_mg": np.round(_noisy(0.18, 0.3, lo=0.01), 3),
        "bioburden_cfu_per_10ml": np.zeros(N_BATCHES, dtype=int),
        "ph_final": np.round(_noisy(6.2, 0.01), 2),
        "osmolality_mosm_kg": np.round(_noisy(300, 0.03), 0),
        "viral_inactivation_hold_time_min": np.round(_noisy(65, 0.05, lo=60), 1),
        "culture_duration_days": 14,
    })
    return df


# ---------------------------------------------------------------------------
# Process 2: ENZ-02 - E. coli recombinant enzyme process
# ---------------------------------------------------------------------------

ENZ02_DESCRIPTION = {
    "process_id": "ENZ-02",
    "process_name": "Recombinant Industrial Lipase - E. coli Fermentation Process",
    "modality": "Recombinant enzyme (microbial, intracellular inclusion-body-free)",
    "development_scale": "10 L seed fermenter / 150 L production fermenter",
    "target_commercial_scale": "3000 L production fermenter",
    "unit_operations": [
        {
            "step": 1, "name": "Seed Fermentation",
            "description": "Shake flask to 10 L seed fermenter expansion, 16-18 hr, OD600 target reached before transfer.",
            "equipment": "Shake flasks, 10 L stirred-tank fermenter",
            "cpps": {"duration_hr": "16-18", "od600_target": "8-12", "temperature_c": "37.0 +/- 0.5"},
        },
        {
            "step": 2, "name": "Production Fermentation (Fed-Batch, IPTG Induction)",
            "description": "150 L fed-batch fermentation with glycerol feed; IPTG induction at mid-log phase for recombinant expression.",
            "equipment": "150 L stainless steel fermenter",
            "cpps": {"induction_od600": "40-60", "iptg_concentration_mm": "0.5 +/- 0.1",
                     "post_induction_duration_hr": "18-20", "temperature_c_post_induction": "25.0 +/- 0.5",
                     "do_pct": "30 +/- 10", "ph_setpoint": "6.80 +/- 0.10"},
        },
        {
            "step": 3, "name": "Cell Harvest (Centrifugation)",
            "description": "Continuous centrifugation to pellet cells; resuspend in lysis buffer.",
            "equipment": "Disc-stack centrifuge",
            "cpps": {"bowl_speed_rpm": "8000-10000", "feed_flow_lpm": "5-10"},
        },
        {
            "step": 4, "name": "High-Pressure Homogenization (Lysis)",
            "description": "Two passes through high-pressure homogenizer to lyse cells and release soluble enzyme.",
            "equipment": "High-pressure homogenizer",
            "cpps": {"pressure_bar": "800-1000", "passes": 2, "post_lysis_temperature_c": "<=15"},
        },
        {
            "step": 5, "name": "Clarification (Depth Filtration)",
            "description": "Depth filtration to remove cell debris from lysate.",
            "equipment": "Depth filter train",
            "cpps": {"flux_lmh": "40-120", "max_turbidity_ntu_post": "<=15"},
        },
        {
            "step": 6, "name": "Anion Exchange Capture",
            "description": "IEX bind-elute capture step exploiting target enzyme's acidic pI.",
            "equipment": "Q Sepharose column",
            "cpps": {"load_g_per_l_resin": "<=25", "gradient_nacl_mm": "50-400"},
        },
        {
            "step": 7, "name": "Hydrophobic Interaction Chromatography Polish",
            "description": "HIC step to remove host cell protein and aggregated species.",
            "equipment": "Phenyl Sepharose column",
            "cpps": {"load_ammonium_sulfate_m": "1.0-1.2", "load_g_per_l_resin": "<=20"},
        },
        {
            "step": 8, "name": "UF/DF Formulation",
            "description": "Ultrafiltration/diafiltration into final storage buffer with stabilizing excipients.",
            "equipment": "Tangential flow filtration, 10 kDa MWCO",
            "cpps": {"target_concentration_mg_ml": "20 +/- 2", "diavolumes": ">=6"},
        },
        {
            "step": 9, "name": "Sterile Filtration & Fill",
            "description": "0.2 um sterile filtration into final bulk containers.",
            "equipment": "0.2 um PES sterile filter",
            "cpps": {"bioburden_cfu_per_100ml": "<=1"},
        },
    ],
    "release_specifications": {
        "specific_activity_u_per_mg": {"spec": ">=800", "unit": "U/mg"},
        "purity_sds_page_pct": {"spec": ">=95.0", "unit": "%"},
        "hcp_ppm": {"spec": "<=100", "unit": "ppm"},
        "residual_dna_pg_per_mg": {"spec": "<=10", "unit": "pg/mg"},
        "endotoxin_eu_per_mg": {"spec": "<=5.0", "unit": "EU/mg"},
        "bioburden_cfu_per_10ml": {"spec": "<=1", "unit": "CFU/10mL"},
        "ph_final": {"spec": "7.0-7.4", "unit": "pH"},
        "moisture_content_pct": {"spec": "<=5.0", "unit": "%"},
    },
}


def _simulate_enz02():
    lots = [f"ENZ02-DEV-{i+1:03d}" for i in range(N_BATCHES)]
    df = pd.DataFrame({
        "lot_id": lots,
        "process_id": "ENZ-02",
        "specific_activity_u_per_mg": np.round(_noisy(950, 0.07, lo=700), 0),
        "purity_sds_page_pct": np.round(_noisy(96.5, 0.01, hi=99.5), 2),
        "hcp_ppm": np.round(_noisy(65, 0.3, lo=5), 1),
        "residual_dna_pg_per_mg": np.round(_noisy(4.5, 0.35, lo=0.1), 2),
        "endotoxin_eu_per_mg": np.round(_noisy(1.8, 0.3, lo=0.05), 3),
        "bioburden_cfu_per_10ml": np.zeros(N_BATCHES, dtype=int),
        "ph_final": np.round(_noisy(7.2, 0.008), 2),
        "moisture_content_pct": np.round(_noisy(3.2, 0.15, lo=0.5), 2),
        "induction_od600": np.round(_noisy(50, 0.1, lo=35), 1),
        "post_induction_duration_hr": np.round(_noisy(19, 0.04, lo=16), 1),
    })
    return df


# ---------------------------------------------------------------------------
# Process 3: VAX-03 - Plasmid DNA downstream process (HEK293 suspension)
# ---------------------------------------------------------------------------

VAX03_DESCRIPTION = {
    "process_id": "VAX-03",
    "process_name": "Plasmid DNA Drug Substance - E. coli Fermentation & AEX Downstream Process",
    "modality": "Plasmid DNA (pDNA) for gene therapy / vaccine applications",
    "development_scale": "5 L seed / 100 L production fermenter",
    "target_commercial_scale": "1500 L production fermenter",
    "unit_operations": [
        {
            "step": 1, "name": "Seed Train Expansion",
            "description": "Glycerol stock to shake flask to 5 L seed fermenter, antibiotic-free selective medium.",
            "equipment": "Shake flasks, 5 L stirred-tank fermenter",
            "cpps": {"duration_hr": "12-14", "od600_target": "4-6", "temperature_c": "37.0 +/- 0.5"},
        },
        {
            "step": 2, "name": "Production Fermentation (Fed-Batch)",
            "description": "100 L fed-batch fermentation to high cell density, non-antibiotic plasmid maintenance system.",
            "equipment": "100 L stainless steel fermenter",
            "cpps": {"harvest_od600": "80-100", "duration_hr": "16-18",
                     "temperature_c": "37.0 +/- 0.5", "ph_setpoint": "7.00 +/- 0.10", "do_pct": "30 +/- 10"},
        },
        {
            "step": 3, "name": "Cell Harvest (Centrifugation)",
            "description": "Continuous centrifugation to pellet cells for alkaline lysis.",
            "equipment": "Disc-stack centrifuge",
            "cpps": {"bowl_speed_rpm": "8000-10000"},
        },
        {
            "step": 4, "name": "Alkaline Lysis & Neutralization",
            "description": "NaOH/SDS lysis followed by potassium acetate neutralization to precipitate genomic DNA and protein.",
            "equipment": "In-line static mixer, hold tanks",
            "cpps": {"lysis_time_min": "5 +/- 1", "neutralization_hold_time_min": "15-20", "lysate_temperature_c": "15-20"},
        },
        {
            "step": 5, "name": "Clarification (Depth Filtration)",
            "description": "Depth filtration to remove precipitated gDNA/protein/cell debris flocs.",
            "equipment": "Depth filter train",
            "cpps": {"flux_lmh": "30-80", "max_turbidity_ntu_post": "<=10"},
        },
        {
            "step": 6, "name": "Endotoxin/RNA Reduction (Selective Precipitation)",
            "description": "Calcium chloride precipitation step to reduce residual RNA and endotoxin ahead of chromatography.",
            "equipment": "Agitated precipitation vessel",
            "cpps": {"cacl2_concentration_m": "0.3-0.5", "hold_time_min": "30-60"},
        },
        {
            "step": 7, "name": "Anion Exchange Capture Chromatography",
            "description": "AEX bind-elute step, resolving supercoiled plasmid from open-circular/linear isoforms and RNA.",
            "equipment": "Q resin column",
            "cpps": {"load_mg_per_ml_resin": "<=5", "gradient_nacl_m": "0.8-1.2"},
        },
        {
            "step": 8, "name": "Size-Exclusion / Hydrophobic Polish",
            "description": "Polish step to further enrich supercoiled topology and remove residual HCP/endotoxin.",
            "equipment": "SEC or HIC column",
            "cpps": {"load_mg_per_ml_resin": "<=3"},
        },
        {
            "step": 9, "name": "Tangential Flow Filtration (Concentration/Diafiltration)",
            "description": "TFF to concentrate and exchange into final formulation buffer (TE or saline).",
            "equipment": "Tangential flow filtration, 100-300 kDa MWCO",
            "cpps": {"target_concentration_mg_ml": "2.0 +/- 0.2", "diavolumes": ">=10"},
        },
        {
            "step": 10, "name": "Sterile Filtration & Fill",
            "description": "0.2 um sterile filtration into final bulk containers.",
            "equipment": "0.2 um PES sterile filter",
            "cpps": {"bioburden_cfu_per_100ml": "<=1"},
        },
    ],
    "release_specifications": {
        "pct_supercoiled": {"spec": ">=85.0", "unit": "%"},
        "concentration_mg_ml": {"spec": "1.8-2.2", "unit": "mg/mL"},
        "residual_gdna_pct": {"spec": "<=1.0", "unit": "%"},
        "residual_rna_pct": {"spec": "<=1.0", "unit": "%"},
        "residual_protein_ug_mg": {"spec": "<=2.0", "unit": "ug/mg"},
        "endotoxin_eu_per_mg": {"spec": "<=10.0", "unit": "EU/mg"},
        "bioburden_cfu_per_10ml": {"spec": "<=1", "unit": "CFU/10mL"},
        "identity_restriction_digest": {"spec": "conforms", "unit": "pass/fail"},
        # NOTE (intentional data-integrity defect, left in for the
        # consolidation pipeline's cross-reference check to catch): this
        # spec was added to the process description during a downstream
        # assay change but the corresponding batch record column was never
        # added to the batch record template. consolidate.py's
        # spec-to-batch-record cross-reference check flags this.
        "residual_antibiotic_ppm": {"spec": "<=0.1", "unit": "ppm"},
    },
}


def _simulate_vax03():
    lots = [f"VAX03-DEV-{i+1:03d}" for i in range(N_BATCHES)]
    df = pd.DataFrame({
        "lot_id": lots,
        "process_id": "VAX-03",
        "pct_supercoiled": np.round(_noisy(90.5, 0.02, hi=98.0), 2),
        "concentration_mg_ml": np.round(_noisy(2.0, 0.03), 2),
        "residual_gdna_pct": np.round(_noisy(0.4, 0.3, lo=0.01), 3),
        "residual_rna_pct": np.round(_noisy(0.35, 0.3, lo=0.01), 3),
        "residual_protein_ug_mg": np.round(_noisy(0.9, 0.3, lo=0.05), 3),
        "endotoxin_eu_per_mg": np.round(_noisy(4.5, 0.25, lo=0.1), 2),
        "bioburden_cfu_per_10ml": np.zeros(N_BATCHES, dtype=int),
        "identity_restriction_digest": ["conforms"] * N_BATCHES,
        "harvest_od600": np.round(_noisy(90, 0.05, lo=80), 1),
        "duration_hr": np.round(_noisy(17, 0.03, lo=16), 1),
    })
    return df


PROCESSES = {
    "mAb-01": {"description": MAB01_DESCRIPTION, "simulate": _simulate_mab01},
    "ENZ-02": {"description": ENZ02_DESCRIPTION, "simulate": _simulate_enz02},
    "VAX-03": {"description": VAX03_DESCRIPTION, "simulate": _simulate_vax03},
}


def simulate():
    for pid, pconf in PROCESSES.items():
        df = pconf["simulate"]()
        batch_path = os.path.join(RAW_DIR, f"{pid}_batch_records.csv")
        df.to_csv(batch_path, index=False)

        desc_path = os.path.join(RAW_DIR, f"{pid}_process_description.json")
        with open(desc_path, "w") as f:
            json.dump(pconf["description"], f, indent=2)

        print(f"  {pid}: {len(df)} dev-scale batch records -> {batch_path}")
        print(f"  {pid}: process description ({len(pconf['description']['unit_operations'])} unit ops) -> {desc_path}")


if __name__ == "__main__":
    simulate()
