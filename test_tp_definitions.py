#!/usr/bin/env python3
"""
Detailed Analysis: What is a True Positive (TP)?

This script demonstrates the EXACT definition of True Positive (TP) used by:
1. nervaluate library (strict mode)
2. GoLLIE SpanScorer framework
"""

import sys
import os
from typing import List, Dict, Type
from nervaluate import Evaluator

# Add GoLLIE to path - but we'll define our own minimal classes to avoid import issues
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'GoLLIE'))

# Define minimal Entity class matching GoLLIE's implementation
from dataclasses import dataclass as org_dataclass

def dataclass(cls=None, /, *, init=True, repr=False, eq=False, order=False, unsafe_hash=False, frozen=False):
    return org_dataclass(cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash, frozen=frozen)

@dataclass
class Entity:
    """A general class to represent entities (matching GoLLIE implementation)."""
    span: str

    def __post_init__(self) -> None:
        self._allow_partial_match: bool = False

    def __eq__(self, other) -> bool:
        """This is the EXACT equality check from GoLLIE's utils_typing.py"""
        self_span = self.span.lower().strip()
        other_span = other.span.lower().strip()
        if self._allow_partial_match:
            return type(self) == type(other) and (self.span in other_span or other_span in self.span)
        return type(self) == type(other) and self_span == other_span


# Minimal SpanScorer implementation matching GoLLIE's logic
class SpanScorer:
    """Minimal SpanScorer implementation matching GoLLIE's src/tasks/utils_scorer.py"""
    
    valid_types: List[Type] = []
    
    def __call__(self, reference: List[List[Entity]], predictions: List[List[Entity]]) -> Dict[str, Dict]:
        """This is the EXACT logic from GoLLIE's SpanScorer.__call__"""
        tp = total_pos = total_pre = 0
        
        for ref, pre in zip(reference, predictions):
            # Filter valid types
            ref = [e for e in ref if any(isinstance(e, t) for t in self.valid_types)]
            pre = [e for e in pre if any(isinstance(e, t) for t in self.valid_types)]
            
            ref2 = ref.copy()
            
            total_pos += len(ref)
            total_pre += len(pre)
            
            # KEY LOGIC: Check if entity in ref using __eq__
            for entity in pre:
                if entity in ref:  # This uses Entity.__eq__!
                    tp += 1
                    ref.pop(ref.index(entity))
        
        precision = tp / total_pre if total_pre > 0.0 else 0.0
        recall = tp / total_pos if total_pos > 0.0 else 0.0
        f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0.0 else 0.0
        
        return {
            "entities": {
                "tp": tp,
                "total_pos": total_pos,
                "total_pre": total_pre,
                "precision": precision,
                "recall": recall,
                "f1-score": f1_score
            }
        }


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


print_header("TRUE POSITIVE DEFINITIONS IN NER EVALUATION")

# ============================================================================
# 1. GOLLIE SPANSCORER ANALYSIS
# ============================================================================

print_header("1. GoLLIE SpanScorer - What is a True Positive?")

print("📖 Source Code Analysis:")
print("   Location: GoLLIE/src/tasks/utils_scorer.py")
print("   Key Logic:")
print("""
   for entity in predictions:
       if entity in reference:
           tp += 1
           reference.pop(reference.index(entity))
""")

print("\n📖 Entity Equality Check (utils_typing.py):")
print("""
   def __eq__(self: Entity, other: Entity) -> bool:
       self_span = self.span.lower().strip()
       other_span = other.span.lower().strip()
       return type(self) == type(other) and self_span == other_span
""")

print("\n✅ True Positive Definition for GoLLIE SpanScorer:")
print("   A prediction is a TP if:")
print("   1. type(prediction) == type(gold)  ← Entity CLASS must match")
print("   2. prediction.span.lower().strip() == gold.span.lower().strip()")
print("      ← Text span must match (case-insensitive, whitespace-stripped)")
print("\n   Both conditions MUST be satisfied simultaneously!")

print("\n" + "-" * 80)
print("🧪 PRACTICAL TEST WITH GOLLIE:")
print("-" * 80)

# Define entity classes for GoLLIE
@dataclass
class Organization(Entity):
    """An organization entity."""
    span: str

@dataclass
class Person(Entity):
    """A person entity."""
    span: str

@dataclass  
class Location(Entity):
    """A location entity."""
    span: str

