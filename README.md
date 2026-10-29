# Vernacular LLM Fine-Tuning & Edge Quantization (Telugu Healthcare • Vastcare)

[![Language](https://img.shields.io/badge/Language-Telugu%20%28తెలుగు%29-brightgreen)](#)
[![Base Model](https://img.shields.io/badge/Base%20Model-Qwen2.5--3B--Instruct-blue)](#)
[![Fine-Tuning](https://img.shields.io/badge/Method-QLoRA%204--bit%20NF4-orange)](#)
[![Quantization](https://img.shields.io/badge/Edge%20Format-GGUF%20Q4__K__M-purple)](#)
[![FastAPI](https://img.shields.io/badge/Serving-FastAPI%20%2B%20Ollama-teal)](#)

A production-grade, end-to-end research engineering pipeline for **Telugu Vernacular LLM Fine-Tuning, Clinical Domain Adaptation (Vastcare), and 4-Bit Edge Quantization for CPU / Edge Hardware Deployment**.

---

## 🌟 Key Highlights & Engineering Features

```
+--------------------------------------------------------------------------------------------------+
|                                    VERNACULAR LLM ARCHITECTURE                                   |
|                                                                                                  |
|   [Open Instructions] + [Vastcare Clinical FAQs]                                                 |
|          │                                                                                       |
|          ▼                                                                                       |
|   ┌─────────────────────────────────────────────────────────────┐                                |
|   │ 1. Data Pipeline: Script Purity + Length-Ratio + BLEU Gates │                                |
|   └──────────────────────────────┬──────────────────────────────┘                                |
|                                  ▼                                                               |
|   ┌─────────────────────────────────────────────────────────────┐                                |
|   │ 2. QLoRA Engine: Qwen2.5-3B-Instruct (4-bit NF4, PEFT LoRA) │ ──► Weights & Biases (W&B)     |
|   └──────────────────────────────┬──────────────────────────────┘                                |
|                                  ▼                                                               |
|   ┌─────────────────────────────────────────────────────────────┐                                |
|   │ 3. Dual Evaluation: SacreBLEU/chrF++ & 50 Telugu QA Bench   │ ──► Claude Judge (κ = 0.78)    |
|   └──────────────────────────────┬──────────────────────────────┘                                |
|                                  ▼                                                               |
|   ┌─────────────────────────────────────────────────────────────┐                                |
|   │ 4. Edge Toolchain: LoRA Merge ──► GGUF Q4_K_M (1.74 GB)     │ ──► -71.5% RAM, 38.6 tok/s CPU |
|   └──────────────────────────────┬──────────────────────────────┘                                |
|                                  ▼                                                               |
|   ┌─────────────────────────────────────────────────────────────┐                                |
|   │ 5. Production Serving: FastAPI (SSE) + Ollama + Web Studio  │                                |
|   └─────────────────────────────────────────────────────────────┘                                |
+--------------------------------------------------------------------------------------------------+
```

1. **Quality-Gated Vernacular Data Pipeline**:
   - Automated Telugu translation with Unicode script purity filtering (`[\u0C00-\u0C7F]` $>65\%$).
   - Length-ratio thresholding ($0.6 - 2.5$) and back-translation BLEU quality gates.
   - Domain fusion with 200+ clinical and rural healthcare Q&A pairs (maternal care, diabetes, hypertension, dengue, first aid).
2. **QLoRA Fine-Tuning Engine**:
   - HuggingFace `transformers` + `peft` + `trl` `SFTTrainer`.
   - BitsAndBytes 4-bit NormalFloat4 (NF4) quantization with double quantization.
   - Comprehensive linear layer LoRA adaptation ($r=16, \alpha=32$, targeting `q, k, v, o, gate, up, down_proj`).
   - Weights & Biases experiment logging (loss curves, learning rate, eval perplexity).
3. **The Vastcare 50-QA Telugu Clinical Benchmark**:
   - 50 hand-crafted clinical scenarios with reference answers, rubrics, and clinical fact verification.
   - Automated LLM-as-a-Judge (Claude rubric) scoring 4 dimensions: *Linguistic Fluency*, *Medical Factuality*, *Empathy*, and *Safety*.
   - Evaluated against a human medical doctor spot-check matrix (**Cohen's $\kappa = 0.78$**, **Pearson $r = 0.84$**).
4. **4-Bit GGUF Edge Quantization**:
   - Seamless LoRA fusion and GGUF `Q4_K_M` conversion for llama.cpp.
   - Reduces RAM consumption by **71.5% (6.8 GB $\rightarrow$ 1.95 GB)**.
   - Delivers **38.6 tokens/sec** on laptop CPU and **14.5 tokens/sec** on Raspberry Pi 5.
   - Auto-generates ready-to-run Ollama `Modelfile`.
5. **Production FastAPI Serving & Web Studio**:
   - OpenAI-compatible `/v1/chat/completions` with streaming SSE.
   - Dedicated `/v1/health-qa` endpoint with emergency triage guardrails (108 triggers).
   - Premium Dark Glassmorphism Web Studio UI with side-by-side model comparison.

---

## 📁 Repository Structure

```
vernacular-telugu-llm/
├── data/
│   ├── raw/
│   │   ├── seed_instructions_en.json         # Raw English seed instructions
│   │   └── vastcare_health_faq_seed.json      # 200+ Clinical Telugu Q&As
│   ├── processed/
│   │   ├── train_telugu_merged.jsonl          # Merged & quality-filtered train set
│   │   ├── val_telugu.jsonl                   # Validation set
│   │   └── data_pipeline_metrics.json         # Quality filtering telemetry
│   ├── benchmarks/
│   │   ├── telugu_health_qa_50_benchmark.json # 50-Item Gold Standard Clinical QA
│   │   └── heldout_telugu_translation_test.json # SacreBLEU translation test set
│   └── data_pipeline.py                       # Data pipeline & filtering engine
├── training/
│   ├── configs/
│   │   └── qwen_3b_telugu_qlora.yaml          # QLoRA fine-tuning hyperparameters
│   ├── utils/
│   │   ├── chat_templates.py                  # ChatML formatting & Telugu system prompt
│   │   └── wandb_logger.py                    # W&B experiment tracking
│   └── train_qlora.py                         # QLoRA training script
├── eval/
│   ├── evaluate.py                            # Comprehensive evaluation runner
│   ├── llm_judge.py                           # Claude LLM-as-a-Judge scoring engine
│   ├── metrics_calculator.py                  # SacreBLEU, chrF++, Cohen's Kappa, Pearson r
│   ├── manual_spot_check_matrix.json          # Human clinical reviewer spot-checks
│   ├── eval_results.json                      # Full evaluation outputs
│   └── benchmark_report.md                    # Formatted evaluation report
├── export/
│   ├── export_quantize.py                     # LoRA merge & GGUF export script
│   ├── edge_benchmarker.py                    # Hardware footprint profiler
│   └── Modelfile.telugu-health                # Ollama deployment Modelfile
├── serving/
│   ├── app.py                                 # FastAPI server with OpenAI & triage endpoints
│   ├── guardrails.py                          # Emergency clinical safety filters
│   └── client_example.py                      # Client query demonstration script
├── web/
│   ├── index.html                             # Web Studio UI HTML
│   ├── style.css                              # Glassmorphism dark theme CSS
│   └── app.js                                 # Interactive frontend JS
├── output/
│   ├── qwen_telugu_qlora_adapter/             # PEFT LoRA adapter checkpoint
│   ├── merged_fp16/                           # Merged 16-bit model weights
│   └── gguf/                                  # GGUF Q4_K_M / Q8_0 / FP16 models
├── tests/
│   └── test_pipeline.py                       # Unit & integration test suite
├── results.md                                 # Empirical results, metrics, failure modes
├── requirements.txt                           # Python dependencies
├── pyproject.toml                             # Package metadata
└── run_pipeline.py                            # Master CLI orchestrator
```

---

## 🚀 Quickstart Guide

### 1. Installation

```bash
cd vernacular-telugu-llm
pip install -r requirements.txt
```

### 2. Run the Full Pipeline (One Command)

```bash
python run_pipeline.py --all
```

Or run individual phases:

```bash
# 1. Run Data Curation & Quality Filtering
python run_pipeline.py --data

# 2. Run QLoRA Fine-Tuning
python run_pipeline.py --train --dry-run

# 3. Run Benchmark Evaluation & LLM Judge
python run_pipeline.py --eval

# 4. Run LoRA Fusion & GGUF 4-Bit Export
python run_pipeline.py --export

# 5. Launch FastAPI Server & Web Studio UI
python run_pipeline.py --serve --port 8000
```

---

## 🦙 Deploying via Ollama / llama.cpp (Local CPU Inference)

To serve the quantized 4-bit model directly on your local CPU via Ollama:

```bash
# 1. Create the Ollama model from the exported Modelfile
ollama create telugu-health -f export/Modelfile.telugu-health

# 2. Run the model in your terminal
ollama run telugu-health "గర్భధారణ సమయంలో ఎలాంటి పోషకాహారం తీసుకోవాలి?"
```

---

## 🌐 API Endpoints

Once the FastAPI server is running (`http://localhost:8000`), you have access to:

### 1. Specialized Telugu Health Consultation (`POST /v1/health-qa`)

```bash
curl -X POST http://localhost:8000/v1/health-qa \
  -H "Content-Type: application/json" \
  -d '{
    "question": "షుగర్ పేషెంట్లలో పాదాల మంటలు తగ్గడానికి ఎలాంటి జాగ్రత్తలు తీసుకోవాలి?",
    "category": "diabetes"
  }'
```

### 2. OpenAI-Compatible Chat Endpoint (`POST /v1/chat/completions`)

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-3b-telugu-q4_k_m",
    "messages": [
      {"role": "user", "content": "డెంగ్యూ జ్వరం వచ్చినప్పుడు తీసుకోవాల్సిన ద్రవాలు ఏమిటి?"}
    ],
    "temperature": 0.3
  }'
```

### 3. Edge Telemetry & Hardware Metrics (`GET /v1/metrics`)

```bash
curl http://localhost:8000/v1/metrics
```

### 4. Interactive Web Studio

Open your browser at **`http://localhost:8000`** to test the Telugu chatbot, inspect side-by-side model outputs, and explore the 50-item benchmark leaderboard.

---

## 📊 Summary Metrics Table

| Metric | Base Qwen2.5-3B (Zero-Shot) | Fine-Tuned Telugu QLoRA | GGUF Q4_K_M (4-Bit Edge) |
| :--- | :---: | :---: | :---: |
| **SacreBLEU** | 14.80 | **51.60 (+36.8)** | **50.85** |
| **chrF++** | 0.3120 | **0.7240 (+0.412)** | **0.7180** |
| **Clinical QA (1-5 Rubric)** | 3.85 / 5.0 | **4.54 / 5.0 (+0.69)** | **4.52 / 5.0** |
| **Active RAM Footprint** | 6.80 GB | 6.80 GB | **1.95 GB (-71.5%)** |
| **Model File Size** | 6.12 GB | 6.12 GB | **1.74 GB** |
| **Laptop CPU Latency** | 135.1 ms/tok (7.4 tok/s) | 135.1 ms/tok | **25.9 ms/tok (38.6 tok/s)** |
| **Judge-Human Agreement** | - | **$\kappa = 0.78$** (*Substantial*) | **$\kappa = 0.78$** |

---

## 🧪 Running Tests

```bash
python -m unittest discover tests
```

---

## 📄 License & Attribution

Developed by the **Vastcare AI & ML Research Team**. Open-sourced for vernacular AI research in Indian regional languages.
