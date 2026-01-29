import json
from datasets import load_from_disk
from tqdm import tqdm
import os

def format_sentence(tokens, tags, label_names, target_label_idx=None):
    """
    Formats a sentence by appending the label name in parentheses for entities.
    If target_label_idx is provided, it only annotates that specific label.
    Otherwise, if labels are provided, it annotates all non-'O' labels.
    """
    annotated_tokens = []
    
    # We need to handle multi-token entities properly if they appear, 
    # but Few-NERD in this format often has individual tags per token.
    # The example provided "Hicks (Person)" suggests we annotate each token that has the tag.
    
    for token, tag_id in zip(tokens, tags):
        if tag_id != 0: # 0 is usually 'O'
            label_name = label_names[tag_id]
            # Updated format: Token #Label#
            annotated_tokens.append(f"{token} #{label_name}#")
        else:
            annotated_tokens.append(token)
    
    return " ".join(annotated_tokens)

def collect_examples(ds, label_feature_name, num_examples=3):
    label_names = ds.features[label_feature_name].feature.names
    examples_dict = {}
    
    # Initialize dictionary for all labels except 'O'
    for name in label_names:
        if name != 'O':
            examples_dict[name] = []
            
    # Iterate through the dataset to find examples
    # We use a set to keep track of labels that reached the limit to stop early
    completed_labels = set()
    total_labels_to_find = len(examples_dict)
    
    print(f"Searching for examples for {label_feature_name}...")
    
    for i in tqdm(range(len(ds))):
        if len(completed_labels) == total_labels_to_find:
            break
            
        item = ds[i]
        tokens = item['tokens']
        tags = item[label_feature_name]
        
        # Find which non-'O' labels are in this sentence
        present_tags = set(tags)
        if 0 in present_tags:
            present_tags.remove(0)
            
        for tag_id in present_tags:
            label_name = label_names[tag_id]
            if len(examples_dict[label_name]) < num_examples:
                # Format the sentence
                formatted = format_sentence(tokens, tags, label_names)
                # Check if this sentence is already added for this label to avoid duplicates
                if formatted not in examples_dict[label_name]:
                    examples_dict[label_name].append(formatted)
                    
                    if len(examples_dict[label_name]) == num_examples:
                        completed_labels.add(label_name)
                        
    return examples_dict

def main():
    train_path = './few-nerd_train'
    if not os.path.exists(train_path):
        print(f"Error: {train_path} not found.")
        return

    print("Loading dataset...")
    ds = load_from_disk(train_path)
    
    # Coarse Labels
    coarse_examples = collect_examples(ds, 'ner_tags')
    with open('coarse_labels_examples.json', 'w') as f:
        json.dump(coarse_examples, f, indent=2)
    print("Saved coarse_labels_examples.json")
    
    # Fine Labels
    fine_examples = collect_examples(ds, 'fine_ner_tags')
    with open('fine_labels_examples.json', 'w') as f:
        json.dump(fine_examples, f, indent=2)
    print("Saved fine_labels_examples.json")

if __name__ == "__main__":
    main()
