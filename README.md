# KDAI-Experiments: Named Entity Recognition with Prompt Engineering

This repository contains experiments comparing **GoLLIE** and **CodeIE** frameworks for Named Entity Recognition (NER) on the **Few-NERD** dataset. The key research focus is studying how **prompt variations** (paraphrased annotation guidelines) affect model performance.

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Prompt Engineering Methodology](#prompt-engineering-methodology)
   - [Data Source: Few-NERD Dataset](#data-source-few-nerd-dataset)
   - [Example Sampling Strategy](#example-sampling-strategy)
   - [Base Guidelines Generation](#base-guidelines-generation)
   - [Prompt Variation Generation](#prompt-variation-generation)
4. [GoLLIE Experiments](#gollie-experiments)
   - [Prompt Format](#gollie-prompt-format)
   - [Running GoLLIE Experiments](#running-gollie-experiments)
5. [CodeIE Experiments](#codeie-experiments)
   - [Prompt Format](#codeie-prompt-format)
   - [Running CodeIE Experiments](#running-codeie-experiments)
6. [Setup Instructions](#setup-instructions)
7. [Results](#results)
8. [References](#references)

---


## Overview

This project investigates the effect of **annotation guideline paraphrasing** on zero-shot and few-shot NER performance. We leverage two state-of-the-art information extraction frameworks:

| Framework | Approach | Key Feature |
|-----------|----------|-------------|
| **GoLLIE** | Guideline-following LLM | Uses Python dataclass definitions with docstrings as entity schema |
| **CodeIE** | Code generation for IE | Frames NER as code generation with function templates |

Both frameworks are enhanced with **explicit entity type definitions** in prompts, giving the model clearer guidance about valid entity types.

---

## Project Structure

```
KDAI-Experiments/
├── annotation_guidelines/          # Generated GoLLIE prompt variations
│   ├── guidelines_coarse_gollie.py          # Base coarse-grained guidelines
│   ├── guidelines_coarse_gollie_v1.py       # Standard paraphrase variation 1
│   ├── guidelines_coarse_gollie_detailed_v1.py  # Detailed paraphrase variation 1
│   ├── guidelines_fine_gollie.py            # Base fine-grained guidelines
│   ├── guidelines_fine_gollie_v1.py         # Fine-grained variations
│   └── *.json                               # Creation logs with similarity scores
│

├── Code_for_Prompt_generation/     # Scripts for generating prompts and variations
│   ├── generate_annotated_examples.py   # Extracts examples from Few-NERD
│   ├── coarse_labels_examples.json      # 8 examples per coarse entity type
│   ├── fine_labels_examples.json        # 8 examples per fine entity type
│   ├── create_gollie_guidelines.py      # Generates base GoLLIE guidelines
│   └── generate_variations_v2.py        # Enhanced variation generator
│
├── GoLLIE/                         # GoLLIE framework (submodule)
│   ├── src/                        # Core GoLLIE source code
│   └── templates/prompt.txt        # Jinja2 template for prompts
│
├── CodeIE/                         # CodeIE framework (adapted)
│   ├── prepare_fewnerd_for_codeie.py       # Data converter
│   ├── generate_codeie_prompt_variations.py # Prompt variation generator
│   ├── run_codeie_experiments.py           # Experiment runner
│   └── data/                               # Converted Few-NERD data
│
├── few-nerd_train/                 # Few-NERD training split (HuggingFace format)
├── few-nerd_validation/            # Few-NERD validation split
├── few-nerd_test/                  # Few-NERD test split
│
├── run_gollie_experiments.py       # Main GoLLIE experiment script
├── Experiments.ipynb               # Notebook version not ready yet
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## Prompt Engineering Methodology

### Data Source: Few-NERD Dataset

We use the **Few-NERD** dataset ([Ding et al., 2021](https://aclanthology.org/2021.acl-long.248/)), which provides:

| Granularity | Entity Types | Description |
|-------------|--------------|-------------|
| **Coarse** | 8 types | `person`, `location`, `organization`, `building`, `art`, `product`, `event`, `other` |
| **Fine** | 66 types | Hierarchical subtypes (e.g., `person-actor`, `location-GPE`, `art-film`) |

**Dataset Statistics:**
- Training: ~131,000 sentences
- Validation: ~18,000 sentences  
- Test: ~37,000 sentences

The dataset is automatically downloaded and saved in HuggingFace `datasets` format:

```python
from datasets import load_dataset
dataset = load_dataset("DFKI-SLT/few-nerd", name='supervised')
```

### Example Sampling Strategy

Examples for the prompt guidelines are extracted using **`generate_annotated_examples.py`**:

#### Sampling Process

1. **Iterate through training data** to find sentences containing each entity type
2. **Extract 8 representative examples per class** to ensure diversity
3. **Format with inline annotations**: Entities are marked with `#Label#` tags

**Example Output Format:**
```
"Time #art# " magazine said the film was " a multimillion dollar improvisation...
```

**Algorithm:**
```python
def collect_examples(ds, label_feature_name, num_examples=8):
    # Initialize dict for all labels except 'O'
    for name in label_names:
        if name != 'O':
            examples_dict[name] = []
    
    # Find examples for each entity type
    for sample in ds:
        for tag_id in sample[tags]:
            if len(examples_dict[label_name]) < num_examples:
                # Format: "Token #label#"
                formatted = format_sentence(tokens, tags, label_names)
                examples_dict[label_name].append(formatted)
```

**Output Files:**
- `coarse_labels_examples.json` - 8 examples × 8 types = 64 examples
- `fine_labels_examples.json` - 8 examples × 66 types = 528 examples

### Prompt Generation Pipeline

The following flowchart illustrates how the prompt variations are created, ensuring a clear distinction between Standard (4-shot) and Detailed (8-shot) guidelines.

```mermaid
graph TD
    A[Few-NERD Dataset] -->|generate_annotated_examples.py| B[examples.json<br>(8 examples/class)]
    B -->|create_gollie_guidelines.py| C{Split & Generate}
    C -->|Slice: First 4 Examples| D[Base Standard<br>guidelines_*.py<br>(4 Examples)]
    C -->|Keep: All 8 Examples| E[Detailed Source<br>guidelines_*_8_examples.py<br>(8 Examples)]
    D -->|generate_variations_v2.py<br>Mode: Standard| F[Standard Variations<br>v1, v2, v3<br>(4 Examples Paraphrased)]
    E -->|generate_variations_v2.py<br>Mode: Detailed| G[Detailed Variations<br>detailed_v1, detailed_v2, detailed_v3<br>(8 Examples Paraphrased)]
```

#### 1. Example Extraction
We extract 8 examples per class from the Few-NERD training set using `generate_annotated_examples.py`. These are saved to JSON files.

#### 2. Base Guidelines & Splitting
`create_gollie_guidelines.py` reads the JSONs and generates two Python files per granularity:
- **Base Guidelines (`guidelines_*.py`)**: Uses only the first **4 examples** per class. This serves as the primary baseline and source for standard variations.
- **Detailed Source (`guidelines_*_8_examples.py`)**: Uses all **8 examples** per class. This serves as the rich source for detailed variations.

#### 3. Variation Generation
`generate_variations_v2.py` uses Gemini to paraphrase the guidelines:
- **Standard Variations (v1-v3)**: Derived from the 4-example Base Guidelines. The LLM is allowed to substitute examples.
- **Detailed Variations (detailed_v1-v3)**: Derived from the 8-example Detailed Source. The LLM preserves the richer context of 8 examples.

---

## GoLLIE Experiments

### GoLLIE Prompt Format

GoLLIE uses a **Jinja2 template** (`GoLLIE/templates/prompt.txt`):

```jinja
# The following lines describe the task definition
{%- for definition in guidelines %}
{{ definition }}
{%- endfor %}

# This is the text to analyze
text = {{ text.__repr__() }}

# The annotation instances that take place in the text above are listed here
result = [
{%- for ann in annotations %}
    {{ ann }},
{%- endfor %}
]
```

**Rendered Example:**
```python
# The following lines describe the task definition
@dataclass
class Person(Entity):
    """Refers to individual human beings, including historical figures..."""
    span: str  # Such as: "George Axelrod", "Richard Quine"

@dataclass
class Location(Entity):
    """Refers to geographical entities, including countries, regions..."""
    span: str  # Such as: "Michigan", "Republic of Croatia"

# This is the text to analyze
text = "Apple announced Steve Jobs would present the new iPhone in San Francisco."

# The annotation instances that take place in the text above are listed here
result = [
    Person(span="Steve Jobs"),
    Location(span="San Francisco"),
]
```

### Running GoLLIE Experiments

**Script:** `run_gollie_experiments.py`

```bash
# Activate virtual environment
source .venv/bin/activate

# Run experiments (iterates through all 14 guideline modules)
python run_gollie_experiments.py
```

**Configuration:**
```python
MODEL_LOAD_PARAMS = {
    "inference": True,
    "model_weights_name_or_path": "HiTZ/GoLLIE-7B",
    "quantization": None,  # Set to 4 for 4-bit quantization on Colab
    "use_lora": False,
    "force_auto_device_map": True,
    "use_flash_attention": True,  # False for T4 GPUs
    "torch_dtype": "bfloat16"
}

GENERATE_PARAMS = {
    "max_new_tokens": 128,
    "do_sample": False,
    "num_beams": 1,
    "num_return_sequences": 1,
}
```

**Output:** Results are saved to `GOLLIE-results/` as JSON files with:
- Per-sentence predictions and gold labels
- Running F1/P/R scores
- Model and generation parameters

---

## CodeIE Experiments

### CodeIE Prompt Format

CodeIE supports two styles:

#### 1. Code Style (pl-func)
```python
def named_entity_recognition(input_text):
    """ extract named entities from the input_text """
    # Entity types to extract
    # "person": A named individual...
    # "location": A geographical location...
    
    input_text = "Apple announced Steve Jobs would present..."
    entity_list = []
    # extracted named entities
    entity_list.append({"text": "Steve Jobs", "type": "person"})
    entity_list.append({"text": "San Francisco", "type": "location"})
# END
```

#### 2. Natural Language Style (nl-sel)
```
Given the entity types: person, location, organization, ...

Text: "Apple announced Steve Jobs would present the new iPhone in San Francisco."

Named entities found: <0> person <5> Steve Jobs <1> <0> location <5> San Francisco <1>
```

### CodeIE Data Preparation

**Script:** `CodeIE/prepare_fewnerd_for_codeie.py`

```bash
# Convert Few-NERD to CodeIE format
python CodeIE/prepare_fewnerd_for_codeie.py --granularity coarse
python CodeIE/prepare_fewnerd_for_codeie.py --granularity fine
```

**Few-Shot Sampling:**
- Creates stratified samples: 1, 2, 3, 5, 10 shots per entity type
- Multiple seeds (1, 2, 3) for reproducibility
- Matches original CodeIE sampling strategy

### Running CodeIE Experiments

**Script:** `CodeIE/run_codeie_experiments.py`

```bash
# Single variation
python CodeIE/run_codeie_experiments.py \
    --granularity coarse \
    --style pl \
    --variation v1_schema_aware \
    --num_shots 5

# All variations
python CodeIE/run_codeie_experiments.py \
    --granularity coarse \
    --style pl \
    --run_all_variations

# Without entity schema (original CodeIE behavior)
python CodeIE/run_codeie_experiments.py \
    --granularity coarse \
    --style pl \
    --no_schema
```

**Key Arguments:**
| Argument | Options | Description |
|----------|---------|-------------|
| `--granularity` | `coarse`, `fine` | Entity granularity level |
| `--style` | `pl`, `nl` | Prompt style (code or natural language) |
| `--variation` | `v0_original`, `v1_schema_aware`, etc. | Prompt variation to use |
| `--num_shots` | 1, 2, 3, 5, 10 | Few-shot examples per type |
| `--no_schema` | flag | Disable entity definitions in prompt |

---

## Setup Instructions

### Prerequisites

- Python 3.10+
- CUDA-capable GPU (recommended: A100, L4, or T4 with quantization)
- 16GB+ GPU memory (or use 4-bit quantization)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Marc8350/KDAI-Experiments.git
cd KDAI-Experiments

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows

# 3. Run the setup_project.py to setup the the experiments. 
python setup_project.py

# 4. Before running the run_gollie_experiments.py please modify the configurations according to your system
#For colab / T4 based systems you can use: 
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
#and for Cuda use if you have enough G RAM: 
# Configurable parameters
MODEL_LOAD_PARAMS = {
    inference=True,
    model_weights_name_or_path="HiTZ/GoLLIE-7B",
    quantization=None,
    use_lora=False,
    force_auto_device_map=True,
    use_flash_attention=True,
    torch_dtype="bfloat16"
}
```
### Environment Variables

Create a `.env` file in the project root:

```bash
# For prompt variation generation
GEMINI_API_KEY=your_gemini_api_key_here
#
GIT_SET_URL=your_git_access_token # or remove the git functions from the code. 
# For CodeIE experiments (if using custom API)
CUSTOM_API_BASE_URL=http://localhost:8000/v1
CUSTOM_API_KEY=not-needed
CUSTOM_MODEL_NAME=qwen2.5-7b
```


### Running on Google Colab

->  Use the terminal in colab to run the steps shown above with the modified model configuration. 
```bash
python run_gollie_experiments.py
```
---

## Results

Results are saved in:
- **GoLLIE:** `GOLLIE-results/{module_name}_{timestamp}.json`
- **CodeIE:** `CodeIE/CODEIE-results/{config}_{timestamp}.json`

**Result Format:**
```json
{
  "module": "annotation_guidelines.guidelines_coarse_gollie_v1",
  "timestamp": "20260131_143547",
  "model_load_params": { ... },
  "generate_params": { ... },
  "overall_score": {
    "entities": {
      "precision": 0.8234,
      "recall": 0.7891,
      "f1": 0.8058
    }
  },
  "processed_count": 100,
  "sentences": [
    {
      "index": 0,
      "text": "...",
      "gold": ["Person(span='Steve Jobs')"],
      "prediction": ["Person(span='Steve Jobs')"],
      "score": { ... }
    }
  ]
}
```

---

## References

### Frameworks

1. **GoLLIE**: Sainz et al. (2024). "GoLLIE: Annotation Guidelines improve Zero-Shot Information-Extraction." ICLR 2024. [Paper](https://openreview.net/forum?id=Y3wpuxd7u9) | [Code](https://github.com/hitz-zentroa/GoLLIE)

2. **CodeIE**: Li et al. (2023). "CodeIE: Large Code Generation Models are Better Few-Shot Information Extractors." ACL 2023. [Paper](https://arxiv.org/abs/2305.05711) | [Code](https://github.com/artpli/CodeIE)

### Dataset

3. **Few-NERD**: Ding et al. (2021). "Few-NERD: A Few-shot Named Entity Recognition Dataset." ACL 2021. [Paper](https://aclanthology.org/2021.acl-long.248/) | [Dataset](https://huggingface.co/datasets/DFKI-SLT/few-nerd)

### Models

4. **GoLLIE-7B**: [HiTZ/GoLLIE-7B](https://huggingface.co/HiTZ/GoLLIE-7B)


---

## License

This project is for academic research purposes. Please refer to the individual licenses of GoLLIE, CodeIE, and Few-NERD for their respective usage terms.

## Citation

If you use this work, please cite:

```bibtex
@misc{kdai-experiments,
  author = {Marc Rodig},
  title = {KDAI-Experiments: NER with Prompt Engineering},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/Marc8350/KDAI-Experiments}
}
```
