import os
from datasets import load_dataset

def main():
    # Define the dataset name
    dataset_name = "DFKI-SLT/few-nerd"

    # Define the directory to save the dataset
    save_dir = "."

    # Create the directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    print(f"Loading dataset: {dataset_name} (supervised config)")
    # Load the dataset with the 'supervised' config
    dataset = load_dataset(dataset_name, name='supervised')

    # Save each split of the dataset
    for split_name, split_dataset in dataset.items():
        split_save_path = os.path.join(save_dir, f"few-nerd_{split_name}")
        if not os.path.exists(split_save_path):
            print(f"Saving {split_name} split to {split_save_path}...")
            split_dataset.save_to_disk(split_save_path)
        else:
            print(f"Split {split_name} already exists at {split_save_path}")

    print("Dataset setup completed successfully.")

if __name__ == "__main__":
    main()
