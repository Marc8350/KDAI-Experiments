import os
import sys
import subprocess
try:
    from dotenv import load_dotenv
except ImportError:
    # If python-dotenv is not installed, we can't load .env automatically
    # but we can assume environment vars might be set otherwise.
    def load_dotenv(): pass

# Get the absolute path of the project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Add GoLLIE subfolder to path for its internal 'src' imports
GOLLIE_PATH = os.path.join(PROJECT_ROOT, "GoLLIE")
if GOLLIE_PATH not in sys.path:
    sys.path.append(GOLLIE_PATH)

import re
import json
import logging
import inspect
import black
from datetime import datetime
from tqdm import tqdm
import argparse
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
    "quantization": 4, #For testing on Small GPU with less than 20 Gb Ram 
    "use_lora": False,
    "force_auto_device_map": True,
    "use_flash_attention": False, # For testing on Colab
    "torch_dtype": "bfloat16",
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
    """
    Convert dataset label to PascalCase class name.
    
    Examples:
        'art-broadcastprogram' -> 'ArtBroadcastprogram'
        'location-GPE' -> 'LocationGpe'
        'event-attack/battle/war/militaryconflict' -> 'EventAttackBattleWarMilitaryconflict'
    """
    if label == "O":
        return None
    
    # Convert to lowercase first, then split by delimiters
    label_lower = label.lower()
    # Split by both - and / and capitalize first letter of each part
    parts = re.split(r'[-/]', label_lower)
    # Capitalize first letter of each part to create PascalCase
    return "".join(part.capitalize() for part in parts if part)

def setup_git_experiment_branch():
    """Configures git and creates a new branch for the experiment run."""
    try:
        load_dotenv()
        git_url = os.environ.get("GIT_SET_URL")
        
        # Check if we are in a git repo
        if not os.path.isdir(".git"):
            logging.warning("Not a git repository. Skipping git automation.")
            return False

        if git_url:
            # Configure remote with token if provided
             subprocess.run(f"git remote set-url origin {git_url}", shell=True, check=True)
        else:
            logging.info("GIT_SET_URL not set. Assuming existing git config is valid.")
            
        # Configure user if not set (common in Colab)
        try:
            subprocess.run("git config user.name", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
             logging.info("Configuring git user for Colab...")
             subprocess.run('git config --global user.email "experiment@colab.run"', shell=True)
             subprocess.run('git config --global user.name "Colab Experiment"', shell=True)
             
        # Create unique branch for this run
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        branch_name = f"experiment-run-{timestamp}"
        
        # Create and checkout
        subprocess.run(f"git checkout -b {branch_name}", shell=True, check=True)
        
        # Try to push upstream. If it fails (e.g. no permissions), we log it.
        try:
            subprocess.run(f"git push -u origin {branch_name}", shell=True, check=True)
            logging.info(f"Initialized and pushed git branch: {branch_name}")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to push new branch {branch_name}: {e}")
            return False
            
    except Exception as e:
        logging.error(f"Git setup failed: {e}")
        return False

def sync_results_to_git(message: str):
    """Adds, commits, and pushes changes in the results directory."""
    try:
        # Check if there are changes to commit
        status = subprocess.run("git status --porcelain GOLLIE-results/", shell=True, stdout=subprocess.PIPE, text=True)
        if not status.stdout.strip():
            return # No changes
            
        subprocess.run("git add GOLLIE-results/", shell=True, check=True)
        subprocess.run(f'git commit -m "{message}"', shell=True, check=True)
        subprocess.run("git push", shell=True, check=True)
        logging.info(f"Synced results to git: {message}")
    except Exception as e:
        logging.warning(f"Git sync failed: {e}")

def run_experiment(limit: int = None):
    """
    Iterates over guideline modules and processes sentences from few-nerd_test.
    """
    # Create results directory
    RESULTS_DIR = "GOLLIE-results"
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Initialize Git Branch
    setup_git_experiment_branch()

    # Load dataset
    ds = load_from_disk("./few-nerd_test")
    if limit:
        ds = ds.select(range(min(limit, len(ds))))
        logging.info(f"Limiting dataset to {limit} sentences.")
        
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
                sync_results_to_git(f"Update results pending: {module_name} step {i}")

        logging.info(f"Finished module {module_name}. Full results available at {log_filename}")
        sync_results_to_git(f"Completed module: {module_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run GoLLIE experiments.")
    parser.add_argument("--limit", type=int, default=None, help="Limit the number of sentences to process.")
    args = parser.parse_args()
    
    run_experiment(limit=args.limit)