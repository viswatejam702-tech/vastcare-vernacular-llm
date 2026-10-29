# 1. Merge LoRA weights
# python3 merge_peft_adapters.py --base_model_name_or_path Qwen/Qwen2.5-3B-Instruct --peft_model_path telugu-qwen-3b-lora --output_dir merged_model

# 2. Quantize to GGUF using llama.cpp
# git clone https://github.com/ggerganov/llama.cpp
# python3 llama.cpp/convert_hf_to_gguf.py merged_model --outtype q4_k_m --outfile telugu_qwen_q4.gguf

# 3. Serve via Ollama
# Create Modelfile:
# FROM ./telugu_qwen_q4.gguf
# PARAMETER temperature 0.7
# SYSTEM "మీరు తెలుగులో సమాధానమిచ్చే సహాయకరమైన అసిస్టెంట్."

# 4. FastAPI Wrapper
from fastapi import FastAPI
import requests

app = FastAPI()

@app.post("/generate")
async def generate(prompt: str):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "telugu-qwen",
        "prompt": prompt,
        "stream": False
    })
    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)