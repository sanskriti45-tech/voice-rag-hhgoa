from datasets import load_dataset

print("Loading dataset...")

# Load Hindi training data
dataset = load_dataset("ai4bharat/MSMARCO-XI", "hi", split="train")

print("Dataset loaded!")

# Access the data
for example in dataset:
    print(f"Query: {example['query']}")
    print(f"Answers: {example['Answer']}")
    print(f"Passages: {len(example['passages'])}")
    break