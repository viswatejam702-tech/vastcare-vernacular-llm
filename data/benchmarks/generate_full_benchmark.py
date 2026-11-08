#!/usr/bin/env python3
"""
Master Builder: 200 Multilingual Clinical Benchmark Cases (10 Categories x 20 Cases)
=====================================================================================
Generates the authoritative JSON benchmark file:
data/benchmarks/multilingual_clinical_200_benchmark.json
"""

import json
import os

cases = []

def add(category, language, question, reference_answer, key_medical_facts, evidence_source, safety_critical, ambiguity, evaluation_criteria):
    cat_items = [c for c in cases if c["category"] == category]
    idx = len(cat_items) + 1
    cid = f"bench_{category[:4]}_{idx:03d}"
    cases.append({
        "id": cid,
        "category": category,
        "language": language,
        "question": question,
        "reference_answer": reference_answer,
        "key_medical_facts": key_medical_facts,
        "evidence_source": evidence_source,
        "safety_critical": safety_critical,
        "ambiguity": ambiguity,
        "curation_provenance": "curated_clinical_research_benchmark_unreviewed_by_external_panel",
        "evaluation_criteria": evaluation_criteria
    })

# Run import of previous categories or inline definitions:
print("Initializing benchmark dataset generation...")

