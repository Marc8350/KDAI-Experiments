import re
import sys
from pathlib import Path
from typing import Dict

CODEIE_ROOT = Path(__file__).resolve().parents[1]
if str(CODEIE_ROOT) not in sys.path:
    sys.path.append(str(CODEIE_ROOT))

from src.evaluation_nervaluate import evaluate_with_nervaluate
from run_codeie_experiments import parse_code_style_output


def parse_entity_string(entity_str: str) -> Dict[str, str]:
    match = re.match(r"^([\w-]+)\(span='(.*)'\)$", entity_str)
    if match:
        return {'type': match.group(1), 'text': match.group(2)}
    raise ValueError(f"Unrecognized entity string format: {entity_str}")


def assert_close(name: str, actual: float, expected: float, tol: float = 1e-6) -> None:
    if abs(actual - expected) > tol:
        raise AssertionError(f"{name} mismatch: expected {expected}, got {actual}")


def test_nervaluate_raw_input_example() -> None:
    text = (
        "Grill Room at the Taft Hotel in New York featured "
        "George Hall and His Hotel Taft Orchestra."
    )

    gold_strings = [
        "building(span='Grill Room')",
        "building(span='Taft Hotel')",
        "location(span='New York')",
        "organization(span='George Hall and His Hotel Taft Orchestra')"
    ]

    generated_raw = (
        "entity_list.append({\"text\": \"Grill Room\", \"type\": \"building\"})\n"
        "entity_list.append({\"text\": \"Taft Hotel\", \"type\": \"building\"})\n"
        "entity_list.append({\"text\": \"George Hall and His Hotel Taft Orchestra\", \"type\": \"other\"})"
    )

    entity_types = ["building", "location", "organization", "other"]

    gold_entities = [parse_entity_string(s) for s in gold_strings]
    parsed_from_raw = parse_code_style_output(
        output=generated_raw,
        entity_types=entity_types
    )

    print("Parsed gold entities:")
    print(gold_entities)
    print("Parsed prediction entities (from generated_raw):")
    print(parsed_from_raw)

    results = evaluate_with_nervaluate(
        all_gold_entities=[gold_entities],
        all_pred_entities=[parsed_from_raw],
        all_texts=[text],
        entity_types=entity_types
    )

    overall = results['overall']

    # Expected metrics (strict):
    # correct=2 (Grill Room, Taft Hotel)
    # incorrect=1 (George Hall... wrong type)
    # missed=1 (New York)
    # precision=2/3, recall=2/4, f1=0.571428...
    assert_close("strict.precision", overall['strict']['precision'], 2/3)
    assert_close("strict.recall", overall['strict']['recall'], 2/4)
    assert_close("strict.f1", overall['strict']['f1'], 2 * (2/3) * (2/4) / ((2/3) + (2/4)))

    # Expected metrics (exact): type ignored, exact span match => 3 correct
    assert_close("exact.precision", overall['exact']['precision'], 1.0)
    assert_close("exact.recall", overall['exact']['recall'], 3/4)
    assert_close("exact.f1", overall['exact']['f1'], 2 * 1.0 * (3/4) / (1.0 + (3/4)))

    # Expected metrics (partial): same as exact in this case
    assert_close("partial.precision", overall['partial']['precision'], 1.0)
    assert_close("partial.recall", overall['partial']['recall'], 3/4)
    assert_close("partial.f1", overall['partial']['f1'], 2 * 1.0 * (3/4) / (1.0 + (3/4)))

    # Expected metrics (ent_type): same as strict (type-only)
    assert_close("ent_type.precision", overall['ent_type']['precision'], 2/3)
    assert_close("ent_type.recall", overall['ent_type']['recall'], 2/4)
    assert_close("ent_type.f1", overall['ent_type']['f1'], 2 * (2/3) * (2/4) / ((2/3) + (2/4)))

    print("Nervaluate metrics:")
    print({
        "strict": overall['strict'],
        "exact": overall['exact'],
        "partial": overall['partial'],
        "ent_type": overall['ent_type']
    })
    print("Per-entity-type metrics:")
    print(results.get("by_tag", {}))
    print("Full nervaluate output object:")
    print(results)


if __name__ == "__main__":
    test_nervaluate_raw_input_example()
    print("OK")
