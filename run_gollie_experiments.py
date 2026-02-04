import os
import sys

# Get the absolute path of the project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Add GoLLIE subfolder to path for its internal 'src' imports
GOLLIE_PATH = os.path.join(PROJECT_ROOT, "GoLLIE")
if GOLLIE_PATH not in sys.path:
    sys.path.append(GOLLIE_PATH)
import json
import logging
import re
import inspect
import black
from datetime import datetime
from tqdm import tqdm
from typing import Dict, List, Type, Any
from datasets import load_from_disk
from src.model.load_model import load_model
from src.tasks.utils_typing import Entity, AnnotationList
from src.tasks.utils_scorer import SpanScorer

from annotation_guidelines import (
    guidelines_coarse_gollie,
    guidelines_coarse_gollie_detailed_v1,
    guidelines_coarse_gollie_detailed_v2,
    guidelines_coarse_gollie_detailed_v3,
    guidelines_coarse_gollie_v1,
    guidelines_coarse_gollie_v2,
    guidelines_coarse_gollie_v3,
    guidelines_fine_gollie,
    guidelines_fine_gollie_detailed_v1,
    guidelines_fine_gollie_detailed_v2,
    guidelines_fine_gollie_detailed_v3,
    guidelines_fine_gollie_v1,
    guidelines_fine_gollie_v2,
    guidelines_fine_gollie_v3
)

logging.basicConfig(level=logging.INFO)

guideline_modules = [
    guidelines_coarse_gollie,
    guidelines_coarse_gollie_detailed_v1,
    guidelines_coarse_gollie_detailed_v2,
    guidelines_coarse_gollie_detailed_v3,
    guidelines_coarse_gollie_v1,
    guidelines_coarse_gollie_v2,
    guidelines_coarse_gollie_v3,
    guidelines_fine_gollie,
    guidelines_fine_gollie_detailed_v1,
    guidelines_fine_gollie_detailed_v2,
    guidelines_fine_gollie_detailed_v3,
    guidelines_fine_gollie_v1,
    guidelines_fine_gollie_v2,
    guidelines_fine_gollie_v3
]

# Configurable parameters
MODEL_LOAD_PARAMS = {
    "inference": True,
    "model_weights_name_or_path": "HiTZ/GoLLIE-7B",
    "quantization": None,
    "use_lora": False,
    "force_auto_device_map": True,
    "use_flash_attention": True,
    "torch_dtype": "bfloat16"
}

GENERATE_PARAMS = {
    "max_new_tokens": 128,
    "do_sample": False,
    "min_new_tokens": 0,
    "num_beams": 1,
    "num_return_sequences": 1,
}

class MyEntityScorer(SpanScorer):
    """Compute the F1 score for Named Entity Recognition Tasks"""
    
    # We will set valid_types dynamically per module
    valid_types: List[Type] = []

    def __call__(self, reference: List[List[Entity]], predictions: List[List[Entity]]) -> Dict[str, Any]:
        output = super().__call__(reference, predictions)
        return {"entities": output["spans"]}

def label_to_classname(label):
    if label == "O":
        return None
    # Split by both - and / and capitalize each part to match class names
    parts = re.split(r'[-/]', label)
    return "".join(p.capitalize() for p in parts)

