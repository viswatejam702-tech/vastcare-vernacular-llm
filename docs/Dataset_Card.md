# Dataset Card: VastCare Indic Clinical Instruction Corpus

**Dataset Version:** 2.5.0-PROD  
**Language(s):** Telugu (`te`), Hindi (`hi`), English (`en`), Telugu-English Code-Switching (`te-en`)  
**Curators:** Principal Multilingual NLP Research Scientist & Medical Domain Adapters  
**License:** CC-BY-4.0 / Open Government Data (OGD) License India  

---

## 1. Dataset Description

The **VastCare Indic Clinical Instruction Corpus** is a curated, quality-filtered, deduplicated dataset designed to train and benchmark multilingual conversational models on clinical medicine, community health education, and rural healthcare triage.

All records are grounded in verified clinical protocols from:
1. **Ministry of Health and Family Welfare (MoHFW), Government of India**
2. **Indian Council of Medical Research (ICMR)**
3. **National AIDS Control Organisation (NACO)**
4. **National Tuberculosis Elimination Program (NTEP)**
5. **World Health Organization (WHO)**
6. **American Heart Association (AHA / IRC)**

---

## 2. Dataset Structure & Schema

Each instance adheres to the strict Pydantic `ClinicalDataRecord` schema:

```json
{
  "id": "vastcare_te_cpr_001",
  "instruction": "ఒక వ్యక్తి స్పృహ తప్పి శ్వాస ఆగిపోయినప్పుడు (కార్డియాక్ అరెస్ట్) CPR ఎలా చేయాలి?",
  "input": "",
  "output": "కార్డియాక్ అరెస్ట్ వచ్చినప్పుడు C-A-B క్రమంలో తక్షణమే CPR ప్రారంభించాలి: 108 కి కాల్ చేసి...",
  "category": "emergency_cpr",
  "language": "te",
  "code_switching_ratio": 0.0,
  "medical_terms": ["CPR", "కార్డియాక్ అరెస్ట్", "ఛాతీ ఒత్తిడి", "AED"],
  "rural_terms": ["కాచి చల్లార్చిన నీరు"],
  "evidence_reference": "AHA / IRC Guidelines for Cardiopulmonary Resuscitation",
  "safety_label": "emergency_escalate",
  "factuality_label": "clinically_verified_guideline",
  "ambiguity_label": "unambiguous",
  "source": "vastcare_clinical_curation",
  "domain": "healthcare_vastcare",
  "quality_metadata": {
    "is_valid": true,
    "script_purity": 0.884,
    "clinical_grade": true
  }
}
```

---

## 3. Data Splits & Deduplication Statistics

- **Raw Ingested Records:** 58 instances (including domain-adapted healthcare oversamples).
- **Deduplication Engine:** Word 2-gram and 3-gram pairwise Jaccard index similarity ($\tau_{\text{sim}} \ge 0.82$).
- **Unique Post-Dedup Records:** 22 high-value seeds.
- **Split Breakdown:**
  - **Train Split (70%):** 16 records (`data/processed/train.jsonl`)
  - **Validation Split (15%):** 3 records (`data/processed/val.jsonl`)
  - **Test Split (15%):** 3 records (`data/processed/test.jsonl`)
- **Language Distribution:**
  - Pure Telugu (`te`): $86.4\%$
  - Telugu-English Code-Switching (`te-en`): $9.1\%$
  - English Reference (`en`): $4.5\%$

---

## 4. Benchmark Contamination & Leakage Prevention

To guarantee zero test-set contamination:
- The pipeline extracts all character and word 3-grams from all held-out benchmark evaluation suites (`data/benchmarks/*`).
- Any training candidate exhibiting an n-gram overlap $> 0.65$ with an evaluation item is automatically flagged and quarantined.
- Verification status: **Zero Benchmark Contamination Verified**.

---

## 5. Privacy, De-Identification & Ethics

- **Zero Patient Health Information (PHI/PII):** The dataset contains zero patient identifiers, names, hospital registration numbers, or private medical charts.
- **Guideline Synthetic Derivations:** Scenarios are synthetic educational abstractions derived from official clinical guidelines.

