#!/usr/bin/env python3
"""
Client Example: Querying the Vastcare Vernacular Telugu API & Hybrid RAG Engine
"""

import sys
import json
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

API_BASE_URL = "http://localhost:8000"


def test_health_qa(question: str):
    url = f"{API_BASE_URL}/v1/health-qa"
    payload = {
        "question": question,
        "category": "clinical_consultation",
        "model_variant": "qwen2.5-3b-telugu-q4_k_m",
        "enable_rag": True
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print("=" * 60)
            print(f"ప్రశ్న (Query): {data['question']}")
            print("-" * 60)
            print(f"సమాధానం (Response):\n{data['response_telugu']}")
            print("-" * 60)
            print(f"ఎమర్జెన్సీ స్థితి: {data['clinical_triage']['is_emergency']} ({data['clinical_triage']['emergency_category']})")
            print(f"RAG ఆధారాలు వాడారా: {data['rag_grounding']['evidence_used']} ({len(data['rag_grounding']['citations'])} Citations)")
            print(f"జెనరేషన్ వేగం: {data['performance']['latency_ms']} ms")
            print("=" * 60 + "\n")
    except Exception as e:
        print(f"Error querying server: {e}")


if __name__ == "__main__":
    print("Testing Telugu Healthcare Multi-Topic Queries with Real-World RAG Grounding...\n")
    test_health_qa("కార్డియాక్ అరెస్ట్ వచ్చినప్పుడు CPR ఛాతీ ఒత్తిడి వేగం ఎంత ఉండాలి?")
    test_health_qa("ఐవీఎఫ్ (IVF) టెస్ట్ ట్యూబ్ బేబీ చికిత్సలో ప్రధాన దశలు ఏమిటి?")
    test_health_qa("హెచ్‌ఐవీ సోకిన వారు ప్రభుత్వ ART కేంద్రాల్లో లభించే TLD మందులను ఎలా వాడాలి?")
