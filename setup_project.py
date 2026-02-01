import os
import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def run_command(command, cwd=None):
    """Run a shell command and return the exit code."""
    try:
        process = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return True, process.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_gollie():
    """Check if GoLLIE is present, clone if not."""
    if os.path.isdir("GoLLIE"):
        logging.info("GoLLIE directory found.")
        return True
    
    logging.info("GoLLIE directory not found. Cloning...")
    success, output = run_command("git clone https://github.com/hitz-zentroa/GoLLIE.git")
    if success:
        logging.info("Successfully cloned GoLLIE.")
        return True
    else:
        logging.error(f"Failed to clone GoLLIE: {output}")
        return False

def install_requirements():
    """Install requirements if they are not already satisfied."""
    if not os.path.exists("requirements.txt"):
        logging.warning("requirements.txt not found. Skipping dependency installation.")
        return True
    
    logging.info("Checking/Installing requirements from requirements.txt...")
    # Using sys.executable to ensure we install into the current environment
    success, output = run_command(f"\"{sys.executable}\" -m pip install -r requirements.txt")
    if success:
        logging.info("Requirements check/installation complete.")
        return True
    else:
        logging.error(f"Failed to install requirements: {output}")
        return False

def download_data():
    """Ensure dataset is present by downloading if necessary."""
    expected_dirs = ["few-nerd_train", "few-nerd_validation", "few-nerd_test"]
    all_exist = all(os.path.isdir(d) for d in expected_dirs)
    
    if all_exist:
        logging.info("Dataset directories found. Skipping download.")
        return True

    logging.info("Dataset missing or incomplete. Starting download...")
    try:
        # Late import to ensure it works after 'pip install'
        from datasets import load_dataset
        
        dataset_name = "DFKI-SLT/few-nerd"
        save_dir = "."
        
        logging.info(f"Loading dataset: {dataset_name} (supervised config)")
        dataset = load_dataset(dataset_name, name='supervised')

        for split_name, split_dataset in dataset.items():
            split_save_path = os.path.join(save_dir, f"few-nerd_{split_name}")
            if not os.path.exists(split_save_path):
                logging.info(f"Saving {split_name} split to {split_save_path}...")
                split_dataset.save_to_disk(split_save_path)
            else:
                logging.info(f"Split {split_name} already exists.")
        
        logging.info("Data download and setup completed successfully.")
        return True
    except Exception as e:
        logging.error(f"Data download failed: {e}")
        return False

def main():
    logging.info("Starting project setup...")
    
    if not check_gollie():
        sys.exit(1)
        
    if not install_requirements():
        sys.exit(1)
        
    if not download_data():
        sys.exit(1)
        
    logging.info("Setup process finished successfully!")

if __name__ == "__main__":
    main()
