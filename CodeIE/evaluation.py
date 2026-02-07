#!/usr/bin/env python3
"""
NER Evaluation Module for CodeIE Experiments

This module provides evaluation metrics for Named Entity Recognition:
- Micro F1 (overall entity-level)
- Macro F1 (average across entity types)
- Per-type precision, recall, and F1

The evaluation uses string-based matching: an entity is correct if both
the type AND text match exactly (case-sensitive).
"""

from collections import defaultdict
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import json


@dataclass
class EntityMetrics:
    """Metrics for a single entity type."""
    entity_type: str
    tp: int = 0
    fp: int = 0
    fn: int = 0
    
    @property
    def precision(self) -> float:
        """Precision = TP / (TP + FP)"""
        return self.tp / (self.tp + self.fp) if (self.tp + self.fp) > 0 else 0.0
    
    @property
    def recall(self) -> float:
        """Recall = TP / (TP + FN)"""
        return self.tp / (self.tp + self.fn) if (self.tp + self.fn) > 0 else 0.0
    
    @property
    def f1(self) -> float:
        """F1 = 2 * P * R / (P + R)"""
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if (p + r) > 0 else 0.0
    
    @property
    def support(self) -> int:
        """Total gold instances for this type."""
        return self.tp + self.fn
    
    def to_dict(self) -> Dict:
        return {
            'type': self.entity_type,
            'precision': round(self.precision * 100, 2),
            'recall': round(self.recall * 100, 2),
            'f1': round(self.f1 * 100, 2),
            'support': self.support,
            'tp': self.tp,
            'fp': self.fp,
            'fn': self.fn
        }


