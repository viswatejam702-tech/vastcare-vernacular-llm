import os
import json
import pandas as pd
from datasets import load_dataset, Dataset
from deep_translator import GoogleTranslator
import sacrebleu

def translate_text(text, target_lang='te'):
    try:
        return GoogleTranslator(source='en', target=target_lang).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return None

def quality_filter(original, translated, threshold=0.7):
    if not translated or len(translated) == 0:
        return False
    # Length ratio check
    ratio = len(translated) / len(original)
    if ratio < 0.5 or ratio > 2.0:
        return False
    return True

def process_dataset(limit=1000):
    print("Loading Alpaca dataset...")
    dataset = load_dataset("tatsu-lab/alpaca", split="train[:1000]")
    
    processed_data = []
    print(f"Translating {limit} samples to Telugu...")
    
    for i, item in enumerate(dataset):
        instruction_te = translate_text(item['instruction'])
        input_te = translate_text(item['input']) if item['input'] else ""
        output_te = translate_text(item['output'])
        
        if quality_filter(item['instruction'], instruction_te) and quality_filter(item['output'], output_te):
            processed_data.append({
                "instruction": instruction_te,
                "input": input_te,
                "output": output_te,
                "source": "alpaca_translated"
            })
        
        if (i+1) % 100 == 0:
            print(f"Processed {i+1} items...")

    # Merge domain-specific health data
    health_data = [
        {"instruction": "జ్వరం వచ్చినప్పుడు ఏమి చేయాలి?", "input": "", "output": "ధారాళంగా ద్రవాలు త్రాగాలి, విశ్రాంతి తీసుకోవాలి మరియు అవసరమైతే పారాసెటమాల్ వాడాలి. లక్షణాలు కొనసాగితే వైద్యుడిని సంప్రదించండి.", "source": "health_domain"},
        # ... ~200 items would be loaded here
    ]
    processed_data.extend(health_data)
    
    final_df = pd.DataFrame(processed_data)
    final_df.to_json("telugu_instruction_dataset.json", orient="records", force_ascii=False, indent=4)
    print(f"Dataset saved with {len(final_df)} samples.")

if __name__ == "__main__":
    process_dataset()