# Test cases
print("\nTest Case 1: EXACT MATCH (Type + Span)")
gold1 = Organization(span="Apple Inc.")
pred1 = Organization(span="Apple Inc.")
print(f"Gold:       {type(gold1).__name__}(span='{gold1.span}')")
print(f"Prediction: {type(pred1).__name__}(span='{pred1.span}')")
print(f"Result:     {pred1 == gold1} ← This is a TRUE POSITIVE ✅")

print("\nTest Case 2: SAME SPAN, DIFFERENT TYPE")
gold2 = Organization(span="Apple Inc.")
pred2 = Location(span="Apple Inc.")  # Wrong type!
print(f"Gold:       {type(gold2).__name__}(span='{gold2.span}')")
print(f"Prediction: {type(pred2).__name__}(span='{pred2.span}')")
print(f"Result:     {pred2 == gold2} ← This is NOT a TP ❌")
print("            (Wrong entity type → False Positive + False Negative)")

print("\nTest Case 3: SAME TYPE, DIFFERENT SPAN")
gold3 = Organization(span="Apple Inc.")
pred3 = Organization(span="Apple")  # Partial span!
print(f"Gold:       {type(gold3).__name__}(span='{gold3.span}')")
print(f"Prediction: {type(pred3).__name__}(span='{pred3.span}')")
print(f"Result:     {pred3 == gold3} ← This is NOT a TP ❌")
print("            (Different span → False Positive + False Negative)")

print("\nTest Case 4: CASE INSENSITIVE MATCH")
gold4 = Organization(span="Apple Inc.")
pred4 = Organization(span="APPLE INC.")  # Different case
print(f"Gold:       {type(gold4).__name__}(span='{gold4.span}')")
print(f"Prediction: {type(pred4).__name__}(span='{pred4.span}')")
print(f"Result:     {pred4 == gold4} ← This IS a TRUE POSITIVE ✅")
print("            (GoLLIE is case-insensitive!)")

print("\nTest Case 5: WHITESPACE HANDLING")
gold5 = Organization(span="Apple Inc.")
pred5 = Organization(span="  Apple Inc.  ")  # Extra whitespace
print(f"Gold:       {type(gold5).__name__}(span='{gold5.span}')")
print(f"Prediction: {type(pred5).__name__}(span='{pred5.span}')")
print(f"Result:     {pred5 == gold5} ← This IS a TRUE POSITIVE ✅")
print("            (GoLLIE strips whitespace!)")

# Run actual GoLLIE evaluation
print("\n" + "-" * 80)
print("🔬 ACTUAL GOLLIE EVALUATION RESULTS:")
print("-" * 80)

ENTITY_DEFINITIONS = [Organization, Person, Location]

class TestScorer(SpanScorer):
    valid_types: List[Type] = ENTITY_DEFINITIONS
    
    def __call__(self, reference: List[Entity], predictions: List[Entity]) -> Dict[str, Dict[str, float]]:
        output = super().__call__(reference, predictions)
        return {"entities": output["spans"]}

scorer = TestScorer()

# Test evaluation
gold_list = [
    Organization(span="Apple Inc."),
    Person(span="Steve Jobs"),
    Location(span="California")
]

pred_list = [
    Organization(span="APPLE INC."),  # Case different → Still TP
    Organization(span="Steve Jobs"),  # Wrong type → Not TP
    Location(span="California")       # Correct → TP
]

result = scorer(reference=[gold_list], predictions=[pred_list])
print(f"\nGold Entities: {len(gold_list)}")
print(f"Pred Entities: {len(pred_list)}")
print(f"\nTrue Positives:  {result['entities']['tp']}")
print(f"False Positives: {result['entities']['total_pre'] - result['entities']['tp']}")
print(f"False Negatives: {result['entities']['total_pos'] - result['entities']['tp']}")
print(f"\nPrecision: {result['entities']['precision']:.2%}")
print(f"Recall:    {result['entities']['recall']:.2%}")
print(f"F1-Score:  {result['entities']['f1-score']:.2%}")

print("\n💡 Explanation of results:")
print("   - 'APPLE INC.' (case different) → TP ✅ (GoLLIE is case-insensitive)")
print("   - 'Steve Jobs' as Organization → NOT TP ❌ (wrong type → FP + FN)")
print("   - 'California' as Location → TP ✅ (exact match)")
print(f"\n   Therefore: TP=2, FP=1, FN=1")

