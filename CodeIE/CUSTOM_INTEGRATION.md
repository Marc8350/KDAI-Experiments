# CodeIE Integration for FewNerd NER

This integration adapts the [CodeIE](https://github.com/artpli/CodeIE) framework for Named Entity Recognition (NER) experiments on the FewNerd dataset, with support for custom LLM endpoints (e.g., Qwen2.5-7B).

## Overview

### Key Differences from GoLLIE

| Aspect | GoLLIE | CodeIE |
|--------|--------|--------|
| **Prompt Content** | Class definitions with docstrings (guidelines) | Complete examples (input → output) |
| **What varies** | The **docstrings/descriptions** in class definitions | The **function/prompt phrasing** + ICL examples |
| **ICL Strategy** | Guidelines are **static** (no ICL sampling needed) | **Stratified sampling** - N examples per entity type |
| **Prompt Structure** | `guidelines + text + gold` template | `example1 + example2 + ... + test_input` |

### Prompt Styles

1. **Code Style (`pl`)**: Uses Python function call syntax
   ```python
   def named_entity_recognition(input_text):
       """ extract named entities from the input_text . """
       input_text = "The pandemic affected the Mediterranean Basin..."
       entity_list = []
       # extracted named entities
       entity_list.append({"text": "Mediterranean Basin", "type": "location"})
   ```

2. **Natural Language Style (`nl`)**: Uses descriptive text format
   ```
   The text is : "The pandemic affected the Mediterranean Basin..." .
   The named entities in the text: ...
   ```

## Directory Structure

```
CodeIE/
├── data/                           # Prepared datasets
│   ├── fewnerd_coarse/             # Coarse-grained data (8 entity types)
│   │   ├── train.json
│   │   ├── val.json
│   │   ├── test.json
│   │   ├── entity.schema
│   │   └── record.schema
│   └── fewnerd_coarse_shot/        # Stratified few-shot samples
│       └── seed1/
│           ├── 1shot/
│           ├── 3shot/
│           └── 5shot/
│
├── prompt_variations/              # Prompt variations
│   ├── code_style_variations.py    # 7 code-style (pl) variations
│   ├── nl_style_variations.py      # 6 natural language (nl) variations
│   ├── all_variations.json         # JSON export
│   └── __init__.py
│
├── src/api/
│   ├── custom_api_wrapper.py       # Custom Qwen endpoint wrapper
│   └── openai_api_wrapper.py       # Original OpenAI wrapper (reference)
│
├── CODEIE-results/                 # Experiment results (auto-created)
│
# Scripts
├── prepare_fewnerd_for_codeie.py   # Data preparation
├── generate_codeie_prompt_variations.py  # Prompt variation generator
├── run_codeie_experiments.py       # Main experiment runner
└── CUSTOM_INTEGRATION.md           # This file
```

## Quick Start

### 1. Prepare Data

```bash
cd CodeIE

# For testing (limited data)
python prepare_fewnerd_for_codeie.py \
    --granularity coarse \
    --train_path ../few-nerd_train \
    --val_path ../few-nerd_validation \
    --test_path ../few-nerd_test \
    --max_train 1000 \
    --max_test 100 \
    --create_shots 1 3 5 \
    --seeds 1

# For full experiments
python prepare_fewnerd_for_codeie.py \
    --granularity coarse \
    --train_path ../few-nerd_train \
    --val_path ../few-nerd_validation \
    --test_path ../few-nerd_test \
    --create_shots 1 2 3 5 10 \
    --seeds 1 2 3
```

### 2. Generate Prompt Variations

```bash
# Generate predefined variations
python generate_codeie_prompt_variations.py --output_dir prompt_variations

# Also generate LLM-based variations (requires GEMINI_API_KEY in .env)
python generate_codeie_prompt_variations.py --output_dir prompt_variations --generate_llm
```

### 3. Set API Endpoint

Create/update `.env` in the project root:

```bash
CUSTOM_API_BASE_URL=http://localhost:8000/v1
CUSTOM_API_KEY=your-api-key
CUSTOM_MODEL_NAME=qwen2.5-7b
```

Or pass directly via command line:

```bash
python run_codeie_experiments.py --api_url http://localhost:8000/v1 --model qwen2.5-7b
```

### 4. Run Experiments

```bash
# Single experiment
python run_codeie_experiments.py \
    --granularity coarse \
    --style pl \
    --variation v0_original \
    --num_shots 5 \
    --seed 1 \
    --max_test 50  # For testing

# Run all code-style variations
python run_codeie_experiments.py \
    --granularity coarse \
    --style pl \
    --run_all_variations \
    --num_shots 5

# Run all NL-style variations
python run_codeie_experiments.py \
    --granularity coarse \
    --style nl \
    --run_all_variations \
    --num_shots 5
```

## Prompt Variations

### Code Style (7 variations)

| ID | Function Name | Docstring |
|----|---------------|-----------|
| `v0_original` | `named_entity_recognition` | extract named entities from the input_text |
| `v1_formal` | `extract_entities` | identify and extract all named entities present in the input text |
| `v2_task_focused` | `ner_extraction` | perform named entity recognition on the given text and return all entities |
| `v3_concise` | `get_entities` | find named entities in text |
| `v4_detailed` | `named_entity_extraction` | analyze the input text and extract all named entities including persons, locations, organizations and other entity types |
| `v5_academic` | `perform_ner` | apply named entity recognition to identify and classify entity mentions in the text |
| `v6_instruction` | `identify_entities` | given the input text, identify all spans that refer to named entities |

### NL Style (6 variations)

| ID | Input Prefix | Entity Prompt |
|----|--------------|---------------|
| `v0_original` | The text is : | The named entities in the text: |
| `v1_formal` | Input text: | Named entities found: |
| `v2_question` | Given the following text: | What are the named entities? |
| `v3_task` | Text for entity extraction: | Extracted entities: |
| `v4_detailed` | Analyze the following sentence: | The named entities (persons, locations, organizations, etc.) are: |
| `v5_concise` | Text: | Entities: |

## API Endpoint Requirements

The custom API wrapper expects an OpenAI-compatible endpoint with:

- **Completions API**: `POST /v1/completions`
- **Chat API** (optional): `POST /v1/chat/completions`

Request format:
```json
{
    "model": "qwen2.5-7b",
    "prompt": "...",
    "max_tokens": 256,
    "temperature": 0.0,
    "stop": ["# END", "\n----------------------------------------"]
}
```

### Testing the Connection

```python
from src.api.custom_api_wrapper import CustomAPIWrapper

# Test connection
if CustomAPIWrapper.test_connection():
    print("Connected!")
    
# Test generation
response = CustomAPIWrapper.call(
    prompt="def hello():",
    max_tokens=50
)
print(CustomAPIWrapper.parse_response(response))
```

## Output Format

Results are saved as JSON files in `CODEIE-results/`:

```json
{
    "config": {
        "granularity": "coarse",
        "style": "pl",
        "variation": "v0_original",
        "num_shots": 5,
        ...
    },
    "metrics": {
        "precision": 0.85,
        "recall": 0.78,
        "f1": 0.81,
        ...
    },
    "sentences": [
        {
            "index": 0,
            "text": "...",
            "gold": [...],
            "prediction": [...],
            "generated": "...",
            "elapsed_time": 1.23
        }
    ]
}
```

## Comparison with GoLLIE

To compare results with GoLLIE experiments:

1. Both use the same FewNerd test set
2. Both report P/R/F1 using string-based matching
3. Prompt variations are semantically equivalent:
   - GoLLIE: Varies class docstrings/descriptions
   - CodeIE: Varies function docstrings/phrasing

## Troubleshooting

### API Connection Issues
```bash
# Check if endpoint is reachable
curl http://localhost:8000/v1/models
```

### Import Errors
```bash
# Make sure you're in the CodeIE directory
cd CodeIE
python -c "from prompt_variations import CODE_STYLE_VARIATIONS; print('OK')"
```

### Missing Data
```bash
# Re-run data preparation
python prepare_fewnerd_for_codeie.py --help
```
