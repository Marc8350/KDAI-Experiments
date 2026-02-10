# CodeIE Output Parsing & Evaluation Workflow

This document illustrates how raw outputs from the LLM are parsed into structured entity lists for evaluation against ground truth.

## Parsing Workflow Diagram

```mermaid
graph TD
    A([Raw LLM Output]) --> B{Prompt Style?}

    %% --- Code Style Parsing Path ---
    B -- "Code (PL)" --> C[Extract Code Block]
    C --> D{Match Pattern?}
    
    D -- "Standard Dict" --> D1["entity_list.append({text: '...', type: '...'})"]
    D -- "Dict Constructor" --> D2["entity_list.append(dict(...))"]
    D -- "Set Syntax Fallback" --> D3["entity_list.append({text, type})"]
    
    D1 --> E[Extract Raw Type, Text]
    D2 --> E
    D3 --> E

    %% --- NL Style Parsing Path ---
    B -- "Natural Language (NL)" --> F{Match Format?}
    
    F -- "Priority 1: Line/Bullet" --> G["* type: text"]
    F -- "Priority 2: Parenthetical" --> H["(type: text)"]
    F -- "Priority 3: SEL Tags" --> I["< 0 > type < 5 > text < 1 >"]
    
    G --> E
    H --> E
    I --> E

    %% --- Normalization & Validation ---
    E --> J[Normalize & Validate Type]
    
    subgraph "match_entity_type(raw_type)"
        J1{Exact Match?}
        J2{Suffix Match?}
        J3{Prefix Match?}
        
        J --> J1
        J1 -- Yes --> Valid[Return Type]
        J1 -- No --> J2
        J2 -- "e.g. product-hotel to building-hotel" --> Valid
        J2 -- No --> J3
        J3 -- "e.g. location to location-GPE" --> Valid
        J3 -- No --> Invalid[Return None]
    end

    Valid --> K[Add to Prediction List]
    Invalid --> L[Discard / Ignore]

    K --> M([Final Evaluated Entity List])
```

## Example Scenario

### Input (Code Style)
```python
def extract_entities(text):
    entity_list = []
    # Model hallucinates a specific subtype 'product-weapon'
    entity_list.append({"text": "B-52", "type": "product-weapon"}) 
```

### Parsing Steps
1. **Style Check**: Detected `PL` (Code).
2. **Regex Extraction**: Matches standard dictionary pattern.
   - Raw Type: `product-weapon`
   - Raw Text: `B-52`
3. **Normalization (`match_entity_type`)**:
   - **Exact Match?** Is `product-weapon` in `[product-airplane, product-car, ...]`? **No**.
   - **Suffix Match?** Does it end with valid suffix? 
     - Checks `product-airplane` vs `weapon`. No match.
   - **Prefix Match?** Does it start with valid prefix?
     - `product-weapon` starts with `product-`?
     - Found `product-airplane`? No.
     - *Detailed Issue*: The fallback logic tries to match the *base category* if strict matching fails. If `product-weapon` isn't in the schema, and only `product-other` exists:
       - If the schema has `product-other`, `product-weapon` might NOT match `product-other` automatically unless explicitly handled or if `product` is a valid type itself.
   - **Result**: If `product-weapon` is not in schema, it returns `None` (or valid type if mapping exists).

### Common Failure Points (Based on recent logs)
1. **Zero F1**: The raw type (e.g., `product-weapon`) implies a correct category, but isn't in the allowed schema. If normalization fails to map it to `product-other`, it is discarded or counted as a False Positive (if treated as a valid but wrong class) vs False Negative (missed gold entity).
2. **Empty Prediction**: Code syntax errors (e.g. `entity_list.append({"Item", "Type"})`) where regex fails to identify text vs type.