# ============================================================================
# 2. NERVALUATE ANALYSIS
# ============================================================================

print_header("2. nervaluate - What is a True Positive? (Strict Mode)")

print("📖 nervaluate Library:")
print("   Source: https://pypi.org/project/nervaluate/")
print("   Documentation: https://github.com/MantisAI/nervaluate")

print("\n✅ True Positive Definition for nervaluate (STRICT mode):")
print("   A prediction is a TP if:")
print("   1. prediction['label'] == gold['label']  ← Entity TYPE must match")
print("   2. prediction['start'] == gold['start']  ← Start position must match")
print("   3. prediction['end'] == gold['end']      ← End position must match")
print("\n   All THREE conditions MUST be satisfied!")

print("\n📌 Key Differences from GoLLIE:")
print("   • nervaluate uses SPAN POSITIONS (start/end indices)")
print("   • GoLLIE uses TEXT STRINGS (span text)")
print("   • nervaluate is CASE-SENSITIVE (via position matching)")
print("   • GoLLIE is CASE-INSENSITIVE")

print("\n" + "-" * 80)
print("🧪 PRACTICAL TEST WITH NERVALUATE:")
print("-" * 80)

text = "Apple Inc. was founded by Steve Jobs in California."

print(f'\nText: "{text}"')
print("Character positions:")
print("      0123456789012345678901234567890123456789012345678901")
print("                1         2         3         4         5")

# Test case 1: Perfect match
print("\n" + "─" * 80)
print("Test Case 1: EXACT MATCH (Type + Start + End)")
gold_spans = [[
    {'label': 'organization', 'start': 0, 'end': 10},  # "Apple Inc."
    {'label': 'person', 'start': 26, 'end': 37},       # "Steve Jobs"
]]
pred_spans = [[
    {'label': 'organization', 'start': 0, 'end': 10},  # "Apple Inc." - EXACT
    {'label': 'person', 'start': 26, 'end': 37},       # "Steve Jobs" - EXACT
]]

evaluator = Evaluator(gold_spans, pred_spans, tags=['organization', 'person', 'location'])
results = evaluator.evaluate()
strict = results['overall']['strict']

print(f"Gold: organization at [0:10]  → '{text[0:10]}'")
print(f"Pred: organization at [0:10]  → '{text[0:10]}'")
print(f"✅ MATCH (TP)")
print(f"\nGold: person at [26:37]  → '{text[26:37]}'")
print(f"Pred: person at [26:37]  → '{text[26:37]}'")
print(f"✅ MATCH (TP)")
print(f"\nResults: TP={strict.correct}, FP={strict.spurious}, FN={strict.missed}")

# Test case 2: Wrong type
print("\n" + "─" * 80)
print("Test Case 2: SAME POSITION, WRONG TYPE")
gold_spans = [[
    {'label': 'person', 'start': 26, 'end': 37},  # "Steve Jobs" as person
]]
pred_spans = [[
    {'label': 'organization', 'start': 26, 'end': 37},  # "Steve Jobs" as organization
]]

evaluator = Evaluator(gold_spans, pred_spans, tags=['organization', 'person'])
results = evaluator.evaluate()
strict = results['overall']['strict']

print(f"Gold: person at [26:37]        → '{text[26:37]}'")
print(f"Pred: organization at [26:37]  → '{text[26:37]}'")
print(f"❌ NO MATCH - Wrong type!")
print(f"   This counts as 'incorrect' in nervaluate")
print(f"\nResults: TP={strict.correct}, Incorrect={strict.incorrect}")
print("         (Incorrect = right span, wrong type)")

# Test case 3: Wrong boundaries
print("\n" + "─" * 80)
print("Test Case 3: SAME TYPE, WRONG BOUNDARIES")
gold_spans = [[
    {'label': 'organization', 'start': 0, 'end': 10},  # "Apple Inc."
]]
pred_spans = [[
    {'label': 'organization', 'start': 0, 'end': 5},   # "Apple" only
]]

evaluator = Evaluator(gold_spans, pred_spans, tags=['organization'])
results = evaluator.evaluate()
strict = results['overall']['strict']

