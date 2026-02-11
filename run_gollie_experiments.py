
import os
import sys
import json
import logging
import re
import inspect
import black
from datetime import datetime
from typing import Dict, List, Type, Any
from datasets import load_from_disk
from concurrent.futures import ProcessPoolExecutor

# Get the absolute path of the project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Add GoLLIE subfolder to path for its internal 'src' imports
GOLLIE_PATH = os.path.join(PROJECT_ROOT, "GoLLIE")
if GOLLIE_PATH not in sys.path:
    sys.path.append(GOLLIE_PATH)

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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Map string names to module objects for easy lookup
MODULE_MAP = {
    m.__name__: m for m in [
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
}

# Configurable parameters
MODEL_LOAD_PARAMS = {
    "inference": True,
    "model_weights_name_or_path": "HiTZ/GoLLIE-7B",
    "quantization": None,
    "use_lora": False,
    "force_auto_device_map": True,
    "use_flash_attention": False,
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

def process_module(module_name: str, max_examples: int = 3765) -> str:
    """
    Process a single guideline module.
    Runs in a separate process.
    """
    try:
        # Re-import or get module from map
        module = MODULE_MAP.get(module_name)
        if not module:
            return f"Error: Module {module_name} not found"

        RESULTS_DIR = "GOLLIE-results"
        os.makedirs(RESULTS_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = os.path.join(RESULTS_DIR, f"{module_name}_{timestamp}.json")
        
        logging.info(f"[{module_name}] Starting processing...")

        # Load dataset locally in worker
        ds_path = os.path.join(PROJECT_ROOT, "few-nerd_test")
        ds = load_from_disk(ds_path)
        coarse_names = ds.features["ner_tags"].feature.names
        fine_names = ds.features["fine_ner_tags"].feature.names

        # Load model locally in worker
        logging.info(f"[{module_name}] Loading model...")
        model, tokenizer = load_model(**MODEL_LOAD_PARAMS)
        
        # Determine Jinja template
        from jinja2 import Template
        template_path = os.path.join(GOLLIE_PATH, "templates", "prompt.txt")
        with open(template_path, "rt") as f:
            template = Template(f.read())

        is_coarse = "coarse" in module_name
        tag_key = "ner_tags" if is_coarse else "fine_ner_tags"
        names_ref = coarse_names if is_coarse else fine_names
        
        scorer = MyEntityScorer()
        scorer.valid_types = module.ENTITY_DEFINITIONS
        
        gold_per_module = []
        predictions_per_module = []
        sentence_results = []

        for i, sentence in enumerate(ds):
            if i >= max_examples:
                break
                
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
                logging.error(f"[{module_name}] Black formatting failed: {e}")

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
                prediction = AnnotationList.from_output(
                    result_str,
                    task_module=module_name
                )
            except Exception as e:
                logging.error(f"[{module_name}] Parsing failed for sentence {i}: {e}")
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
            
            # 7. Intermediate Saving
            if i % 10 == 0 or i == max_examples - 1:
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
                
                if i % 50 == 0:
                     logging.info(f"[{module_name}] Progress: {i}/{max_examples}")

        logging.info(f"[{module_name}] Finished! Results matched to {log_filename}")
        return log_filename

    except Exception as e:
        import traceback
        traceback.print_exc()
        logging.error(f"[{module_name}] Critical failure: {e}")
        return None

def run_experiment():
    """
    Main entry point. Runs modules in parallel.
    """
    # Create results directory
    RESULTS_DIR = "GOLLIE-results"
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    # List of modules to process
    job_list = list(MODULE_MAP.keys())
    
    logging.info(f"Beginning Parallel Experiment Run on {len(job_list)} modules with 2 workers.")
    
    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = []
        for mod_name in job_list:
            # We set max_examples here
            futures.append(executor.submit(process_module, mod_name, 3765))
            
        for future in futures:
            res = future.result()
            print(f"Task completed. Result: {res}")

if __name__ == "__main__":
    run_experiment()