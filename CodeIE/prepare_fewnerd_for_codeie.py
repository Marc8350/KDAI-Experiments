"""
FewNerd to CodeIE Data Converter

This script converts the FewNerd dataset (in HuggingFace format) to the CodeIE format
for NER experiments. It creates the required directory structure and files:
- Schema files (entity.schema, record.schema)  
- Training/validation/test JSON files
- Stratified few-shot samples

Usage:
    python prepare_fewnerd_for_codeie.py --granularity coarse --output_dir data/fewnerd_coarse
    python prepare_fewnerd_for_codeie.py --granularity fine --output_dir data/fewnerd_fine
"""

import os
import sys
import json
import random
import argparse
from collections import defaultdict
from datasets import load_from_disk
from typing import List, Dict, Tuple

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def convert_tags_to_entities(tokens: List[str], tags: List[int], tag_names: List[str]) -> List[Dict]:
    """
    Convert BIO-like tags to entity spans.
    
    FewNerd uses a simple labeling scheme where consecutive tokens with the same
    non-O tag belong to the same entity.
    
    Args:
        tokens: List of tokens
        tags: List of tag indices
        tag_names: List of tag names (e.g., ['O', 'person', 'location', ...])
    
    Returns:
        List of entity dictionaries with 'type', 'offset', and 'text' keys
    """
    entities = []
    current_entity = None
    
    for i, (token, tag_idx) in enumerate(zip(tokens, tags)):
        tag_name = tag_names[tag_idx]
        
        if tag_name == 'O':
            # End current entity if exists
            if current_entity is not None:
                entities.append(current_entity)
                current_entity = None
        else:
            # Check if continuing same entity or starting new one
            if current_entity is None or current_entity['type'] != tag_name:
                # Save previous entity
                if current_entity is not None:
                    entities.append(current_entity)
                # Start new entity
                current_entity = {
                    'type': tag_name,
                    'offset': [i],
                    'text': token
                }
            else:
                # Continue current entity
                current_entity['offset'].append(i)
                current_entity['text'] += ' ' + token
    
    # Don't forget the last entity
    if current_entity is not None:
        entities.append(current_entity)
    
    return entities


def create_spot_asoc(entities: List[Dict]) -> List[Dict]:
    """
    Create spot_asoc structure from entities.
    This is the format CodeIE uses internally.
    
    Args:
        entities: List of entity dictionaries
        
    Returns:
        List of spot_asoc dictionaries
    """
    return [
        {
            'span': entity['text'],
            'label': entity['type'],
            'asoc': []  # Empty for NER (used for relations)
        }
        for entity in entities
    ]


def get_unique_types(entities: List[Dict]) -> List[str]:
    """Extract unique entity types from a list of entities."""
    return list(set(entity['type'] for entity in entities))


def convert_sample(sample: Dict, tag_key: str, tag_names: List[str]) -> Dict:
    """
    Convert a single FewNerd sample to CodeIE format.
    
    Args:
        sample: FewNerd sample dict
        tag_key: 'ner_tags' for coarse or 'fine_ner_tags' for fine-grained
        tag_names: List of tag names
        
    Returns:
        CodeIE-formatted sample dict
    """
    tokens = sample['tokens']
    tags = sample[tag_key]
    text = ' '.join(tokens)
    
    entities = convert_tags_to_entities(tokens, tags, tag_names)
    spot_asoc = create_spot_asoc(entities)
    spots = get_unique_types(entities)
    
    return {
        'text': text,
        'tokens': tokens,
        'entity': entities,
        'relation': [],  # Empty for NER
        'event': [],     # Empty for NER
        'spot': spots,
        'asoc': [],      # Empty for NER
        'spot_asoc': spot_asoc
    }


