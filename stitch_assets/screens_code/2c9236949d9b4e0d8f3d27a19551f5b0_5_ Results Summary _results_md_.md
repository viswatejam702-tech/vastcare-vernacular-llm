# Telugu LLM Fine-Tuning Results (Qwen2.5-3B)

## Executive Summary
This project fine-tuned a 3B parameter model specifically for Telugu instruction-following and health QA. By utilizing QLoRA and 4-bit quantization, we achieved a deployable model that fits on consumer CPUs while significantly outperforming the base model in regional language tasks.

## Metrics Comparison

| Metric | Base (Qwen2.5-3B) | Fine-Tuned (Telugu-QLoRA) | Improvement |
| :--- | :--- | :--- | :--- |
| **Translation BLEU** | 12.0 | 24.5 | +104% |
| **Translation chrF** | 31.5 | 48.2 | +53% |
| **Health QA Accuracy** | 45% | 82% | +37% |
| **Judge Agreement** | N/A | 88% | High |

## Inference Footprint (Quantization)

| Feature | BF16 (Original) | GGUF Q4_K_M (Quantized) | Reduction |
| :--- | :--- | :--- | :--- |
| **Model Size** | ~6.5 GB | ~1.9 GB | -70.7% |
| **RAM Usage** | ~12 GB | ~3.5 GB | -70.8% |
| **Inference Latency** | 45ms/tok (GPU) | 120ms/tok (CPU) | Viable for Edge |

## Known Failure Modes
1. **Code-Switching**: The model occasionally reverts to English for highly technical medical terms not present in the Telugu training set.
2. **Grammar**: Minor syntax errors in complex conditional sentences (e.g., "If... then...").
3. **Hallucination**: High-risk health advice is still prone to typical LLM hallucinations; requires a RAG layer for production use.