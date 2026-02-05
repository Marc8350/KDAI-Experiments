import os
import sys

# Set environment variable to optimize CUDA memory allocation
# Must be set before importing torch to be effective
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
os.environ["PYTORCH_ALLOC_CONF"] = "expandable_segments:True"

import torch
import gc
import subprocess
try:
    from dotenv import load_dotenv
    load_dotenv()
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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
# Silence only extremely noisy network libraries
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
# Suppress the "Setting pad_token_id to eos_token_id" warning
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="transformers.generation.utils")

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
    "quantization": None, # No quantization (A100) 4 for t4 
    "use_lora": False,
    "force_auto_device_map": True,
    "use_flash_attention": False, # DIAGNOSTIC: Disabled to test if standard attention works
    "torch_dtype": "bfloat16",
}

GENERATE_PARAMS = {
    "max_new_tokens": 128,
    "do_sample": False,
    "min_new_tokens": 5,
    "num_beams": 1,
    "num_return_sequences": 1,
    "pad_token_id": 2, # Manually set to avoid the repetitive warning
    "eos_token_id": 2,
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

def sync_results_to_git(message: str, enabled: bool = True):
    """Adds, commits, and pushes changes in the results directory."""
    if not enabled:
        return
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

def reconstruct_entities(entity_strings, module):
    """Helper to reconstruct Entity objects from their string representation."""
    entities = []
    for s in entity_strings:
        # Match format like Building(span='Grill Room')
        # We use a non-greedy .*? for the span content to handle potential nested quotes if any (though span is usually simple)
        match = re.match(r"(\w+)\(span='(.*)'\)", s)
        if match:
            class_name, span = match.groups()
            entity_class = getattr(module, class_name, None)
            if entity_class:
                # Use class name as stored in module (PascalCase)
                entities.append(entity_class(span=span))
    return entities

def run_experiment(limit: int = None, enable_git: bool = True, resume: bool = False):
    """
    Iterates over guideline modules and processes sentences from few-nerd_test.
    """
    # Create results directory
    RESULTS_DIR = "GOLLIE-results"
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Initialize Git Branch
    if enable_git:
        setup_git_experiment_branch()

    # Load dataset
    ds = load_from_disk("./few-nerd_test")
    if limit:
        ds = ds.select(range(min(limit, len(ds))))
        logging.info(f"Limiting dataset to {limit} sentences.")
        
    coarse_names = ds.features["ner_tags"].feature.names
    fine_names = ds.features["fine_ner_tags"].feature.names

    # Load model
    logging.info(f"Loading GoLLIE model ({MODEL_LOAD_PARAMS['model_weights_name_or_path']})...")
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
        
        is_coarse = "coarse" in module_name
        tag_key = "ner_tags" if is_coarse else "fine_ner_tags"
        names_ref = coarse_names if is_coarse else fine_names
        
        scorer = MyEntityScorer()
        scorer.valid_types = module.ENTITY_DEFINITIONS
        
        gold_per_module = []
        predictions_per_module = []
        sentence_results = []

        # Resumability: Check for existing results
        processed_ids = set()
        if resume:
            # Find the most recent result file for this module
            existing_files = [f for f in os.listdir(RESULTS_DIR) if f.startswith(f"{module_name}_") and f.endswith(".json")]
            if existing_files:
                # Sort by filename (timestamp) to get the latest
                latest_file = sorted(existing_files)[-1]
                latest_path = os.path.join(RESULTS_DIR, latest_file)
                try:
                    with open(latest_path, "r") as f:
                        prev_results = json.load(f)
                    
                    if prev_results.get("sentences"):
                        sentence_results = prev_results["sentences"]
                        # Collect all processed IDs
                        for s in sentence_results:
                            if "id" in s:
                                processed_ids.add(s["id"])
                            gold_per_module.append(reconstruct_entities(s["gold"], module))
                            predictions_per_module.append(reconstruct_entities(s["prediction"], module))
                        
                        # Keep the old filename and timestamp to continue the same run record
                        log_filename = latest_path
                        timestamp = prev_results["timestamp"]
                        
                        logging.info(f"Resuming {module_name} with {len(processed_ids)} already processed samples from {latest_file}")
                except Exception as e:
                    logging.error(f"Failed to load previous results for {module_name}: {e}")

        # Processing loop
        for i, sentence in enumerate(tqdm(ds, desc=f"Processing {module_name}", leave=False)):
            sentence_id = sentence.get("id", str(i))
            if resume and sentence_id in processed_ids:
                continue
            
            if limit and len(sentence_results) >= limit:
                break
            # 1. Prepare sentence text
            tokens = sentence["tokens"]
            text = " ".join(tokens)
            
            # 2. Extract Gold Objects
            tags = sentence[tag_key]
            gold = []

            current_class_name = None
            current_span_tokens = []

            for token, tag_id in zip(tokens, tags):
                label = names_ref[tag_id]
                class_name = label_to_classname(label)
                
                # Check if we have a valid entity class for this tag
                entity_class = getattr(module, class_name, None) if class_name else None
                
                # If same class as strictly previous token, merge
                if entity_class and class_name == current_class_name:
                    current_span_tokens.append(token)
                else:
                    # Flush previous span if valid
                    if current_class_name:
                        prev_entity_class = getattr(module, current_class_name, None)
                        if prev_entity_class:
                           gold.append(prev_entity_class(span=" ".join(current_span_tokens)))
                    
                    # Start new span if valid class
                    if entity_class:
                        current_class_name = class_name
                        current_span_tokens = [token]
                    else:
                        current_class_name = None
                        current_span_tokens = []
            
            # Flush the final span if exists
            if current_class_name:
                prev_entity_class = getattr(module, current_class_name, None)
                if prev_entity_class:
                    gold.append(prev_entity_class(span=" ".join(current_span_tokens)))
            
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
            
            # Check if EOS token was added and remove it if present
            last_token_id = model_input["input_ids"][0, -1].item()
            if last_token_id == tokenizer.eos_token_id:
                if i < 3: logging.info(f"Removing EOS token (id {last_token_id}) from prompt end.")
                model_input["input_ids"] = model_input["input_ids"][:, :-1]
                model_input["attention_mask"] = model_input["attention_mask"][:, :-1]
            else:
                 if i < 3: logging.info(f"Last token (id {last_token_id}) is NOT EOS (expected {tokenizer.eos_token_id}). NOT truncating.")
            
            model_output = model.generate(
                **model_input.to(model.device),
                **GENERATE_PARAMS
            )
            
            # 5. Parse output
            decoded_output = tokenizer.decode(model_output[0], skip_special_tokens=True)
            result_str = decoded_output.split("result =")[-1]
            
            # Debug logging for the first few items
            if i < 3:
                input_len = model_input["input_ids"].shape[1]
                output_len = model_output.shape[1]
                new_tokens = output_len - input_len
                logging.info(f"--- RAW OUTPUT DEBUG (Item {i}) ---")
                logging.info(f"Input tokens: {input_len}, Output tokens: {output_len}, NEW tokens: {new_tokens}")
                logging.info(f"'result =' in output: {'result =' in decoded_output}")
                if result_str.strip():
                    logging.info(f"Extracted Result Str: {result_str[:200]}")
                else:
                    # Show the END of the decoded output to see what's happening
                    logging.info(f"Result is EMPTY! Last 500 chars of decoded output:")
                    logging.info(decoded_output[-500:])
                logging.info("-------------------------------------")
            
            try:
                # AnnotationList.from_output expects a string that looks like [Entity(span='...'), ...]
                # and a task_module name (the package where classes are defined)
                prediction = AnnotationList.from_output(
                    result_str,
                    task_module=module_name
                )
            except Exception as e:
                logging.error(f"Parsing failed for sentence {i}: {e}")
                logging.error(f"Failed string was: {result_str}")
                prediction = []

            # 6. Score individual sentence
            sentence_score = scorer(reference=[gold], predictions=[prediction])
            
            # Store for overall
            gold_per_module.append(gold)
            predictions_per_module.append(prediction)
            
            # Log current sentence
            sentence_data = {
                "index": i,
                "id": sentence_id,
                "timestamp": datetime.now().isoformat(),
                "text": text,
                "gold": [str(g) for g in gold],
                "prediction": [str(p) for p in prediction],
                "score": sentence_score
            }
            sentence_results.append(sentence_data)
            
            # Explicitly free tensor memory
            del model_input, model_output
            
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
            
            if i % 50 == 0 and i > 0:
                logging.info(f"[{module_name}] Processed {i} sentences...")
                sync_results_to_git(f"Step {i}: {module_name}", enabled=enable_git)

        # Clear GPU memory before starting the next module
        gc.collect()
        torch.cuda.empty_cache()
        logging.info(f"Finished module {module_name}. Full results available at {log_filename}")
        sync_results_to_git(f"Completed module: {module_name}", enabled=enable_git)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run GoLLIE experiments.")
    parser.add_argument("--limit", type=int, default=None, help="Limit the number of sentences to process.")
    parser.add_argument("--no-git", action="store_true", help="Disable git automation (branching/pushing).")
    parser.add_argument("--resume", action="store_true", help="Resume experiment from existing results.")
    args = parser.parse_args()
    
    run_experiment(limit=args.limit, enable_git=not args.no_git, resume=args.resume)
