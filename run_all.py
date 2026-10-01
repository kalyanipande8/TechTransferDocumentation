"""
run_all.py

Runs the full tech-transfer documentation pipeline end-to-end:
  1. Simulate dev/pilot-scale process data for 3 manufacturing processes -> data/raw/
  2. Consolidate + validate data integrity across the 3 processes -> output/integrity_report.json
  3. Generate process description docs, batch record templates, and SOPs -> output/documentation/
  4. Generate the consolidated process understanding report -> output/process_understanding_report.md

Run with:  python run_all.py
"""

import simulate_process_data
import consolidate
import generate_documents
import process_understanding_report


def main():
    print("--- Simulating dev/pilot-scale process data for 3 processes ---")
    simulate_process_data.simulate()

    print("\n--- Consolidating documentation & validating data integrity ---")
    consolidate.consolidate()

    print("\n--- Generating process descriptions, batch record templates, and SOPs ---")
    generate_documents.generate_documents()

    print("\n--- Generating process understanding report ---")
    process_understanding_report.generate_report()


if __name__ == "__main__":
    main()
