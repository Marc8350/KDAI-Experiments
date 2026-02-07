#!/usr/bin/env python3
"""
Script to reduce data files for Git push.
- Keeps 20% of test data
- Keeps 5% of val data  
- Removes train data (not needed for inference tests)
"""

import json
import os
from pathlib import Path
import random

# Set seed for reproducibility
random.seed(42)

CODEIE_DATA = Path(__file__).parent.parent / "data"

def reduce_json_file(file_path: Path, keep_fraction: float):
    """Load JSONL (JSON Lines), keep a fraction of entries, and save back."""
    if not file_path.exists():
        print(f"  Skipping (not found): {file_path}")
        return
    
    print(f"  Processing: {file_path.name}")
    
    # Read JSONL format (one JSON object per line)
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    
    original_count = len(data)
    keep_count = max(1, int(original_count * keep_fraction))
    
    # Randomly sample
    reduced_data = random.sample(data, keep_count)
    
    # Write back as JSONL
    with open(file_path, 'w') as f:
        for entry in reduced_data:
            f.write(json.dumps(entry) + '\n')
    
    print(f"    Reduced from {original_count} to {keep_count} entries ({keep_fraction*100:.0f}%)")

def delete_file(file_path: Path):
    """Delete a file if it exists."""
    if file_path.exists():
        os.remove(file_path)
        print(f"  Deleted: {file_path.name}")

def process_directory(dir_path: Path, test_fraction: float = 0.2, val_fraction: float = 0.05):
    """Process a single data directory."""
    print(f"\nProcessing: {dir_path}")
    
    # Delete train files (not needed)
    delete_file(dir_path / "train.json")
    
    # Reduce test and val
    reduce_json_file(dir_path / "test.json", test_fraction)
    reduce_json_file(dir_path / "val.json", val_fraction)

def main():
    print("=" * 60)
    print("Reducing CodeIE data files for Git")
    print("=" * 60)
    
    # Main directories
    for granularity in ["coarse", "fine"]:
        main_dir = CODEIE_DATA / f"few-nerd-{granularity}"
        process_directory(main_dir, test_fraction=0.2, val_fraction=0.05)
        
        # Shot directories (1shot, 3shot, etc.)
        shot_base = CODEIE_DATA / f"few-nerd-{granularity}_shot"
        if shot_base.exists():
            for seed_dir in shot_base.iterdir():
                if seed_dir.is_dir():
                    for shot_dir in seed_dir.iterdir():
                        if shot_dir.is_dir():
                            process_directory(shot_dir, test_fraction=0.2, val_fraction=0.05)
    
    print("\n" + "=" * 60)
    print("Done! Data files reduced. You can now commit and push.")
    print("=" * 60)

if __name__ == "__main__":
    main()
