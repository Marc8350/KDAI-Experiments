import os
import sys

# Set environment variable to optimize CUDA memory allocation
# Must be set before importing torch to be effective
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
os.environ["PYTORCH_ALLOC_CONF"] = "expandable_segments:True"

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
import importlib
import signal
import multiprocessing as mp
from typing import Dict, List, Type, Any
from datasets import load_from_disk

from annotation_guidelines import (
    guidelines_coarse_gollie,
    guidelines_coarse_gollie_backtranslated_v1,
    guidelines_coarse_gollie_backtranslated_v2,
    guidelines_coarse_gollie_backtranslated_v3,
    guidelines_coarse_gollie_v1,
    guidelines_coarse_gollie_v2,
    guidelines_coarse_gollie_v3,
    guidelines_fine_gollie,
    guidelines_fine_gollie_backtranslated_v1,
    guidelines_fine_gollie_backtranslated_v2,
    guidelines_fine_gollie_backtranslated_v3,
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
    guidelines_coarse_gollie_backtranslated_v1,
    guidelines_coarse_gollie_backtranslated_v2,
    guidelines_coarse_gollie_backtranslated_v3,
    guidelines_coarse_gollie_v1,
    guidelines_coarse_gollie_v2,
    guidelines_coarse_gollie_v3,
    guidelines_fine_gollie,
    guidelines_fine_gollie_backtranslated_v1,
    guidelines_fine_gollie_backtranslated_v2,
    guidelines_fine_gollie_backtranslated_v3,
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
    "use_flash_attention": False, # Enabled for A100 and False to disable flash attention.
    "torch_dtype": "bfloat16",
}

GENERATE_PARAMS = {
    "max_new_tokens": 128,
    "do_sample": False,
    "min_new_tokens": 0,
    "num_beams": 1,
    "num_return_sequences": 1,
    "pad_token_id": 2, # Manually set to avoid the repetitive warning
    "eos_token_id": 2,
}

# Batch size for incremental saving (save every N sentences per worker)
INCREMENTAL_SAVE_BATCH_SIZE = 50

class MyEntityScorer:
    """Compute the F1 score for Named Entity Recognition Tasks"""
    pass  # Will be properly initialized in worker with SpanScorer

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

