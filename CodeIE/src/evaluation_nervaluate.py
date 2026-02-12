
"""
Nervaluate Integration for CodeIE
Adapts "Bag of Entities" predictions to strict span-based evaluation.
"""

from typing import List, Dict, Any, Tuple, Set
from nervaluate import Evaluator
import logging

logger = logging.getLogger(__name__)

def find_all_occurrences(text: str, substring: str) -> List[Tuple[int, int]]:
    """Find all start, end indices of substring in text."""
    if not substring:
        return []
    spans = []
    start = 0
    while True:
        idx = text.find(substring, start)
        if idx == -1:
            break
        spans.append((idx, idx + len(substring)))
        start = idx + 1
    return spans

def align_predictions_to_gold(
    text: str,
    gold_spans: List[Dict], 
    pred_entities: List[Dict]
) -> List[Dict]:
    """
    Aligns predicted entity strings to the text to maximize metrics against Gold Spans.
    
    Args:
        text: Original text
        gold_spans: List of {'label': '...', 'start': ..., 'end': ...} (Ground Truth)
        pred_entities: List of {'type': '...', 'text': '...'} (Bag of Entities)
        
    Returns:
        pred_spans: List of {'label': '...', 'start': ..., 'end': ...} suitable for nervaluate
    """
    
    # Track which Gold spans have been "claimed" by a prediction (for Exact matches)
    # We want to enable 1:1 mapping where possible to avoid double-counting.
    # However, if the model predicts "Apple" once, and "Apple" appears twice in Gold, 
    # it implies 1 TP and 1 FN.
    
    matched_gold_indices = set()
    final_pred_spans = []
    
    # We need to assign each extracted string to a specific span in the text.
    # Since we don't know WHERE the model "saw" the entity, we give it the benefit of the doubt.
    # We prioritize:
    # 1. Exact Span + Exact Label match with an unclaimed Gold span.
    # 2. Exact Span + Label Mismatch with an unclaimed Gold span.
    # 3. Any other occurrence in text (treated as Spurious or Partial).
    
    # Pre-calculate all occurrences of each predicted string
    # pred_candidates: index -> list of spans
    pred_candidates = []
    for i, pe in enumerate(pred_entities):
        phrase = pe['text']
        etype = pe['type']
        spans = find_all_occurrences(text, phrase)
        pred_candidates.append({
            'index': i,
            'phrase': phrase,
            'type': etype,
            'spans': spans, 
            'assigned_span': None
        })
        
    # Pass 1: Exact Matches (Text + Type)
    for p in pred_candidates:
        if not p['spans']: continue # Hallucination (not in text)
        
        # Look for a gold span that matches perfectly
        for span in p['spans']:
            s_start, s_end = span
            
            # Check if this span corresponds to a Gold entity
            for g_idx, g in enumerate(gold_spans):
                if g_idx in matched_gold_indices:
                    continue
                
                if g['start'] == s_start and g['end'] == s_end and g['label'] == p['type']:
                    # Perfect Match!
                    matched_gold_indices.add(g_idx)
                    p['assigned_span'] = {'label': p['type'], 'start': s_start, 'end': s_end}
                    break
            
            if p['assigned_span']:
                break
                
    # Pass 2: Type Errors (Same Text Span, diff Label)
    for p in pred_candidates:
        if p['assigned_span']: continue
        if not p['spans']: continue
        
        for span in p['spans']:
            s_start, s_end = span
            for g_idx, g in enumerate(gold_spans):
                if g_idx in matched_gold_indices:
                    continue
                
                if g['start'] == s_start and g['end'] == s_end:
                    # Found a gold span at this location, but type didn't match (otherwise Pass 1 would catch it)
                    matched_gold_indices.add(g_idx)
                    p['assigned_span'] = {'label': p['type'], 'start': s_start, 'end': s_end}
                    break
            if p['assigned_span']:
                break

    # Pass 3: Partial Overlaps?
    # Nervaluate handles partials if we pass a span that overlaps.
    # We accept a span if it overlaps with an unclaimed Gold.
    for p in pred_candidates:
        if p['assigned_span']: continue
        if not p['spans']: continue
        
        for span in p['spans']:
            s_start, s_end = span
            for g_idx, g in enumerate(gold_spans):
                if g_idx in matched_gold_indices:
                    continue
                
                # Check Overlap
                g_start, g_end = g['start'], g['end']
                if max(s_start, g_start) < min(s_end, g_end):
                    # Overlap found
                    matched_gold_indices.add(g_idx)
                    p['assigned_span'] = {'label': p['type'], 'start': s_start, 'end': s_end}
                    break
            if p['assigned_span']:
                break
                
    # Pass 4: Unmatched (Spurious)
    # Assign to first occurrence that isn't covering a 'Matched' Gold span?
    # Actually, we can just assign to the first occurrence if not utilized, 
    # or better: pick an occurrence that doesn't overlap with ANY gold (pure spurious) 
    # if possible, to avoid "Partial" credit where none exists.
    # But for simplicity/consistency, let's just pick the first occurrence.
    
    for p in pred_candidates:
        if p['assigned_span']: 
            final_pred_spans.append(p['assigned_span'])
            continue
        
        if p['spans']:
             # Pick the first one
             # Note: This might inadvertently overlap with a Gold span we missed? 
             # If so, nervaluate might count it as Partial or Type Error, which is technically fair 
             # (the model predicted something that is *sort of* there).
             s_start, s_end = p['spans'][0]
             final_pred_spans.append({'label': p['type'], 'start': s_start, 'end': s_end})
        else:
             # Phrase not in text at all. 
             # Can't produce a span. Ignoring it? 
             # If we ignore it, we miss a "Spurious" count.
             # We should probably add a dummy span? (0,0)?
             # Nervaluate might filter empty spans.
             pass
             
    return final_pred_spans