def create_schema_files(output_dir: str, entity_types: List[str]):
    """
    Create schema files required by CodeIE.
    
    Args:
        output_dir: Directory to save schema files
        entity_types: List of entity type names (excluding 'O')
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # entity.schema - one entity type per line
    entity_schema_path = os.path.join(output_dir, 'entity.schema')
    with open(entity_schema_path, 'w') as f:
        for entity_type in entity_types:
            f.write(f"{entity_type}\n")
    print(f"Created: {entity_schema_path}")
    
    # record.schema - JSON format with type list and role info
    record_schema = {
        'type': entity_types,
        'role': [],  # Empty for NER
        'type_role': {t: [] for t in entity_types}
    }
    record_schema_path = os.path.join(output_dir, 'record.schema')
    with open(record_schema_path, 'w') as f:
        json.dump(record_schema, f, indent=2)
    print(f"Created: {record_schema_path}")


def stratified_sample(
    data: List[Dict],
    entity_types: List[str],
    num_shot: int,
    seed: int = 42
) -> List[Dict]:
    """
    Perform stratified sampling to get N examples per entity type.
    This is CodeIE's sampling strategy.
    
    Args:
        data: List of samples
        entity_types: List of entity types to sample
        num_shot: Number of examples per type
        seed: Random seed
        
    Returns:
        List of sampled examples
    """
    random.seed(seed)
    
    # Build index: entity_type -> list of sample indices that contain it
    type_to_indices = defaultdict(list)
    for idx, sample in enumerate(data):
        if not sample['spot']:  # Empty entity list
            type_to_indices['NULL'].append(idx)
        else:
            for entity_type in set(sample['spot']):
                type_to_indices[entity_type].append(idx)
    
    # Sample from each type
    sampled_indices = set()
    for entity_type in list(entity_types) + ['NULL']:
        if entity_type not in type_to_indices:
            continue
        indices = type_to_indices[entity_type]
        if len(indices) < num_shot:
            print(f"Warning: {entity_type} has only {len(indices)} samples (< {num_shot})")
            sample_count = len(indices)
        else:
            sample_count = num_shot
        sampled = random.sample(indices, sample_count)
        sampled_indices.update(sampled)
    
    # Return sampled data in order
    return [data[i] for i in sorted(sampled_indices)]


def save_data(data: List[Dict], filepath: str):
    """Save data as JSONL file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        for sample in data:
            f.write(json.dumps(sample) + '\n')
    print(f"Saved {len(data)} samples to: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Convert FewNerd to CodeIE format")
    parser.add_argument('--granularity', choices=['coarse', 'fine'], default='coarse',
                        help="Entity granularity: coarse or fine-grained")
    parser.add_argument('--train_path', default='few-nerd_train',
                        help="Path to training dataset")
    parser.add_argument('--val_path', default='few-nerd_validation', 
                        help="Path to validation dataset")
    parser.add_argument('--test_path', default='few-nerd_test',
                        help="Path to test dataset")
    parser.add_argument('--output_dir', default=None,
                        help="Output directory (default: data/fewnerd_{granularity})")
    parser.add_argument('--max_train', type=int, default=None,
                        help="Maximum training samples (for testing)")
    parser.add_argument('--max_test', type=int, default=None,
                        help="Maximum test samples (for testing)")
    parser.add_argument('--create_shots', nargs='+', type=int, default=[1, 2, 3, 5, 10],
                        help="Shot counts to create for few-shot learning")
    parser.add_argument('--seeds', nargs='+', type=int, default=[1, 2, 3],
                        help="Random seeds for few-shot sampling")
    
    args = parser.parse_args()
    
    # Determine tag key and output directory
    if args.granularity == 'coarse':
        tag_key = 'ner_tags'
        output_dir = args.output_dir or 'data/fewnerd_coarse'
    else:
        tag_key = 'fine_ner_tags'
        output_dir = args.output_dir or 'data/fewnerd_fine'
    
    output_dir = os.path.join(PROJECT_ROOT, 'CodeIE', output_dir)
    
    print(f"\n{'='*60}")
    print(f"FewNerd to CodeIE Converter")
    print(f"{'='*60}")
    print(f"Granularity: {args.granularity}")
    print(f"Tag key: {tag_key}")
    print(f"Output directory: {output_dir}")
    print(f"{'='*60}\n")
    
    # Load datasets
    print("Loading datasets...")
    ds_train = load_from_disk(args.train_path)
    ds_val = load_from_disk(args.val_path)
    ds_test = load_from_disk(args.test_path)
    
    # Get tag names
    tag_names = ds_train.features[tag_key].feature.names
    entity_types = [t for t in tag_names if t != 'O']
    
    print(f"Entity types ({len(entity_types)}): {entity_types}")
    
    # Create schema files
    create_schema_files(output_dir, entity_types)
    
    # Convert datasets
    print("\nConverting training set...")
    train_data = []
    for i, sample in enumerate(ds_train):
        if args.max_train and i >= args.max_train:
            break
        train_data.append(convert_sample(sample, tag_key, tag_names))
    
    print("Converting validation set...")
    val_data = [convert_sample(sample, tag_key, tag_names) for sample in ds_val]
    
    print("Converting test set...")
    test_data = []
    for i, sample in enumerate(ds_test):
        if args.max_test and i >= args.max_test:
            break
        test_data.append(convert_sample(sample, tag_key, tag_names))
    
    # Save full datasets
    save_data(train_data, os.path.join(output_dir, 'train.json'))
    save_data(val_data, os.path.join(output_dir, 'val.json'))
    save_data(test_data, os.path.join(output_dir, 'test.json'))
    
    # Create few-shot samples
    print("\nCreating few-shot samples...")
    shot_dir = output_dir + '_shot'
    
    for seed in args.seeds:
        for num_shot in args.create_shots:
            shot_subdir = os.path.join(shot_dir, f'seed{seed}', f'{num_shot}shot')
            os.makedirs(shot_subdir, exist_ok=True)
            
            # Sample training data
            sampled = stratified_sample(train_data, entity_types, num_shot, seed=seed)
            save_data(sampled, os.path.join(shot_subdir, 'train.json'))
            
            # Copy val and test (unchanged)
            save_data(val_data, os.path.join(shot_subdir, 'val.json'))
            save_data(test_data, os.path.join(shot_subdir, 'test.json'))
            
            # Copy schema files
            for schema_file in ['entity.schema', 'record.schema']:
                src = os.path.join(output_dir, schema_file)
                dst = os.path.join(shot_subdir, schema_file)
                if os.path.exists(src):
                    import shutil
                    shutil.copy(src, dst)
    
    print(f"\n{'='*60}")
    print("Conversion complete!")
    print(f"Base data: {output_dir}")
    print(f"Few-shot data: {shot_dir}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