@dataclass
class EvaluationResult:
    """Complete evaluation results."""
    # Per-type metrics
    per_type_metrics: Dict[str, EntityMetrics] = field(default_factory=dict)
    
    # Overall counts
    total_tp: int = 0
    total_fp: int = 0
    total_fn: int = 0
    
    @property
    def micro_precision(self) -> float:
        """Micro-averaged precision."""
        return self.total_tp / (self.total_tp + self.total_fp) if (self.total_tp + self.total_fp) > 0 else 0.0
    
    @property
    def micro_recall(self) -> float:
        """Micro-averaged recall."""
        return self.total_tp / (self.total_tp + self.total_fn) if (self.total_tp + self.total_fn) > 0 else 0.0
    
    @property
    def micro_f1(self) -> float:
        """Micro-averaged F1 (same as overall F1)."""
        p, r = self.micro_precision, self.micro_recall
        return 2 * p * r / (p + r) if (p + r) > 0 else 0.0
    
    @property
    def macro_precision(self) -> float:
        """Macro-averaged precision (average across types with support > 0)."""
        valid_types = [m for m in self.per_type_metrics.values() if m.support > 0]
        if not valid_types:
            return 0.0
        return sum(m.precision for m in valid_types) / len(valid_types)
    
    @property
    def macro_recall(self) -> float:
        """Macro-averaged recall (average across types with support > 0)."""
        valid_types = [m for m in self.per_type_metrics.values() if m.support > 0]
        if not valid_types:
            return 0.0
        return sum(m.recall for m in valid_types) / len(valid_types)
    
    @property
    def macro_f1(self) -> float:
        """Macro-averaged F1 (average of per-type F1 scores)."""
        valid_types = [m for m in self.per_type_metrics.values() if m.support > 0]
        if not valid_types:
            return 0.0
        return sum(m.f1 for m in valid_types) / len(valid_types)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary format."""
        return {
            'micro': {
                'precision': round(self.micro_precision * 100, 2),
                'recall': round(self.micro_recall * 100, 2),
                'f1': round(self.micro_f1 * 100, 2),
            },
            'macro': {
                'precision': round(self.macro_precision * 100, 2),
                'recall': round(self.macro_recall * 100, 2),
                'f1': round(self.macro_f1 * 100, 2),
            },
            'counts': {
                'tp': self.total_tp,
                'fp': self.total_fp,
                'fn': self.total_fn,
                'total_gold': self.total_tp + self.total_fn,
                'total_pred': self.total_tp + self.total_fp,
            },
            'per_type': {k: v.to_dict() for k, v in sorted(self.per_type_metrics.items())}
        }
    
    def summary(self, include_per_type: bool = False) -> str:
        """Generate a human-readable summary."""
        lines = [
            "=" * 60,
            "                 EVALUATION RESULTS",
            "=" * 60,
            "",
            f"Micro F1:  {self.micro_f1 * 100:6.2f}%  (P: {self.micro_precision * 100:.2f}%, R: {self.micro_recall * 100:.2f}%)",
            f"Macro F1:  {self.macro_f1 * 100:6.2f}%  (P: {self.macro_precision * 100:.2f}%, R: {self.macro_recall * 100:.2f}%)",
            "",
            f"TP: {self.total_tp}, FP: {self.total_fp}, FN: {self.total_fn}",
            f"Total Gold: {self.total_tp + self.total_fn}, Total Pred: {self.total_tp + self.total_fp}",
        ]
        
        if include_per_type and self.per_type_metrics:
            lines.append("")
            lines.append("-" * 60)
            lines.append("Per-Type Metrics:")
            lines.append("-" * 60)
            lines.append(f"{'Type':<30} {'P':>8} {'R':>8} {'F1':>8} {'Support':>8}")
            lines.append("-" * 60)
            
            for etype in sorted(self.per_type_metrics.keys()):
                m = self.per_type_metrics[etype]
                if m.support > 0:  # Only show types with gold examples
                    lines.append(
                        f"{etype:<30} {m.precision*100:>7.1f}% {m.recall*100:>7.1f}% {m.f1*100:>7.1f}% {m.support:>8}"
                    )
        
        lines.append("=" * 60)
        return "\n".join(lines)


def evaluate_ner(
    gold_list: List[List[Dict]],
    pred_list: List[List[Dict]],
    entity_types: Optional[List[str]] = None
) -> EvaluationResult:
    """
    Evaluate NER predictions against gold standard.
    
    Args:
        gold_list: List of gold entity lists. Each entity is a dict with 'text' and 'type'.
                   Example: [[{'text': 'Apple', 'type': 'organization'}], ...]
        pred_list: List of predicted entity lists, same format as gold_list.
        entity_types: Optional list of entity types to include. If None, auto-detect from data.
    
    Returns:
        EvaluationResult with micro/macro metrics and per-type breakdown.
    """
    result = EvaluationResult()
    
    # Auto-detect entity types if not provided
    if entity_types is None:
        entity_types = set()
        for entities in gold_list + pred_list:
            for e in entities:
                entity_types.add(e.get('type', 'UNKNOWN'))
        entity_types = sorted(entity_types)
    
    # Initialize per-type metrics
    for etype in entity_types:
        result.per_type_metrics[etype] = EntityMetrics(entity_type=etype)
    
    # Process each instance
    for gold_entities, pred_entities in zip(gold_list, pred_list):
        # Convert to sets of (type, text) tuples for comparison
        gold_set = set((e.get('type', 'UNKNOWN'), e.get('text', '')) for e in gold_entities)
        pred_set = set((e.get('type', 'UNKNOWN'), e.get('text', '')) for e in pred_entities)
        
        # True positives: in both gold and pred
        tp_set = gold_set & pred_set
        # False positives: in pred but not gold
        fp_set = pred_set - gold_set
        # False negatives: in gold but not pred
        fn_set = gold_set - pred_set
        
        # Update overall counts
        result.total_tp += len(tp_set)
        result.total_fp += len(fp_set)
        result.total_fn += len(fn_set)
        
        # Update per-type metrics
        for etype, text in tp_set:
            if etype in result.per_type_metrics:
                result.per_type_metrics[etype].tp += 1
            else:
                result.per_type_metrics[etype] = EntityMetrics(entity_type=etype, tp=1)
        
        for etype, text in fp_set:
            if etype in result.per_type_metrics:
                result.per_type_metrics[etype].fp += 1
            else:
                result.per_type_metrics[etype] = EntityMetrics(entity_type=etype, fp=1)
        
        for etype, text in fn_set:
            if etype in result.per_type_metrics:
                result.per_type_metrics[etype].fn += 1
            else:
                result.per_type_metrics[etype] = EntityMetrics(entity_type=etype, fn=1)
    
    return result


def evaluate_from_files(
    gold_file: str,
    pred_file: str,
    entity_types: Optional[List[str]] = None
) -> EvaluationResult:
    """
    Evaluate from JSONL files.
    
    Each line should be a JSON object with an 'entity' key containing a list of entities.
    Each entity should have 'text' and 'type' keys.
    
    Args:
        gold_file: Path to gold JSONL file
        pred_file: Path to predictions JSONL file
        entity_types: Optional list of entity types
    
    Returns:
        EvaluationResult
    """
    gold_list = []
    pred_list = []
    
    with open(gold_file, 'r') as f:
        for line in f:
            data = json.loads(line.strip())
            entities = data.get('entity', [])
            gold_list.append(entities)
    
    with open(pred_file, 'r') as f:
        for line in f:
            data = json.loads(line.strip())
            entities = data.get('entity', [])
            pred_list.append(entities)
    
    if len(gold_list) != len(pred_list):
        raise ValueError(f"Mismatch: {len(gold_list)} gold instances vs {len(pred_list)} predictions")
    
    return evaluate_ner(gold_list, pred_list, entity_types)


# Backwards compatibility with original function signature
def evaluate_predictions(
    gold_list: List[List[Dict]],
    pred_list: List[List[Dict]]
) -> Dict[str, float]:
    """
    Backwards-compatible evaluation function.
    
    Returns a simple dict with micro metrics (same as original implementation).
    For full metrics including macro F1, use evaluate_ner() instead.
    """
    result = evaluate_ner(gold_list, pred_list)
    return {
        'precision': result.micro_precision,
        'recall': result.micro_recall,
        'f1': result.micro_f1,
        'micro_f1': result.micro_f1,
        'macro_f1': result.macro_f1,
        'tp': result.total_tp,
        'gold_count': result.total_tp + result.total_fn,
        'pred_count': result.total_tp + result.total_fp
    }


if __name__ == "__main__":
    # Simple test
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate NER predictions")
    parser.add_argument('--gold', '-g', required=True, help='Gold JSONL file')
    parser.add_argument('--pred', '-p', required=True, help='Predictions JSONL file')
    parser.add_argument('--per-type', action='store_true', help='Show per-type metrics')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    result = evaluate_from_files(args.gold, args.pred)
    
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(result.summary(include_per_type=args.per_type))
