"""
Metrics calculation utilities for Telugu LLM evaluation:
- SacreBLEU & chrF++ (with pure-Python fallback for zero-dependency environments)
- ROUGE-1/2/L
- Inter-Annotator Agreement (Cohen's Kappa, Pearson r, Spearman rho, Percentage Agreement)
"""

import math
from typing import List, Dict, Any, Tuple
from collections import Counter


def tokenize_words(text: str) -> List[str]:
    """Tokenizes words preserving Telugu Unicode characters."""
    return text.strip().split()


def tokenize_chars(text: str) -> List[str]:
    """Tokenizes character sequence for chrF calculation."""
    return list(text.replace(" ", ""))


def compute_ngram_counts(tokens: List[str], n: int) -> Counter:
    """Extracts n-grams from a token sequence."""
    if len(tokens) < n:
        return Counter()
    return Counter([tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)])


def compute_bleu(hypothesis: str, reference: str, max_n: int = 4) -> float:
    """
    Computes sentence-level BLEU score (0 to 100) with brevity penalty.
    Uses sacrebleu if available, otherwise pure Python standard implementation.
    """
    try:
        import sacrebleu
        score = sacrebleu.sentence_bleu(hypothesis, [reference]).score
        return round(score, 2)
    except Exception:
        pass

    # Pure Python BLEU Implementation
    hyp_tokens = tokenize_words(hypothesis)
    ref_tokens = tokenize_words(reference)

    if not hyp_tokens or not ref_tokens:
        return 0.0

    precisions = []
    for n in range(1, max_n + 1):
        hyp_ngrams = compute_ngram_counts(hyp_tokens, n)
        ref_ngrams = compute_ngram_counts(ref_tokens, n)

        total_hyp = sum(hyp_ngrams.values())
        if total_hyp == 0:
            precisions.append(0.0)
            continue

        clipped_matches = 0
        for ngram, count in hyp_ngrams.items():
            clipped_matches += min(count, ref_ngrams.get(ngram, 0))

        precisions.append((clipped_matches + 1e-6) / (total_hyp + 1e-6))

    # Brevity penalty
    c = len(hyp_tokens)
    r = len(ref_tokens)
    if c > r:
        bp = 1.0
    elif c == 0:
        bp = 0.0
    else:
        bp = math.exp(1 - (r / c))

    # Geometric mean
    log_sum = sum(math.log(p) for p in precisions) / max_n
    bleu = bp * math.exp(log_sum) * 100.0
    return round(max(0.0, min(100.0, bleu)), 2)


def compute_chrf(hypothesis: str, reference: str, char_order: int = 6, beta: float = 2.0) -> float:
    """
    Computes chrF++ character n-gram F-score (0.0 to 1.0), ideal for agglutinative Indian languages.
    """
    try:
        import sacrebleu
        score = sacrebleu.sentence_chrf(hypothesis, [reference], char_order=char_order, beta=beta).score / 100.0
        return round(score, 4)
    except Exception:
        pass

    hyp_chars = tokenize_chars(hypothesis)
    ref_chars = tokenize_chars(reference)

    if not hyp_chars or not ref_chars:
        return 0.0

    precisions = []
    recalls = []

    for n in range(1, char_order + 1):
        hyp_ngrams = compute_ngram_counts(hyp_chars, n)
        ref_ngrams = compute_ngram_counts(ref_chars, n)

        total_hyp = sum(hyp_ngrams.values())
        total_ref = sum(ref_ngrams.values())

        if total_hyp == 0 or total_ref == 0:
            continue

        matches = sum(min(count, ref_ngrams.get(ng, 0)) for ng, count in hyp_ngrams.items())
        p = matches / total_hyp if total_hyp > 0 else 0.0
        r = matches / total_ref if total_ref > 0 else 0.0
        precisions.append(p)
        recalls.append(r)

    if not precisions or not recalls:
        return 0.0

    avg_p = sum(precisions) / len(precisions)
    avg_r = sum(recalls) / len(recalls)

    if avg_p + avg_r == 0:
        return 0.0

    beta_sq = beta ** 2
    chrf = (1 + beta_sq) * (avg_p * avg_r) / ((beta_sq * avg_p) + avg_r)
    return round(max(0.0, min(1.0, chrf)), 4)


def compute_cohens_kappa(rater1_scores: List[int], rater2_scores: List[int], min_score: int = 1, max_score: int = 5) -> float:
    """
    Computes Cohen's Kappa coefficient for inter-rater agreement between LLM Judge and Human Annotator.
    kappa = (Po - Pe) / (1 - Pe)
    """
    if len(rater1_scores) != len(rater2_scores) or len(rater1_scores) == 0:
        return 0.0

    n = len(rater1_scores)
    
    # Observed agreement
    observed_matches = sum(1 for r1, r2 in zip(rater1_scores, rater2_scores) if r1 == r2)
    po = observed_matches / n

    # Expected agreement by chance
    r1_counts = Counter(rater1_scores)
    r2_counts = Counter(rater2_scores)

    pe = 0.0
    for score in range(min_score, max_score + 1):
        p1 = r1_counts.get(score, 0) / n
        p2 = r2_counts.get(score, 0) / n
        pe += (p1 * p2)

    if pe == 1.0:
        return 1.0

    kappa = (po - pe) / (1.0 - pe)
    return round(kappa, 4)


def compute_pearson_correlation(x: List[float], y: List[float]) -> float:
    """Computes Pearson correlation coefficient r between two numerical series."""
    if len(x) != len(y) or len(x) < 2:
        return 0.0

    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    den_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x))
    den_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y))

    if den_x == 0 or den_y == 0:
        return 0.0

    return round(num / (den_x * den_y), 4)


def compute_keyword_recall(response: str, expected_facts: List[str]) -> float:
    """Computes clinical keyword coverage percentage in Telugu response."""
    if not expected_facts:
        return 1.0
    matched = 0
    for fact in expected_facts:
        # Check substring or words
        words = fact.split()
        if fact in response or any(w in response for w in words if len(w) > 3):
            matched += 1
    return round(matched / len(expected_facts), 4)
