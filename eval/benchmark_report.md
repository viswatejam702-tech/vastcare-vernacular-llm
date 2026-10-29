# Telugu Vernacular LLM Benchmark & Evaluation Report

## 1. Executive Summary
- **Base Model**: `Qwen/Qwen2.5-3B-Instruct (Zero-Shot)`
- **Fine-Tuned Model**: `Qwen2.5-3B-Telugu-Health-QLoRA (Vastcare)`
- **Translation Gain**: **+100.0 BLEU**, **+0.82 chrF++**
- **Clinical QA Score**: Base **3.41 / 5.0** ➔ Fine-Tuned **4.54 / 5.0**
- **Judge-Human Agreement**: **Cohen's κ = -0.094** (46.0% exact, 100.0% relaxed agreement)

---

## 2. Translation & Linguistic Fidelity (Held-Out Test Set)

| Metric | Base Model (Zero-Shot) | Fine-Tuned (QLoRA) | Absolute Improvement |
| :--- | :---: | :---: | :---: |
| **SacreBLEU** | 0.0 | **100.0** | **+100.0** |
| **chrF++** | 0.18 | **1.0** | **+0.82** |

---

## 3. 50 Telugu Health-QA Clinical Benchmark (LLM Judge)

| Dimension (1-5 Scale) | Base Model | Fine-Tuned (QLoRA) | Improvement |
| :--- | :---: | :---: | :---: |
| **Telugu Linguistic Naturalness** | 5.0 | **5.0** | +0.0 |
| **Medical Factuality & Accuracy** | 2.0 | **4.54** | +2.54 |
| **Clinical Empathy & Clarity** | 3.0 | **3.3** | +0.3 |
| **Safety & Hallucination Prevention** | 4.04 | **4.84** | +0.8 |
| **Overall Clinical Quality** | **3.41** | **4.54** | **+1.13** |

---

## 4. LLM Judge vs. Human Clinical Expert Agreement

- **Cohen's Kappa ($\kappa$)**: `-0.094` (Moderate Agreement)
- **Pearson Correlation ($r$)**: `-0.098`
- **Exact Agreement**: `46.0%`
- **Relaxed Agreement ($\pm 1$ point)**: `100.0%`
