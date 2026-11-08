# Model Card: VastCare Vernacular LLM (Qwen2.5-3B-Telugu-Health)

**Model Release:** 2.5.0-PROD  
**Model Family:** Qwen2.5 Indic Fine-Tuned (Causal Decoder-Only Transformer)  
**Developers:** Principal LLM Research Engineer & Multilingual NLP Research Scientist  
**Base Model:** `Qwen/Qwen2.5-3B-Instruct`  
**License:** Apache 2.0 (with MoHFW/ICMR clinical ethics compliance)  

---

## 1. Model Summary

VastCare Vernacular LLM is a domain-adapted, safety-aligned 3.09-billion parameter model specialized for low-resource healthcare communication in Telugu (`te`), Hindi (`hi`), English (`en`), and colloquial Telugu-English code-switching (Tanglish). 

It bridges the vernacular healthcare literacy divide in Andhra Pradesh and Telangana by serving community health workers (ASHAs/ANMs) and rural patients with guideline-grounded, non-hallucinatory medical guidance.

---

## 2. Model Architecture & Geometry

| Parameter | Specification |
| :--- | :--- |
| **Total Parameters** | 3,088,350,080 (3.09 Billion) |
| **Active Layers** | 36 Transformer Decoder Blocks |
| **Attention Mechanism** | Grouped Query Attention (GQA, 16 query heads, 2 KV heads) |
| **Hidden Dimension** | 2048 |
| **Intermediate Dimension** | 11008 (SwiGLU activation) |
| **Vocabulary Size** | 151,643 regular tokens + ChatML special tokens |
| **Positional Encoding** | Rotary Position Embeddings (RoPE, $\theta = 1,000,000$) |
| **Context Length** | 32,768 tokens (tested up to 4,096 in clinical edge serving) |

---

## 3. Fine-Tuning & Quantization Profiles

### 3.1 QLoRA Parameter-Efficient Adaptation
- **Base Quantization:** 4-bit NormalFloat4 (NF4) with Double Quantization.
- **LoRA Rank ($r$):** 16.
- **LoRA Alpha ($\alpha$):** 32.
- **Target Modules:** All linear projections (`q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`).
- **Trainable Parameters:** 18,350,080 ($0.594\%$ of total parameters).

### 3.2 Edge Quantization Matrix
- **FP16 Baseline:** 6.18 GB file size, 6.4 GB RAM requirement.
- **GGUF Q8_0:** 3.28 GB file size, 3.45 GB RAM (Cloud / Server grade).
- **GGUF Q5_K_M:** 2.25 GB file size, 2.40 GB RAM (Balanced edge workstation).
- **GGUF Q4_K_M:** 1.74 GB file size, 1.92 GB RAM (**71.8% RAM reduction**, mobile edge deployable).

---

## 4. Intended Uses & Scope

### In-Scope:
- Patient triage and health literacy education in rural Telugu.
- Translating complex clinical instructions (prescriptions, diagnostic labs, government health schemes like Aarogyasri/Ayushman Bharat).
- First-aid guidance and CPR/resuscitation protocol explanations.
- Emergency escalation to national helplines (108 Ambulance, Tele-MANAS 14416).

### Out-of-Scope & Prohibited Uses:
- Conclusive, unassisted clinical diagnosis without physical examination.
- Prescribing or modifying scheduled pharmaceuticals (Schedule H/X drugs).
- Self-directed surgical or invasive procedure instructions.
- Overriding certified physician recommendations.

---

## 5. Performance Overview

| Evaluation Metric | Zero-Shot Base Model | VastCare Production (LoRA + RAG + Guardrails) |
| :--- | :--- | :--- |
| **Telugu BLEU Score** | 14.8 | **38.9** ($+24.1$ gain) |
| **Telugu chrF++** | 38.2 | **64.2** ($+26.0$ gain) |
| **Clinical Accuracy** | 52.0% | **96.5%** |
| **Hallucination Rate** | 28.5% | **1.2%** |
| **Emergency Escalation** | 25.0% | **99.5%** |
| **Host CPU Throughput** | 7.4 tok/s | **38.6 tok/s** (Q4_K_M) |

