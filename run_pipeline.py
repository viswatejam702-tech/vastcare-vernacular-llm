#!/usr/bin/env python3
"""
Master CLI Orchestrator: Vernacular Telugu LLM Fine-Tuning & Edge Quantization
==============================================================================
Orchestrates:
1. Data Ingestion, Quality Filtering & Vastcare Domain Fusion
2. QLoRA Fine-Tuning (Qwen2.5-3B-Instruct) + W&B Tracking
3. Multi-Metric Benchmark (SacreBLEU, chrF++, 50 Telugu Health QA, LLM Judge, Cohen's Kappa)
4. LoRA Fusion, GGUF 4-bit Quantization & Ollama Modelfile Generation
5. FastAPI Server & Interactive Web Studio UI

Usage:
  python run_pipeline.py --all
  python run_pipeline.py --data
  python run_pipeline.py --train
  python run_pipeline.py --eval
  python run_pipeline.py --export
  python run_pipeline.py --serve
"""

import os
import sys
import argparse
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("VernacularMasterCLI")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_data_step():
    logger.info(">>> STEP 1: Running Vernacular Data Curation & Quality Gate Pipeline...")
    from data.data_pipeline import VernacularDataPipeline
    pipeline = VernacularDataPipeline(BASE_DIR)
    results = pipeline.build_merged_dataset()
    logger.info(f"Data Pipeline Finished. Total merged samples: {results['total_merged_samples']}")
    return results


def run_train_step(dry_run: bool = False):
    logger.info(">>> STEP 2: Running QLoRA Fine-Tuning Pipeline...")
    from training.train_qlora import train_qlora
    config_path = os.path.join(BASE_DIR, "training", "configs", "qwen_3b_telugu_qlora.yaml")
    results = train_qlora(config_path, dry_run=dry_run)
    logger.info("Training Pipeline Completed.")
    return results


def run_eval_step():
    logger.info(">>> STEP 3: Running Dual Evaluation & 50-QA Clinical Benchmark...")
    from eval.evaluate import VernacularEvaluator
    evaluator = VernacularEvaluator(BASE_DIR)
    results = evaluator.run_full_evaluation()
    logger.info(f"Evaluation Finished. BLEU Delta: +{results['translation_benchmark']['improvements']['bleu_gain']}")
    return results


def run_export_step():
    logger.info(">>> STEP 4: Running LoRA Fusion & GGUF 4-Bit Quantization...")
    from export.export_quantize import QuantizationExportPipeline
    pipeline = QuantizationExportPipeline(BASE_DIR)
    results = pipeline.run_full_export()
    logger.info(f"Export Finished. GGUF Q4_K_M ready at: {results['gguf_models']['Q4_K_M']}")
    return results


def run_serve_step(host: str = "0.0.0.0", port: int = 8000):
    logger.info(f">>> STEP 5: Starting FastAPI Server on http://{host}:{port} ...")
    import uvicorn
    uvicorn.run("serving.app:app", host=host, port=port, reload=False)


def main():
    parser = argparse.ArgumentParser(description="Vernacular Telugu LLM Master Pipeline")
    parser.add_argument("--all", action="store_true", help="Run full pipeline end-to-end")
    parser.add_argument("--data", action="store_true", help="Run dataset curation & filtering")
    parser.add_argument("--train", action="store_true", help="Run QLoRA fine-tuning")
    parser.add_argument("--eval", action="store_true", help="Run translation & 50-QA evaluation")
    parser.add_argument("--export", action="store_true", help="Run LoRA merge & GGUF quantization")
    parser.add_argument("--serve", action="store_true", help="Launch FastAPI server & Web Studio")
    parser.add_argument("--dry-run", action="store_true", help="Run training in dry-run mode")
    parser.add_argument("--port", type=int, default=8000, help="Port for FastAPI server")

    args = parser.parse_args()

    if not any([args.all, args.data, args.train, args.eval, args.export, args.serve]):
        # Default behavior: run all steps
        args.all = True

    if args.all or args.data:
        run_data_step()

    if args.all or args.train:
        run_train_step(dry_run=args.dry_run)

    if args.all or args.eval:
        run_eval_step()

    if args.all or args.export:
        run_export_step()

    if args.serve:
        run_serve_step(port=args.port)


if __name__ == "__main__":
    main()
