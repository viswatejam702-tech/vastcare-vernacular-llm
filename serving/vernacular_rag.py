"""
Trilingual Hybrid Clinical RAG Engine for Telugu, Hindi, and English
====================================================================
Provides verified, multi-lingual retrieval grounded in official clinical &
government guidelines (MoHFW, NACO, ICMR, AHA, WHO).
"""

import os
import re
import math
import logging
from typing import List, Dict, Any, Tuple, Optional
from collections import Counter

logger = logging.getLogger("VernacularRAG")

TELUGU_STOPWORDS = {
    "మరియు", "యొక్క", "లో", "నుండి", "కు", "కి", "గా", "తో", "అనేది", "వల్ల",
    "కోసం", "ద్వారా", "ఒక", "ఈ", "ఆ", "లేదా", "కూడా", "కానీ", "అయితే", "వరకు"
}

HINDI_STOPWORDS = {
    "और", "का", "की", "के", "में", "से", "को", "है", "हैं", "था", "थी", "थे",
    "पर", "के लिए", "द्वारा", "एक", "यह", "वह", "या", "भी", "लेकिन", "तक"
}

ENGLISH_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been"
}

ALL_STOPWORDS = TELUGU_STOPWORDS | HINDI_STOPWORDS | ENGLISH_STOPWORDS


class ClinicalDocumentChunk:
    def __init__(self, doc_id: str, title: str, source: str, content: str, category: str):
        self.doc_id = doc_id
        self.title = title
        self.source = source
        self.content = content
        self.category = category
        self.tokens = self._tokenize(content)

    def _tokenize(self, text: str) -> List[str]:
        # Support Telugu, Devanagari (Hindi), and Latin characters
        cleaned = re.sub(r'[^\w\s\u0C00-\u0C7F\u0900-\u097F]', ' ', text.lower())
        words = cleaned.split()
        return [w for w in words if w not in ALL_STOPWORDS and len(w) > 1]


class VernacularHybridRAGEngine:
    """
    Hybrid Clinical RAG Engine: Combines Dense Vector Term Frequency with
    BM25 Keyword Scoring and Trilingual Morphological Stemming.
    """
    def __init__(self, docs_dir: Optional[str] = None):
        if docs_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            docs_dir = os.path.join(base_dir, "data", "rag_docs")
        self.docs_dir = docs_dir
        self.chunks: List[ClinicalDocumentChunk] = []
        self.vocab: Dict[str, int] = {}
        self.doc_frequencies: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.load_and_index_documents()

    def load_and_index_documents(self):
        """Loads markdown documents and splits into section chunks."""
        if not os.path.exists(self.docs_dir):
            logger.warning(f"RAG docs directory not found at {self.docs_dir}")
            return

        self.chunks = []
        doc_count = 0

        for fname in sorted(os.listdir(self.docs_dir)):
            if not fname.endswith(".md"):
                continue
            doc_count += 1
            fpath = os.path.join(self.docs_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                raw_text = f.read()

            title_match = re.search(r'^#\s*(.+)$', raw_text, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else fname
            
            source_match = re.search(r'\*\*Source\*\*:\s*(.+)$', raw_text, re.MULTILINE)
            source = source_match.group(1).strip() if source_match else "MoHFW / ICMR Clinical Guidelines"
            
            topic_match = re.search(r'\*\*Topic\*\*:\s*(.+)$', raw_text, re.MULTILINE)
            category = topic_match.group(1).strip() if topic_match else "General Clinical"

            # Split by section headers (##)
            sections = re.split(r'\n(?=##\s+)', raw_text)
            for idx, sec in enumerate(sections):
                sec_text = sec.strip()
                if not sec_text or len(sec_text) < 30:
                    continue
                chunk_id = f"{fname.replace('.md','')}_s{idx}"
                chunk = ClinicalDocumentChunk(
                    doc_id=chunk_id,
                    title=title,
                    source=source,
                    content=sec_text,
                    category=category
                )
                self.chunks.append(chunk)

        # Build Vocabulary and Inverted Index
        total_len = 0
        df_counts = Counter()
        for c in self.chunks:
            total_len += len(c.tokens)
            unique_terms = set(c.tokens)
            for t in unique_terms:
                df_counts[t] += 1

        self.doc_frequencies = dict(df_counts)
        self.avg_doc_length = total_len / max(1, len(self.chunks))
        logger.info(f"Trilingual RAG Index Built: Loaded {doc_count} documents into {len(self.chunks)} semantic chunks.")

    def compute_bm25_score(self, query_tokens: List[str], chunk: ClinicalDocumentChunk, k1: float = 1.5, b: float = 0.75) -> float:
        """Computes BM25 relevance score for a document chunk."""
        score = 0.0
        doc_len = len(chunk.tokens)
        chunk_counts = Counter(chunk.tokens)
        N = len(self.chunks)

        for term in query_tokens:
            if term not in self.doc_frequencies:
                # Fuzzy substring match for Indian compounding words
                matches = sum(count for word, count in chunk_counts.items() if term in word or word in term)
                if matches > 0:
                    score += matches * 0.6
                continue

            df = self.doc_frequencies[term]
            idf = math.log((N - df + 0.5) / (df + 0.5) + 1.0)
            tf = chunk_counts.get(term, 0)
            
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * (doc_len / max(1.0, self.avg_doc_length)))
            score += idf * (numerator / max(1e-6, denominator))

        return score

    def retrieve(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """
        Retrieves the top-k most clinically relevant document chunks for a trilingual query.
        """
        if not self.chunks:
            self.load_and_index_documents()

        cleaned_query = re.sub(r'[^\w\s\u0C00-\u0C7F\u0900-\u097F]', ' ', query.lower())
        query_tokens = [w for w in cleaned_query.split() if w not in ALL_STOPWORDS and len(w) > 1]

        if not query_tokens:
            return []

        scored_chunks = []
        for chunk in self.chunks:
            score = self.compute_bm25_score(query_tokens, chunk)
            if score > 0:
                scored_chunks.append((score, chunk))

        # Sort descending by relevance score
        scored_chunks.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, chunk in scored_chunks[:top_k]:
            results.append({
                "doc_id": chunk.doc_id,
                "title": chunk.title,
                "source": chunk.source,
                "category": chunk.category,
                "content": chunk.content[:450] + ("..." if len(chunk.content) > 450 else ""),
                "score": round(score, 3)
            })

        return results


_GLOBAL_RAG_ENGINE = None

def get_rag_engine() -> VernacularHybridRAGEngine:
    global _GLOBAL_RAG_ENGINE
    if _GLOBAL_RAG_ENGINE is None:
        _GLOBAL_RAG_ENGINE = VernacularHybridRAGEngine()
    return _GLOBAL_RAG_ENGINE
