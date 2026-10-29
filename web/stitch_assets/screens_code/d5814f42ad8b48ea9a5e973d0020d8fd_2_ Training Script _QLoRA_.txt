import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
from datasets import load_dataset
import wandb

# 1. Setup
model_id = "Qwen/Qwen2.5-3B-Instruct"
dataset_path = "telugu_instruction_dataset.json"

wandb.init(project="telugu-llm-finetune", name="qlora-qwen-3b-telugu")

# 2. Load Model with QLoRA
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

tokenizer = AutoTokenizer.from_tokenizer(model_id)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

# 3. Load Dataset
dataset = load_dataset("json", data_files=dataset_path, split="train")

def formatting_func(example):
    text = f"<|im_start|>user\n{example['instruction']}\n{example['input']}<|im_end|>\n<|im_start|>assistant\n{example['output']}<|im_end|>"
    return [text]

# 4. Trainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    max_seq_length=1024,
    tokenizer=tokenizer,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=100,
        max_steps=1000,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=10,
        output_dir="outputs",
        optim="paged_adamw_8bit",
        report_to="wandb"
    ),
    formatting_func=formatting_func,
)

trainer.train()
model.save_pretrained("telugu-qwen-3b-lora")