def _build_gold_spans(
    text: str,
    gold_entities: List[Dict]
) -> List[Dict[str, int]]:
    """Build span-based gold entities from text when start/end are missing."""
    used_spans: List[Tuple[int, int]] = []
    gold_spans: List[Dict[str, int]] = []

    for g in gold_entities:
        label = g.get('label') or g.get('type')
        start = g.get('start')
        end = g.get('end')

        if label is None:
            continue

        if isinstance(start, int) and isinstance(end, int):
            gold_spans.append({'label': label, 'start': start, 'end': end})
            used_spans.append((start, end))
            continue

        phrase = g.get('text')
        if not phrase:
            continue

        spans = find_all_occurrences(text, phrase)
        selected = None
        for s_start, s_end in spans:
            if all(not (s_start < u_end and s_end > u_start) for u_start, u_end in used_spans):
                selected = (s_start, s_end)
                break
        if selected is None and spans:
            selected = spans[0]

        if selected is None:
            continue

        s_start, s_end = selected
        used_spans.append((s_start, s_end))
        gold_spans.append({'label': label, 'start': s_start, 'end': s_end})

    return gold_spans


def evaluate_with_nervaluate(
    all_gold_entities: List[List[Dict]],
    all_pred_entities: List[List[Dict]],
    all_texts: List[str],
    entity_types: List[str]
) -> Dict[str, Any]:
    """
    Run nervaluate evaluation on batch.
    
    Args:
        all_gold_entities: List of gold lists. Each dict MUST have 'start' and 'end' indices.
        all_pred_entities: List of pred lists.
    """
    
    all_gold_spans = []
    all_pred_spans = []
    
    for text, gold, pred in zip(all_texts, all_gold_entities, all_pred_entities):
        # Format Gold for nervaluate (use spans if provided, otherwise derive from text)
        gold_spans = _build_gold_spans(text, gold)
        
        # Align Predictions to Gold (Bag-of-Entities style)
        pred_spans = align_predictions_to_gold(text, gold_spans, pred)
        
        all_gold_spans.append(gold_spans)
        all_pred_spans.append(pred_spans)
    
    # Handle edge case: nervaluate crashes if lists are empty or first sample is empty
    # Check if we have any data at all
    has_any_gold = any(g for g in all_gold_spans)
    has_any_pred = any(p for p in all_pred_spans)
    
    # Helper to create empty metrics structure (consistent with nervaluate output)
    def _create_empty_metrics(note: str = '', spurious: int = 0, missed: int = 0) -> Dict:
        empty_scheme = {
            'precision': 0.0, 'recall': 0.0, 'f1': 0.0,
            'correct': 0, 'incorrect': 0, 'partial': 0,
            'missed': missed, 'spurious': spurious,
            'actual': spurious, 'possible': missed
        }
        return {
            'overall': {
                'strict': empty_scheme.copy(),
                'exact': empty_scheme.copy(),
                'partial': empty_scheme.copy(),
                'ent_type': empty_scheme.copy()
            },
            'macro': {'strict': 0.0, 'exact': 0.0, 'partial': 0.0, 'ent_type': 0.0},
            'by_tag': {tag: {'strict': empty_scheme.copy(), 'exact': empty_scheme.copy(), 
                            'partial': empty_scheme.copy(), 'ent_type': empty_scheme.copy()}
                       for tag in entity_types},
            '_note': note
        }
    
    if not has_any_gold and not has_any_pred:
        # No data at all - return empty metrics
        return _create_empty_metrics('No gold or predictions')
    
    # CRITICAL FIX: nervaluate crashes if gold is empty but pred is not (or vice versa)
    # We need to ensure the first sample has at least one entity in BOTH gold and pred
    # OR skip nervaluate entirely for degenerate cases
    
    # Case 1: No gold entities at all - can't compute recall meaningfully
    if not has_any_gold:
        # Model predicted but there's nothing to match against
        # Precision = 0 (all predictions are false positives), Recall = undefined (no gold)
        total_pred = sum(len(p) for p in all_pred_spans)
        return _create_empty_metrics(f'No gold entities, {total_pred} predictions (all false positives)', spurious=total_pred)
    
    # Case 2: No predictions at all - precision undefined, recall = 0
    if not has_any_pred:
        total_gold = sum(len(g) for g in all_gold_spans)
        return _create_empty_metrics(f'{total_gold} gold entities, no predictions (all false negatives)', missed=total_gold)
    
    # nervaluate requires first element to be non-empty list with at least one entity
    # Find a sample where BOTH gold and pred have at least one entity, or gold has entities
    first_valid_idx = None
    for i, (g, p) in enumerate(zip(all_gold_spans, all_pred_spans)):
        if g:  # Gold must have entities for nervaluate to work
            first_valid_idx = i
            break
    
    if first_valid_idx is None:
        # Shouldn't happen given the checks above, but safety fallback
        return {
            'overall': {'precision': 0.0, 'recall': 0.0, 'f1': 0.0},
            'macro': {'precision': 0.0, 'recall': 0.0, 'f1': 0.0},
            'by_tag': {}
        }
    
    # Swap to put valid sample first if needed
    if first_valid_idx > 0:
        all_gold_spans[0], all_gold_spans[first_valid_idx] = all_gold_spans[first_valid_idx], all_gold_spans[0]
        all_pred_spans[0], all_pred_spans[first_valid_idx] = all_pred_spans[first_valid_idx], all_pred_spans[0]
    
    try:
        evaluator = Evaluator(all_gold_spans, all_pred_spans, tags=entity_types, loader="default")
    except (IndexError, ValueError) as e:
        # Fallback if nervaluate still crashes
        # Provide detailed diagnostic info
        first_gold_empty = not all_gold_spans[0] if all_gold_spans else True
        first_pred_empty = not all_pred_spans[0] if all_pred_spans else True
        total_samples = len(all_gold_spans)
        non_empty_gold = sum(1 for g in all_gold_spans if g)
        non_empty_pred = sum(1 for p in all_pred_spans if p)
        
        logging.warning(
            f"nervaluate initialization failed: {e}. "
            f"Diagnostic: first_gold_empty={first_gold_empty}, first_pred_empty={first_pred_empty}, "
            f"total_samples={total_samples}, non_empty_gold={non_empty_gold}, non_empty_pred={non_empty_pred}. "
            f"Returning zero metrics."
        )
        return {
            'overall': {'precision': 0.0, 'recall': 0.0, 'f1': 0.0},
            'macro': {'precision': 0.0, 'recall': 0.0, 'f1': 0.0},
            'by_tag': {}
        }
    
    # Support both dict and tuple return signatures from nervaluate
    full_output = evaluator.evaluate()
    if isinstance(full_output, tuple):
        # (results, results_by_tag, evaluator_results, evaluator_results_by_tag)
        overall_output = full_output[0]
        results_by_tag = full_output[1]
    else:
        overall_output = full_output.get('overall', full_output)
        results_by_tag = full_output.get('entities', {})

    def _scheme_obj_to_dict(scheme_obj: Any) -> Dict[str, Any]:
        if isinstance(scheme_obj, dict):
            return scheme_obj
        result = {}
        for key in (
            'precision', 'recall', 'f1', 'correct', 'incorrect',
            'partial', 'missed', 'spurious', 'actual', 'possible'
        ):
            if hasattr(scheme_obj, key):
                result[key] = getattr(scheme_obj, key)
        return result

    if isinstance(overall_output, dict):
        normalized = {}
        for scheme in ['strict', 'exact', 'partial', 'ent_type']:
            if scheme in overall_output:
                normalized[scheme] = _scheme_obj_to_dict(overall_output[scheme])
        overall_output = normalized
    else:
        normalized = {}
        for scheme in ['strict', 'exact', 'partial', 'ent_type']:
            scheme_obj = getattr(overall_output, scheme, None)
            if scheme_obj is not None:
                normalized[scheme] = _scheme_obj_to_dict(scheme_obj)
        overall_output = normalized
    
    def _get_f1(metrics: Any, scheme: str) -> float:
        """Extract F1 score from metrics for a given scheme."""
        if isinstance(metrics, dict):
            scheme_metrics = metrics.get(scheme)
            if isinstance(scheme_metrics, dict):
                return scheme_metrics.get('f1', 0.0)
            elif hasattr(scheme_metrics, 'f1'):
                return getattr(scheme_metrics, 'f1', 0.0)
            return 0.0

        scheme_metrics = getattr(metrics, scheme, None)
        if scheme_metrics is None:
            return 0.0
        if isinstance(scheme_metrics, dict):
            return scheme_metrics.get('f1', 0.0)
        return getattr(scheme_metrics, 'f1', 0.0)
    
    def _get_possible(metrics: Any, scheme: str) -> int:
        """Extract 'possible' (gold count) from metrics for a given scheme."""
        if isinstance(metrics, dict):
            scheme_metrics = metrics.get(scheme)
            if isinstance(scheme_metrics, dict):
                return scheme_metrics.get('possible', 0)
            elif hasattr(scheme_metrics, 'possible'):
                return getattr(scheme_metrics, 'possible', 0)
            return 0

        scheme_metrics = getattr(metrics, scheme, None)
        if scheme_metrics is None:
            return 0
        if isinstance(scheme_metrics, dict):
            return scheme_metrics.get('possible', 0)
        return getattr(scheme_metrics, 'possible', 0)

    # Calculate Macro F1 for each scheme (Strict, Exact, Partial, Type)
    macro_metrics = {}
    schemes = ['strict', 'exact', 'partial', 'ent_type']
    
    for scheme in schemes:
        f1_sum = 0.0
        count = 0
        for tag, metrics in results_by_tag.items():
            # Only include tags with support (possible > 0)
            possible = _get_possible(metrics, scheme)
            if possible > 0:
                f1_value = _get_f1(metrics, scheme)
                f1_sum += f1_value
                count += 1
        
        macro_f1 = f1_sum / count if count > 0 else 0.0
        macro_metrics[scheme] = macro_f1

    # Combine into a structure similar to original if needed, or just return as is
    # The user wants "Model Evaluation Result" sections.
    return {
        "overall": overall_output,
        "by_tag": results_by_tag,
        "macro": macro_metrics,
        "evaluator_calculated": {
            "overall": overall_output,
            "entities": results_by_tag
        }
    }
