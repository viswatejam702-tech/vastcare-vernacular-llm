"""
Weights & Biases (W&B) Logging and Telemetry Manager for QLoRA Fine-Tuning.
"""

import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("WandbLogger")


class ExperimentTracker:
    def __init__(
        self,
        project: str = "vernacular-telugu-llm",
        run_name: str = "qwen2.5-3b-telugu-health-qlora",
        config: Optional[Dict[str, Any]] = None,
        mode: str = "offline",
        local_log_dir: str = "./logs"
    ):
        self.project = project
        self.run_name = run_name
        self.config = config or {}
        self.mode = mode
        self.local_log_dir = local_log_dir
        self.wandb_run = None
        self.metrics_history = []

        os.makedirs(self.local_log_dir, exist_ok=True)
        self._init_wandb()

    def _init_wandb(self):
        if self.mode == "disabled":
            logger.info("W&B logging disabled by configuration.")
            return

        try:
            import wandb
            os.environ["WANDB_MODE"] = self.mode
            self.wandb_run = wandb.init(
                project=self.project,
                name=self.run_name,
                config=self.config,
                dir=self.local_log_dir,
                resume="allow"
            )
            logger.info(f"W&B initialized in mode '{self.mode}' (Run: {self.run_name})")
        except ImportError:
            logger.warning("wandb package not found. Falling back to local JSON telemetry logging.")
        except Exception as e:
            logger.warning(f"Failed to initialize W&B ({e}). Falling back to local JSON telemetry logging.")

    def log(self, metrics: Dict[str, Any], step: Optional[int] = None):
        """Logs scalar metrics to W&B and local history."""
        record = {"step": step, **metrics}
        self.metrics_history.append(record)

        if self.wandb_run:
            try:
                import wandb
                wandb.log(metrics, step=step)
            except Exception as e:
                logger.debug(f"W&B log failed: {e}")

        # Local save periodic
        if len(self.metrics_history) % 5 == 0:
            self._save_local_history()

    def _save_local_history(self):
        log_file = os.path.join(self.local_log_dir, f"{self.run_name}_metrics.json")
        try:
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump({
                    "run_name": self.run_name,
                    "project": self.project,
                    "config": self.config,
                    "history": self.metrics_history
                }, f, indent=2)
        except Exception as e:
            logger.debug(f"Local metric save failed: {e}")

    def finish(self):
        """Closes W&B run cleanly."""
        self._save_local_history()
        if self.wandb_run:
            try:
                import wandb
                wandb.finish()
                logger.info("W&B run finalized successfully.")
            except Exception as e:
                logger.debug(f"W&B finish error: {e}")
