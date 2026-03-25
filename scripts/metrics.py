#!/usr/bin/env python3
"""
Epstein Project — Evaluation Metrics Module

Comprehensive accuracy metrics for OCR, NER, Facial Recognition,
and Knowledge Graph evaluation.

Usage:
  from metrics import character_error_rate, compute_ner_metrics, compute_verification_metrics
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

import numpy as np

# =============================================================================
# OCR Metrics
# =============================================================================

def levenshtein_distance(reference: str, hypothesis: str) -> Tuple[int, int, int, int]:
    """Compute Levenshtein distance with operation counts.

    Args:
        reference: Ground truth text.
        hypothesis: OCR output text.

    Returns:
        Tuple of (total_distance, substitutions, deletions, insertions).
    """
    ref_len = len(reference)
    hyp_len = len(hypothesis)

    d = np.zeros((ref_len + 1, hyp_len + 1), dtype=int)
    for i in range(ref_len + 1):
        d[i][0] = i
    for j in range(hyp_len + 1):
        d[0][j] = j

    for i in range(1, ref_len + 1):
        for j in range(1, hyp_len + 1):
            if reference[i-1] == hypothesis[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min(d[i-1][j-1] + 1, d[i-1][j] + 1, d[i][j-1] + 1)

    # Backtrack to count operations
    i, j = ref_len, hyp_len
    subs, dels, ins = 0, 0, 0
    while i > 0 or j > 0:
        if i > 0 and j > 0 and reference[i-1] == hypothesis[j-1]:
            i, j = i-1, j-1
        elif i > 0 and j > 0 and d[i][j] == d[i-1][j-1] + 1:
            subs += 1
            i, j = i-1, j-1
        elif i > 0 and d[i][j] == d[i-1][j] + 1:
            dels += 1
            i -= 1
        else:
            ins += 1
            j -= 1

    return d[ref_len][hyp_len], subs, dels, ins


def character_error_rate(reference: str, hypothesis: str) -> float:
    """Calculate Character Error Rate (CER).

    CER = (S + D + I) / N * 100

    Returns:
        CER as percentage (0.0 = perfect).
    """
    distance, subs, dels, ins = levenshtein_distance(reference, hypothesis)
    n = len(reference)
    if n == 0:
        return 0.0 if len(hypothesis) == 0 else 100.0
    return (subs + dels + ins) / n * 100


def word_error_rate(reference: str, hypothesis: str) -> float:
    """Calculate Word Error Rate (WER).

    WER = (S_words + D_words + I_words) / N_words * 100
    """
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    ref_len = len(ref_words)
    hyp_len = len(hyp_words)

    d = np.zeros((ref_len + 1, hyp_len + 1), dtype=int)
    for i in range(ref_len + 1):
        d[i][0] = i
    for j in range(hyp_len + 1):
        d[0][j] = j

    for i in range(1, ref_len + 1):
        for j in range(1, hyp_len + 1):
            if ref_words[i-1] == hyp_words[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min(d[i-1][j-1] + 1, d[i-1][j] + 1, d[i][j-1] + 1)

    if ref_len == 0:
        return 0.0 if hyp_len == 0 else 100.0
    return d[ref_len][hyp_len] / ref_len * 100


# OCR-aware substitution costs (common confusions)
OCR_SUB_COSTS = {
    ('O', '0'): 0.1, ('0', 'O'): 0.1,
    ('1', 'l'): 0.1, ('l', '1'): 0.1,
    ('1', 'I'): 0.1, ('I', '1'): 0.1,
    ('5', 'S'): 0.2, ('S', '5'): 0.2,
    ('8', 'B'): 0.2, ('B', '8'): 0.2,
}


def weighted_levenshtein(reference: str, hypothesis: str,
                         sub_costs: dict = None) -> float:
    """Weighted Levenshtein distance with OCR-aware costs."""
    if sub_costs is None:
        sub_costs = OCR_SUB_COSTS

    ref_len, hyp_len = len(reference), len(hypothesis)
    d = np.zeros((ref_len + 1, hyp_len + 1))
    for i in range(ref_len + 1):
        d[i][0] = i
    for j in range(hyp_len + 1):
        d[0][j] = j

    for i in range(1, ref_len + 1):
        for j in range(1, hyp_len + 1):
            if reference[i-1] == hypothesis[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                pair = (reference[i-1], hypothesis[j-1])
                sub_cost = sub_costs.get(pair, 1.0)
                d[i][j] = min(d[i-1][j-1] + sub_cost, d[i-1][j] + 1, d[i][j-1] + 1)

    return d[ref_len][hyp_len]


# =============================================================================
# NER Metrics
# =============================================================================

@dataclass
class EntitySpan:
    """Named entity span for evaluation."""
    entity_type: str
    start: int
    end: int
    text: str = ""

    def __hash__(self):
        return hash((self.entity_type, self.start, self.end))

    def __eq__(self, other):
        return (self.entity_type == other.entity_type and
                self.start == other.start and
                self.end == other.end)


def compute_ner_metrics(true_entities: List[EntitySpan],
                        pred_entities: List[EntitySpan],
                        entity_types: List[str] = None) -> Dict:
    """Compute NER metrics under 4 evaluation schemas.

    Schemas:
      - strict: exact boundary + exact type
      - exact: exact boundary, any type
      - partial: any overlap, any type
      - type: any overlap + exact type
    """
    if entity_types is None:
        entity_types = list(set(e.entity_type for e in true_entities + pred_entities))

    results = {}
    for schema in ['strict', 'exact', 'partial', 'type']:
        results[schema] = _ner_schema(true_entities, pred_entities, schema)

    results['by_type'] = {}
    for ent_type in entity_types:
        t = [e for e in true_entities if e.entity_type == ent_type]
        p = [e for e in pred_entities if e.entity_type == ent_type]
        results['by_type'][ent_type] = {s: _ner_schema(t, p, s) for s in ['strict', 'exact', 'partial', 'type']}

    return results


def _ner_schema(true_ents: List[EntitySpan], pred_ents: List[EntitySpan],
                schema: str) -> Dict:
    """Compute metrics for a specific NER evaluation schema."""
    correct, partial_count, missed = 0, 0, 0
    matched = set()

    for true_ent in true_ents:
        found = False
        for j, pred_ent in enumerate(pred_ents):
            if j in matched:
                continue
            overlap = not (true_ent.end < pred_ent.start or pred_ent.end < true_ent.start)

            if schema == 'strict':
                match = true_ent == pred_ent
            elif schema == 'exact':
                match = true_ent.start == pred_ent.start and true_ent.end == pred_ent.end
            elif schema in ('partial', 'type'):
                if schema == 'type':
                    match = overlap and true_ent.entity_type == pred_ent.entity_type
                else:
                    match = overlap
                if match:
                    if true_ent.start == pred_ent.start and true_ent.end == pred_ent.end:
                        correct += 1
                    else:
                        partial_count += 1
                    matched.add(j)
                    found = True
                    break
                continue
            else:
                match = False

            if match:
                correct += 1
                matched.add(j)
                found = True
                break

        if not found:
            missed += 1

    spurious = len(pred_ents) - len(matched)
    possible = len(true_ents)
    actual = len(pred_ents)

    if schema in ('strict', 'exact'):
        precision = correct / actual if actual > 0 else 0.0
        recall = correct / possible if possible > 0 else 0.0
    else:
        precision = (correct + 0.5 * partial_count) / actual if actual > 0 else 0.0
        recall = (correct + 0.5 * partial_count) / possible if possible > 0 else 0.0

    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        'correct': correct, 'partial': partial_count,
        'missed': missed, 'spurious': spurious,
        'possible': possible, 'actual': actual,
        'precision': precision, 'recall': recall, 'f1': f1,
    }


# =============================================================================
# Facial Recognition Metrics
# =============================================================================

def compute_verification_metrics(similarity_scores: np.ndarray,
                                 labels: np.ndarray) -> Dict:
    """Compute facial verification metrics (1:1).

    Args:
        similarity_scores: Pairwise similarity scores.
        labels: 1 for genuine pairs, 0 for impostor pairs.

    Returns:
        Dict with AUC, EER, TAR@FAR, and curve data.
    """
    from sklearn.metrics import auc, roc_curve

    fpr, tpr, thresholds = roc_curve(labels, similarity_scores)
    auc_score = auc(fpr, tpr)

    # EER: where FPR == FNR
    fnr = 1 - tpr
    eer_idx = np.nanargmin(np.absolute(fnr - fpr))
    eer = fpr[eer_idx]

    # TAR at specific FARs
    tar_at_far = {}
    for target_far in [0.001, 0.01, 0.1]:
        idx = np.where(fpr <= target_far)[0]
        tar_at_far[f'tar@far={target_far}'] = tpr[idx[-1]] if len(idx) > 0 else 0.0

    # d-prime (distribution separability)
    genuine_scores = similarity_scores[labels == 1]
    impostor_scores = similarity_scores[labels == 0]
    d_prime = 0.0
    if len(genuine_scores) > 0 and len(impostor_scores) > 0:
        pooled_var = 0.5 * (np.var(genuine_scores) + np.var(impostor_scores))
        if pooled_var > 0:
            d_prime = (np.mean(genuine_scores) - np.mean(impostor_scores)) / np.sqrt(pooled_var)

    return {
        'auc': auc_score,
        'eer': eer,
        'eer_threshold': thresholds[eer_idx],
        'd_prime': d_prime,
        'genuine_mean': float(np.mean(genuine_scores)) if len(genuine_scores) > 0 else 0,
        'genuine_std': float(np.std(genuine_scores)) if len(genuine_scores) > 0 else 0,
        'impostor_mean': float(np.mean(impostor_scores)) if len(impostor_scores) > 0 else 0,
        'impostor_std': float(np.std(impostor_scores)) if len(impostor_scores) > 0 else 0,
        **tar_at_far,
    }


def identification_rate(probe_embeddings: np.ndarray,
                        gallery_embeddings: np.ndarray,
                        probe_labels: np.ndarray,
                        gallery_labels: np.ndarray,
                        k_values: List[int] = None) -> Dict:
    """Compute rank-k identification rate (1:N).

    Args:
        probe_embeddings: Query face embeddings.
        gallery_embeddings: Database face embeddings.
        probe_labels: True identity labels for probes.
        gallery_labels: True identity labels for gallery.
        k_values: Rank values to evaluate (default: [1, 5, 10]).

    Returns:
        Dict with rank-k rates and CMC curve.
    """
    if k_values is None:
        k_values = [1, 5, 10]

    from sklearn.metrics.pairwise import cosine_similarity
    sim_matrix = cosine_similarity(probe_embeddings, gallery_embeddings)

    results = {}
    for k in k_values:
        correct = 0
        for i, label in enumerate(probe_labels):
            top_k = np.argsort(sim_matrix[i])[::-1][:k]
            if label in gallery_labels[top_k]:
                correct += 1
        results[f'rank_{k}'] = correct / len(probe_labels)

    return results


# =============================================================================
# Knowledge Graph Metrics
# =============================================================================

def pairwise_precision(prediction: Dict[str, str],
                       reference: Dict[str, str]) -> float:
    """Pairwise precision for entity resolution."""
    pred_pairs = _get_pairs(prediction)
    ref_pairs = _get_pairs(reference)
    if len(pred_pairs) == 0:
        return 0.0
    return len(pred_pairs & ref_pairs) / len(pred_pairs)


def pairwise_recall(prediction: Dict[str, str],
                    reference: Dict[str, str]) -> float:
    """Pairwise recall for entity resolution."""
    pred_pairs = _get_pairs(prediction)
    ref_pairs = _get_pairs(reference)
    if len(ref_pairs) == 0:
        return 0.0
    return len(pred_pairs & ref_pairs) / len(ref_pairs)


def _get_pairs(clustering: Dict[str, str]) -> Set[Tuple[str, str]]:
    """Get all pairs of records in the same cluster."""
    clusters = defaultdict(set)
    for record, cluster in clustering.items():
        clusters[cluster].add(record)
    pairs = set()
    for records in clusters.values():
        sorted_r = sorted(records)
        for i in range(len(sorted_r)):
            for j in range(i + 1, len(sorted_r)):
                pairs.add((sorted_r[i], sorted_r[j]))
    return pairs


def b_cubed_f1(prediction: Dict[str, str],
               reference: Dict[str, str]) -> Tuple[float, float, float]:
    """B-Cubed precision, recall, F1 for entity resolution."""
    pred_clusters = defaultdict(set)
    ref_clusters = defaultdict(set)
    for r, c in prediction.items():
        pred_clusters[c].add(r)
    for r, c in reference.items():
        ref_clusters[c].add(r)

    records = set(prediction.keys()) & set(reference.keys())
    if not records:
        return 0.0, 0.0, 0.0

    prec_sum, rec_sum = 0.0, 0.0
    for r in records:
        pc = pred_clusters[prediction[r]]
        rc = ref_clusters[reference[r]]
        correct = len(pc & rc)
        prec_sum += correct / len(pc)
        rec_sum += correct / len(rc)

    p = prec_sum / len(records)
    r = rec_sum / len(records)
    f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
    return p, r, f1


def relationship_precision(predicted: List[Tuple[str, str, str]],
                           reference: Set[Tuple[str, str, str]]) -> float:
    """Precision of extracted relationship triples."""
    if len(predicted) == 0:
        return 0.0
    return sum(1 for t in predicted if t in reference) / len(predicted)


# =============================================================================
# Evaluation Runner
# =============================================================================

@dataclass
class OCRMetrics:
    """Container for OCR evaluation results."""
    cer: float = 0.0
    wer: float = 0.0
    weighted_lev: float = 0.0
    substitutions: int = 0
    deletions: int = 0
    insertions: int = 0
    total_chars_ref: int = 0
    total_chars_hyp: int = 0


def evaluate_ocr_page(reference: str, hypothesis: str) -> OCRMetrics:
    """Evaluate a single OCR page against ground truth."""
    dist, subs, dels, ins = levenshtein_distance(reference, hypothesis)
    return OCRMetrics(
        cer=character_error_rate(reference, hypothesis),
        wer=word_error_rate(reference, hypothesis),
        weighted_lev=weighted_levenshtein(reference, hypothesis),
        substitutions=subs, deletions=dels, insertions=ins,
        total_chars_ref=len(reference), total_chars_hyp=len(hypothesis),
    )
