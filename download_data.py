import os
from datasets import load_dataset

def download_datasets():
    """
    Downloads validation and test splits for specified datasets:
    - eriktks/conll2003
    - tner/bc5cdr
    - tner/ontonotes5
    
    Checks if data exists before downloading.
    Slices datasets if specific counts are requested/implied (e.g. 5000 for validation).
    """
    
    # Configuration for datasets
    # limits: None = get all. Integer = get first N.
    datasets_config = [
        {
            "name": "eriktks/conll2003",
            "splits": ["validation", "test"],
            "limits": {"validation": None, "test": None} 
        },
        {
            "name": "tner/bc5cdr",
            "splits": ["validation", "test"],
            "limits": {"validation": 5000, "test": 4798}
        },
        {
            "name": "tner/ontonotes5",
            "splits": ["validation", "test"],
            "limits": {"validation": 5000, "test": 12217}
        }
    ]
    
    # Create the output directory relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "datasets")
    os.makedirs(output_dir, exist_ok=True)

    for ds_config in datasets_config:
        dataset_name = ds_config["name"]
        print(f"\n--- Processing dataset: {dataset_name} ---")
        
        for split in ds_config["splits"]:
            try:
                # Prepare filename (sanitize slashes in dataset name)
                safe_name = dataset_name.replace("/", "_")
                save_dirname = f"{safe_name}_{split}"
                save_path = os.path.join(output_dir, save_dirname)
                
                # Check if already downloaded
                if os.path.exists(save_path):
                    print(f"Dataset '{dataset_name}' split '{split}' already exists at: {save_dirname}. Skipping.")
                    continue
                
                if dataset_name == "tner/ontonotes5":
                    # Special handling for ontonotes5: rebalance validation and test
                    # We need 12217 for test, but test only has 8262. validation has ~8500.
                    # We will merge them and re-split.
                    
                    # 1. Load both splits fully first
                    print("Custom rebalancing for tner/ontonotes5...")
                    full_valid = load_dataset(dataset_name, split="validation", trust_remote_code=True)
                    full_test = load_dataset(dataset_name, split="test", trust_remote_code=True)
                    
                    from datasets import concatenate_datasets
                    merged = concatenate_datasets([full_valid, full_test])
                    
                    total_available = len(merged)
                    target_test = 12217
                    target_valid = 5000
                    
                    print(f"Total available rows (valid+test): {total_available}")
                    
                    if total_available < target_test:
                        print(f"Warning: requested {target_test} for test, but only {total_available} total available.")
                    
                    # 2. Select the splits
                    # Test gets the FIRST 12217 (or as many as possible)
                    # Validation gets the NEXT 5000
                    
                    test_len = min(target_test, total_available)
                    # Use select for deterministic splitting
                    ds_test = merged.select(range(0, test_len))
                    
                    remaining = total_available - test_len
                    valid_len = min(target_valid, remaining)
                    
                    if valid_len > 0:
                        ds_valid = merged.select(range(test_len, test_len + valid_len))
                    else:
                        print("Warning: No data left for validation split after satisfying test split.")
                        # Create empty dataset if needed, or just warn
                        ds_valid = merged.select(range(0, 0))

                    # 3. Save them explicitly and skip the loop's standard saving
                    
                    path_test = os.path.join(output_dir, f"{safe_name}_test")
                    ds_test.save_to_disk(path_test)
                    print(f"Special save: {safe_name}_test -> {len(ds_test)} rows")
                    
                    path_valid = os.path.join(output_dir, f"{safe_name}_validation")
                    ds_valid.save_to_disk(path_valid)
                    print(f"Special save: {safe_name}_validation -> {len(ds_valid)} rows")
                    
                    # Break the inner loop since we handled both splits
                    break

                # Standard processing for other datasets
                print(f"Downloading '{split}' split for {dataset_name}...")
                
                # Load the specific split
                # trust_remote_code=True needed for some datasets/scripts
                ds = load_dataset(dataset_name, split=split, trust_remote_code=True)
                
                # Apply limit if specified
                limit = ds_config["limits"].get(split)
                if limit is not None:
                    if len(ds) > limit:
                        print(f"Slicing '{split}' from {len(ds)} to {limit} rows.")
                        ds = ds.select(range(limit))
                    elif len(ds) < limit:
                        print(f"Note: Requested limit {limit} is larger than available data {len(ds)} for '{split}'. Keeping all data.")
                    # If equal, do nothing
                
                # Save to disk
                ds.save_to_disk(save_path)
                
                print(f"Successfully saved '{split}' split to: {save_dirname}")
                print(f"Count: {len(ds)} rows")
                
            except Exception as e:
                print(f"Error processing {dataset_name} split '{split}': {e}")

if __name__ == "__main__":
    download_datasets()