print(f"Gold: organization at [0:10]  → '{text[0:10]}'")
print(f"Pred: organization at [0:5]   → '{text[0:5]}'")
print(f"❌ NO MATCH - Wrong boundaries!")
print(f"   This counts as 'partial' in some modes, but NOT a TP in strict mode")
print(f"\nResults: TP={strict.correct}, Partial={strict.partial}")

# Test case 4: Partial overlap
print("\n" + "─" * 80)
print("Test Case 4: OVERLAPPING BUT NOT EXACT")
gold_spans = [[
    {'label': 'organization', 'start': 0, 'end': 10},  # "Apple Inc."
]]
pred_spans = [[
    {'label': 'organization', 'start': 6, 'end': 10},  # "Inc." only
]]

evaluator = Evaluator(gold_spans, pred_spans, tags=['organization'])
results = evaluator.evaluate()
strict = results['overall']['strict']
partial = results['overall']['partial']

print(f"Gold: organization at [0:10]   → '{text[0:10]}'")
print(f"Pred: organization at [6:10]   → '{text[6:10]}'")
print(f"❌ NO MATCH in strict mode!")
print(f"   Strict:  TP={strict.correct} (requires exact boundaries)")
print(f"   Partial: TP={partial.correct} (accepts overlaps)")

# ============================================================================
# SUMMARY COMPARISON
# ============================================================================

print_header("SUMMARY: TRUE POSITIVE DEFINITIONS COMPARED")

print("""
┌─────────────────────┬──────────────────────────┬──────────────────────────┐
│ Criterion           │ GoLLIE SpanScorer        │ nervaluate (strict)      │
├─────────────────────┼──────────────────────────┼──────────────────────────┤
│ Type/Label Match    │ ✅ Required              │ ✅ Required              │
│                     │ type(pred) == type(gold) │ pred['label'] == gold[…] │
├─────────────────────┼──────────────────────────┼──────────────────────────┤
│ Text/Span Match     │ ✅ Required              │ ✅ Required              │
│                     │ span text (string)       │ start/end positions      │
├─────────────────────┼──────────────────────────┼──────────────────────────┤
│ Case Sensitivity    │ ❌ Case-INSENSITIVE      │ ⚠️  Position-based       │
│                     │ "Apple" == "APPLE"       │ (depends on text)        │
├─────────────────────┼──────────────────────────┼──────────────────────────┤
│ Whitespace          │ ❌ Strips whitespace     │ ⚠️  Position-based       │
│                     │ " Apple " == "Apple"     │ (depends on text)        │
├─────────────────────┼──────────────────────────┼──────────────────────────┤
│ Partial Match       │ ❌ NO (in strict mode)   │ ❌ NO (in strict mode)   │
│                     │ "Apple" ≠ "Apple Inc."   │ [0:5] ≠ [0:10]          │
├─────────────────────┼──────────────────────────┼──────────────────────────┤
│ Wrong Type          │ ❌ NOT TP                │ ❌ NOT TP                │
│                     │ (FP + FN)                │ (counts as 'incorrect')  │
└─────────────────────┴──────────────────────────┴──────────────────────────┘
""")

print("\n🎯 KEY TAKEAWAY:")
print("""
Both frameworks require EXACT matching in strict mode:
  1. Entity TYPE/LABEL must match exactly
  2. Entity SPAN must match exactly (text or position)

A prediction is only a TP when BOTH conditions are satisfied.
Any deviation → NOT a TP (results in FP + FN instead).
""")

print("\n📝 FOR YOUR THESIS:")
print("""
Under strict evaluation mode, a True Positive occurs when a predicted entity
matches a gold standard entity in BOTH entity type (class/label) and exact
span boundaries. In the GoLLIE SpanScorer framework, this is implemented as
a Python equality check that compares entity class types and normalized span
text (case-insensitive, whitespace-stripped). In nervaluate's strict mode,
the comparison requires exact matches of the entity label and character-level
start and end positions within the text. Both frameworks reject partial matches:
for example, predicting "Apple" when the gold standard is "Apple Inc." results
in a false positive (for the incorrect prediction) and a false negative (for
the missed correct entity), not a true positive. Similarly, predicting the
correct text span with an incorrect entity type (e.g., labeling "Steve Jobs"
as an organization instead of a person) also fails to produce a true positive,
as both the type and span must be correct simultaneously.
""")

print("\n" + "=" * 80)
print("✅ Analysis Complete!")
print("=" * 80 + "\n")