def run_experiment():
    """
    Iterates over guideline modules and processes sentences from few-nerd_test.
    """
    # Create results directory
    RESULTS_DIR = "GOLLIE-results"
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Load dataset
    ds = load_from_disk("./few-nerd_test")
    coarse_names = ds.features["ner_tags"].feature.names
    fine_names = ds.features["fine_ner_tags"].feature.names

    # Load model
    logging.info(f"Loading model with params: {MODEL_LOAD_PARAMS}")
    model, tokenizer = load_model(**MODEL_LOAD_PARAMS)

    # Read template
    from jinja2 import Template
    template_path = os.path.join(GOLLIE_PATH, "templates", "prompt.txt")
    with open(template_path, "rt") as f:
        template = Template(f.read())

    for module in tqdm(guideline_modules, desc="Processing modules"):
        module_name = module.__name__
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = os.path.join(RESULTS_DIR, f"{module_name}_{timestamp}.json")
        
        logging.info(f"Processing module: {module_name}")
        
        is_coarse = "coarse" in module_name
        tag_key = "ner_tags" if is_coarse else "fine_ner_tags"
        names_ref = coarse_names if is_coarse else fine_names
        
        scorer = MyEntityScorer()
        scorer.valid_types = module.ENTITY_DEFINITIONS
        
        gold_per_module = []
        predictions_per_module = []
        sentence_results = []

        # We might want to limit sentences for testing, but user said "iterate over the sentences"
        for i, sentence in enumerate(tqdm(ds, desc=f"Processing {module_name}", leave=False)):
            # 1. Prepare sentence text
            tokens = sentence["tokens"]
            text = " ".join(tokens)
            
            # 2. Extract Gold Objects
            tags = sentence[tag_key]
            gold = []
            for token, tag_id in zip(tokens, tags):
                label = names_ref[tag_id]
                class_name = label_to_classname(label)
                if class_name:
                    entity_class = getattr(module, class_name, None)
                    if entity_class:
                        gold.append(entity_class(span=token))
            
            # 3. Format Prompt
            formatted_text = template.render(
                guidelines=[inspect.getsource(definition) for definition in module.ENTITY_DEFINITIONS],
                text=text,
                annotations=gold,
                gold=gold
            )
            
            # Clean up with black
            try:
                formatted_text = black.format_str(formatted_text, mode=black.Mode())
            except Exception as e:
                logging.error(f"Black formatting failed: {e}")

            # Prepare prompt by stripping existing result
            prompt, _ = formatted_text.split("result =")
            prompt = prompt + "result ="

            # 4. Inference
            model_input = tokenizer(prompt, add_special_tokens=True, return_tensors="pt")
            # Remove EOS token
            model_input["input_ids"] = model_input["input_ids"][:, :-1]
            model_input["attention_mask"] = model_input["attention_mask"][:, :-1]
            
            model_output = model.generate(
                **model_input.to(model.device),
                **GENERATE_PARAMS
            )
            
            # 5. Parse output
            decoded_output = tokenizer.decode(model_output[0], skip_special_tokens=True)
            result_str = decoded_output.split("result =")[-1]
            
            try:
                # AnnotationList.from_output expects a string that looks like [Entity(span='...'), ...]
                # and a task_module name (the package where classes are defined)
                prediction = AnnotationList.from_output(
                    result_str,
                    task_module=module_name
                )
            except Exception as e:
                logging.error(f"Parsing failed for sentence {i}: {e}")
                prediction = []

            # 6. Score individual sentence
            sentence_score = scorer(reference=[gold], predictions=[prediction])
            
            # Store for overall
            gold_per_module.append(gold)
            predictions_per_module.append(prediction)
            
            # Log current sentence
            sentence_data = {
                "index": i,
                "timestamp": datetime.now().isoformat(),
                "text": text,
                "gold": [str(g) for g in gold],
                "prediction": [str(p) for p in prediction],
                "score": sentence_score
            }
            sentence_results.append(sentence_data)
            
            # 7. Intermediate Saving (Avoid data loss on long runs)
            current_overall_score = scorer(reference=gold_per_module, predictions=predictions_per_module)
            
            final_results = {
                "module": module_name,
                "timestamp": timestamp,
                "model_load_params": MODEL_LOAD_PARAMS,
                "generate_params": GENERATE_PARAMS,
                "overall_score": current_overall_score,
                "processed_count": len(sentence_results),
                "sentences": sentence_results
            }
            
            with open(log_filename, "w") as f:
                json.dump(final_results, f, indent=4)
            
            if i % 10 == 0:
                logging.info(f"[{module_name}] Progress: {i} sentences saved to {log_filename}")

        logging.info(f"Finished module {module_name}. Full results available at {log_filename}")

if __name__ == "__main__":
    run_experiment()