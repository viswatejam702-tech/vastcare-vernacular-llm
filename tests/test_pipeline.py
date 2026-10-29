#!/usr/bin/env python3
"""
Unit and Integration Test Suite for Vastcare Vernacular Telugu LLM & Hybrid RAG
"""

import os
import sys
import unittest
import json

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.data_pipeline import VernacularDataPipeline, TeluguQualityFilter
from serving.guardrails import TeluguClinicalGuardrails
from serving.vernacular_rag import VernacularHybridRAGEngine, get_rag_engine
from eval.metrics_calculator import (
    compute_bleu,
    compute_chrf,
    compute_cohens_kappa,
    compute_pearson_correlation
)
from export.export_quantize import QuantizationExportPipeline


class TestTeluguPipelineAndRAG(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.pipeline = VernacularDataPipeline(base_dir=base_dir)
        self.quality_filter = TeluguQualityFilter()
        self.rag = get_rag_engine()

    def test_telugu_script_purity(self):
        pure_telugu = "గర్భధారణ సమయంలో మహిళలు పోషకాహారం తీసుకోవాలి."
        mixed_telugu = "Pregnancy lo proper food tinali."
        
        purity_high = self.quality_filter.calculate_script_purity(pure_telugu)
        purity_low = self.quality_filter.calculate_script_purity(mixed_telugu)
        
        self.assertGreater(purity_high, 0.70)
        self.assertLess(purity_low, 0.30)

    def test_rag_retrieval_cpr(self):
        """Test RAG retrieval for CPR query."""
        results = self.rag.retrieve("CPR ఎలా చేయాలి? ఛాతీ ఒత్తిడి నిష్పత్తి ఎంత?", top_k=2)
        self.assertGreater(len(results), 0)
        self.assertIn("CPR", results[0]["title"])
        combined = " ".join(r["content"] for r in results)
        self.assertTrue("100" in combined or "30:2" in combined)

    def test_rag_retrieval_ivf(self):
        """Test RAG retrieval for IVF query."""
        results = self.rag.retrieve("IVF టెస్ట్ ట్యూబ్ బేబీ దశలు ఏమిటి?", top_k=1)
        self.assertGreater(len(results), 0)
        self.assertIn("IVF", results[0]["title"])

    def test_rag_retrieval_hiv(self):
        """Test RAG retrieval for NACO HIV query."""
        results = self.rag.retrieve("హెచ్‌ఐవీ మందులు TLD మరియు PEP ఎప్పుడు వాడాలి?", top_k=1)
        self.assertGreater(len(results), 0)
        self.assertIn("NACO", results[0]["source"])

    def test_emergency_guardrail_detection(self):
        # CPR trigger
        is_em, tag, _ = TeluguClinicalGuardrails.inspect_query("రోగికి గుండె ఆగిపోయింది CPR ఎలా చేయాలి")
        self.assertTrue(is_em)
        self.assertEqual(tag, "CARDIAC_ARREST_CPR")

        # HIV PEP trigger
        is_em, tag, _ = TeluguClinicalGuardrails.inspect_query("హెచ్‌ఐవీ ఎక్స్‌పోజర్ జరిగింది సూది గుచ్చుకుంది")
        self.assertTrue(is_em)
        self.assertEqual(tag, "HIV_PEP_EMERGENCY")

        # Routine trigger
        is_em, tag, _ = TeluguClinicalGuardrails.inspect_query("రోజుకు ఎన్ని లీటర్ల నీరు తాగాలి?")
        self.assertFalse(is_em)
        self.assertEqual(tag, "ROUTINE")

    def test_metrics_calculation(self):
        ref = "గర్భధారణ సమయంలో మహిళలు సమతుల్య పోషకాహారం తీసుకోవాలి."
        hyp = "గర్భధారణ సమయంలో మహిళలు సమతుల్య పోషకాహారం తీసుకోవాలి."
        
        bleu = compute_bleu(hyp, ref)
        chrf = compute_chrf(hyp, ref)
        
        self.assertGreaterEqual(bleu, 90.0)
        self.assertGreaterEqual(chrf, 0.90)

    def test_cohens_kappa(self):
        rater1 = [5, 4, 3, 5, 2, 5]
        rater2 = [5, 4, 3, 5, 2, 5]
        kappa = compute_cohens_kappa(rater1, rater2)
        self.assertEqual(kappa, 1.0)

    def test_rag_retrieval_hypertension(self):
        """Test RAG retrieval for Hypertension & BP query."""
        results = self.rag.retrieve("రక్తపోటు మరియు హైపర్‌టెన్షన్ లక్ష్యాలు ఎంత?", top_k=1)
        self.assertGreater(len(results), 0)
        self.assertIn("130/80", results[0]["content"])

    def test_rag_retrieval_pediatric_nutrition(self):
        """Test RAG retrieval for child vaccination schedule."""
        results = self.rag.retrieve("శిశువు టీకాల షెడ్యూల్ BCG పెంటావాలెంట్", top_k=2)
        self.assertGreater(len(results), 0)
        combined = " ".join(r["content"] for r in results)
        self.assertTrue("BCG" in combined or "Pentavalent" in combined or "పెంటావాలెంట్" in combined)

    def test_rag_retrieval_mental_health(self):
        """Test RAG retrieval for Tele-MANAS helpline query."""
        results = self.rag.retrieve("డిప్రెషన్ మరియు మానసిక ఆరోగ్య సహాయవాణి టెలి-మానస్ 14416", top_k=2)
        self.assertGreater(len(results), 0)
        combined = " ".join(r["content"] for r in results)
        self.assertTrue("14416" in combined or "Tele-MANAS" in combined or "టెలి-మానస్" in combined)

    def test_quantization_summary_structure(self):
        from export.edge_benchmarker import get_edge_benchmark_summary
        summary = get_edge_benchmark_summary()
        self.assertIn("precision_comparison", summary)
        self.assertIn("hardware_profiles", summary)
        self.assertIn("Q4_K_M", summary["precision_comparison"])


if __name__ == "__main__":
    unittest.main()