def _worker_loop(
    gpu_id: int,
    task_queue: "mp.Queue",
    result_queue: "mp.Queue",
    template_path: str,
    ready_barrier: "mp.Barrier" = None
):
    """Worker process that loads the model once and processes tasks."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    # Import torch-dependent modules AFTER setting CUDA_VISIBLE_DEVICES
    from src.model.load_model import load_model
    from src.tasks.utils_typing import Entity, AnnotationList
    from src.tasks.utils_scorer import SpanScorer
    
    import torch
    try:
        torch.cuda.set_device(0)
    except Exception:
        pass

    ds = load_from_disk("./few-nerd_test")
    from jinja2 import Template
    with open(template_path, "rt") as f:
        template = Template(f.read())

    logging.info(f"[worker:{gpu_id}] Loading GoLLIE model...")
    model, tokenizer = load_model(**MODEL_LOAD_PARAMS)
    
    logging.info(f"[worker:{gpu_id}] Model loaded, signaling ready...")
    if ready_barrier:
        ready_barrier.wait()  # Signal that this worker is ready
    logging.info(f"[worker:{gpu_id}] Starting task processing loop...")

    while True:
        task = task_queue.get()
        if task is None:
            break

        module_name, indices, tag_key, names_ref = task
        module = importlib.import_module(module_name)
        
        # Create scorer class dynamically in worker
        from src.tasks.utils_scorer import SpanScorer
        
        class WorkerEntityScorer(SpanScorer):
            """Compute the F1 score for Named Entity Recognition Tasks"""
            valid_types: List[Type] = []
            
            def __call__(self, reference, predictions):
                output = super().__call__(reference, predictions)
                return {"entities": output["spans"]}
        
        scorer = WorkerEntityScorer()
        scorer.valid_types = module.ENTITY_DEFINITIONS

        results = []
        for i in indices:
            sentence = ds[i]
            sentence_id = sentence.get("id", str(i))

            tokens = sentence["tokens"]
            text = " ".join(tokens)

            tags = sentence[tag_key]
            gold = []

            current_class_name = None
            current_span_tokens = []

            for token, tag_id in zip(tokens, tags):
                label = names_ref[tag_id]
                class_name = label_to_classname(label)

                entity_class = getattr(module, class_name, None) if class_name else None

                if entity_class and class_name == current_class_name:
                    current_span_tokens.append(token)
                else:
                    if current_class_name:
                        prev_entity_class = getattr(module, current_class_name, None)
                        if prev_entity_class:
                            gold.append(prev_entity_class(span=" ".join(current_span_tokens)))

                    if entity_class:
                        current_class_name = class_name
                        current_span_tokens = [token]
                    else:
                        current_class_name = None
                        current_span_tokens = []

            if current_class_name:
                prev_entity_class = getattr(module, current_class_name, None)
                if prev_entity_class:
                    gold.append(prev_entity_class(span=" ".join(current_span_tokens)))

            formatted_text = template.render(
                guidelines=[inspect.getsource(definition) for definition in module.ENTITY_DEFINITIONS],
                text=text,
                annotations=gold,
                gold=gold
            )

            try:
                formatted_text = black.format_str(formatted_text, mode=black.Mode())
            except Exception as e:
                logging.error(f"Black formatting failed: {e}")

            prompt, _ = formatted_text.split("result =")
            prompt = prompt + "result ="

            model_input = tokenizer(prompt, add_special_tokens=True, return_tensors="pt")
            model_input["input_ids"] = model_input["input_ids"][:, :-1]
            model_input["attention_mask"] = model_input["attention_mask"][:, :-1]

            model_output = model.generate(
                **model_input.to(model.device),
                **GENERATE_PARAMS
            )

            decoded_output = tokenizer.decode(model_output[0], skip_special_tokens=True)
            result_str = decoded_output.split("result =")[-1]

            try:
                prediction = AnnotationList.from_output(
                    result_str,
                    task_module=module_name
                )
            except Exception as e:
                logging.error(f"Parsing failed for sentence {i}: {e}")
                prediction = []

            sentence_score = scorer(reference=[gold], predictions=[prediction])

            results.append({
                "index": i,
                "id": sentence_id,
                "timestamp": datetime.now().isoformat(),
                "text": text,
                "gold": [str(g) for g in gold],
                "prediction": [str(p) for p in prediction],
                "score": sentence_score
            })

            del model_input, model_output
            
            # Send batch incrementally
            if len(results) >= INCREMENTAL_SAVE_BATCH_SIZE:
                result_queue.put((module_name, results, False))  # False = not final batch
                results = []

        # Send remaining results (final batch for this task)
        if results:
            result_queue.put((module_name, results, True))  # True = final batch
        else:
            result_queue.put((module_name, [], True))  # Empty final to signal completion

    gc.collect()
    torch.cuda.empty_cache()


def _run_module_experiment(
    module,
    limit: int = None,
    enable_git: bool = True,
    resume: bool = False,
    task_queues: List["mp.Queue"] = None,
    result_queue: "mp.Queue" = None,
    pbar: tqdm = None
):
    """
    Runs experiment for a single guideline module with sentence-level parallelism.
    """
    RESULTS_DIR = "GOLLIE-results"
    os.makedirs(RESULTS_DIR, exist_ok=True)

    module_name = module.__name__
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(RESULTS_DIR, f"{module_name}_{timestamp}.json")

    ds = load_from_disk("./few-nerd_test")
    if limit:
        ds = ds.select(range(min(limit, len(ds))))
        logging.info(f"Limiting dataset to {limit} sentences.")

    coarse_names = ds.features["ner_tags"].feature.names
    fine_names = ds.features["fine_ner_tags"].feature.names

    is_coarse = "coarse" in module_name
    tag_key = "ner_tags" if is_coarse else "fine_ner_tags"
    names_ref = coarse_names if is_coarse else fine_names

    # Import scorer here to avoid early torch initialization
    from src.tasks.utils_scorer import SpanScorer
    
    class ModuleEntityScorer(SpanScorer):
        """Compute the F1 score for Named Entity Recognition Tasks"""
        valid_types: List[Type] = []
        
        def __call__(self, reference, predictions):
            output = super().__call__(reference, predictions)
            return {"entities": output["spans"]}
    
    scorer = ModuleEntityScorer()
    scorer.valid_types = module.ENTITY_DEFINITIONS

    sentence_results = []
    processed_ids = set()

    if resume:
        existing_files = [
            f for f in os.listdir(RESULTS_DIR)
            if f.startswith(f"{module_name}_") and f.endswith(".json")
        ]
        if existing_files:
            latest_file = sorted(existing_files)[-1]
            latest_path = os.path.join(RESULTS_DIR, latest_file)
            try:
                with open(latest_path, "r") as f:
                    prev_results = json.load(f)

                if prev_results.get("sentences"):
                    sentence_results = prev_results["sentences"]
                    for s in sentence_results:
                        if "id" in s:
                            processed_ids.add(s["id"])

                    log_filename = latest_path
                    timestamp = prev_results["timestamp"]
                    logging.info(
                        f"Resuming {module_name} with {len(processed_ids)} already processed samples from {latest_file}"
                    )
            except Exception as e:
                logging.error(f"Failed to load previous results for {module_name}: {e}")

    if limit is not None and len(sentence_results) >= limit:
        logging.info(
            f"[{module_name}] Resume has {len(sentence_results)} samples; limit={limit}. Skipping processing."
        )
        return log_filename

    indices_to_process = []
    for i, sentence in enumerate(ds):
        sentence_id = sentence.get("id", str(i))
        if resume and sentence_id in processed_ids:
            continue
        indices_to_process.append(i)

    if not indices_to_process:
        logging.info(f"[{module_name}] No new sentences to process.")
        return log_filename

    worker_count = len(task_queues) if task_queues else 1
    chunks = [indices_to_process[i::worker_count] for i in range(worker_count)]

    logging.info(f"[{module_name}] Distributing {len(indices_to_process)} sentences to {worker_count} workers")
    
    tasks_sent = 0
    for gpu_id, chunk in enumerate(chunks):
        if chunk:
            logging.info(f"[{module_name}] Sending {len(chunk)} sentences to worker {gpu_id}")
            task_queues[gpu_id].put((module_name, chunk, tag_key, names_ref))
            tasks_sent += 1

    logging.info(f"[{module_name}] Waiting for results from {tasks_sent} workers...")
    workers_done = 0
    batches_received = 0
    
    while workers_done < tasks_sent:
        result_module, result_items, is_final = result_queue.get()
        if result_module != module_name:
            logging.warning(f"[{module_name}] Received results for {result_module}")
        
        batches_received += 1
        sentence_results.extend(result_items)
        
        if pbar:
            pbar.update(len(result_items))
        
        if is_final:
            workers_done += 1
            logging.info(f"[{module_name}] Worker completed. {workers_done}/{tasks_sent} done. Total results: {len(sentence_results)}")
        
        # Save incrementally every few batches
        if batches_received % 4 == 0 or is_final:  # Save roughly every 200 sentences (4 batches * 50)
            sentence_results.sort(key=lambda s: s["index"])
            interim_results = {
                "module": module_name,
                "timestamp": timestamp,
                "model_load_params": MODEL_LOAD_PARAMS,
                "generate_params": GENERATE_PARAMS,
                "overall_score": None,  # Will be computed at the end
                "processed_count": len(sentence_results),
                "status": "in_progress" if workers_done < tasks_sent else "completed",
                "sentences": sentence_results
            }
            with open(log_filename, "w") as f:
                json.dump(interim_results, f, indent=4)
    
    sentence_results.sort(key=lambda s: s["index"])

    gold_per_module = [reconstruct_entities(s["gold"], module) for s in sentence_results]
    predictions_per_module = [reconstruct_entities(s["prediction"], module) for s in sentence_results]
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

    logging.info(f"Finished module {module_name}. Full results available at {log_filename}")
    sync_results_to_git(f"Completed module: {module_name}", enabled=enable_git)

    return log_filename


def run_experiment(limit: int = None, enable_git: bool = True, resume: bool = False, num_workers: int = 2):
    """
    Iterates over guideline modules and processes sentences from few-nerd_test.
    Runs modules sequentially with sentence-level parallelism.
    """
    RESULTS_DIR = "GOLLIE-results"
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Initialize Git Branch
    if enable_git:
        setup_git_experiment_branch()

    import torch
    gpu_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
    worker_count = min(num_workers, gpu_count) if gpu_count else num_workers
    worker_count = max(1, worker_count)

    # Calculate total sentences BEFORE spawning workers to avoid dataset loading conflicts
    ds = load_from_disk("./few-nerd_test")
    if limit:
        ds = ds.select(range(min(limit, len(ds))))
    total_sentences = len(ds) * len(guideline_modules)
    
    logging.info(f"Starting experiment with {len(guideline_modules)} modules and {len(ds)} sentences per module")
    logging.info(f"Total sentences to process: {total_sentences}")

    ctx = mp.get_context("spawn")
    template_path = os.path.join(GOLLIE_PATH, "templates", "prompt.txt")
    task_queues = [ctx.Queue() for _ in range(worker_count)]
    result_queue = ctx.Queue()
    
    # Create a barrier that waits for all workers + main process
    ready_barrier = ctx.Barrier(worker_count + 1)
    
    logging.info(f"Spawning {worker_count} worker processes...")
    workers = [
        ctx.Process(target=_worker_loop, args=(gpu_id, task_queues[gpu_id], result_queue, template_path, ready_barrier))
        for gpu_id in range(worker_count)
    ]
    for p in workers:
        p.start()
    
    logging.info(f"Workers started, waiting for all {worker_count} workers to load models...")
    ready_barrier.wait()  # Wait for all workers to signal ready
    logging.info("All workers ready. Proceeding with experiment...")

    try:
        # Use simple tqdm without multiprocessing features
        pbar = tqdm(total=total_sentences, desc="Overall progress", leave=True, position=0, disable=False)
        try:
            for module in guideline_modules:
                logging.info(f"Starting module: {module.__name__}")
                try:
                    result_path = _run_module_experiment(
                        module,
                        limit=limit,
                        enable_git=enable_git,
                        resume=resume,
                        task_queues=task_queues,
                        result_queue=result_queue,
                        pbar=pbar
                    )
                    logging.info(f"[{module.__name__}] Completed. Results: {result_path}")
                except Exception as e:
                    logging.error(f"[{module.__name__}] Failed: {e}", exc_info=True)
        finally:
            pbar.close()
    except KeyboardInterrupt:
        logging.warning("Received Ctrl+C. Terminating workers...")
        raise
    finally:
        for q in task_queues:
            q.put(None)
        for p in workers:
            p.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run GoLLIE experiments.")
    parser.add_argument("--limit", type=int, default=None, help="Limit the number of sentences to process.")
    parser.add_argument("--no-git", action="store_true", help="Disable git automation (branching/pushing).")
    parser.add_argument("--resume", action="store_true", help="Resume experiment from existing results.")
    parser.add_argument("--workers", type=int, default=2, help="Number of parallel workers.")
    args = parser.parse_args()
    
    run_experiment(limit=args.limit, enable_git=not args.no_git, resume=args.resume, num_workers=args.workers)
