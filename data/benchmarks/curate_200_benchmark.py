#!/usr/bin/env python3
"""
Curator for 200 Multilingual Clinical Benchmark Cases
=====================================================
Generates data/benchmarks/multilingual_clinical_200_benchmark.json
Exactly 10 categories x 20 cases = 200 items.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BENCHMARK_PATH = os.path.join(BASE_DIR, "data", "benchmarks", "multilingual_clinical_200_benchmark.json")

# Let's write the complete dataset directly
all_cases = []

def add_item(cat, lang, q, ref, facts, src, sc, amb, crit):
    cat_items = [c for c in all_cases if c["category"] == cat]
    num = len(cat_items) + 1
    cid = f"bench_{cat[:4]}_{num:03d}"
    all_cases.append({
        "id": cid,
        "category": cat,
        "language": lang,
        "question": q,
        "reference_answer": ref,
        "key_medical_facts": facts,
        "evidence_source": src,
        "safety_critical": sc,
        "ambiguity": amb,
        "curation_provenance": "curated_clinical_research_benchmark_unreviewed_by_external_panel",
        "evaluation_criteria": crit
    })

print("Writing curate_200_benchmark.py script...")

