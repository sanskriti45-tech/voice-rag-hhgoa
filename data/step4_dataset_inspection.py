import pandas as pd
import numpy as np
from datasets import load_dataset
LANGUAGE = "hi"

dataset = load_dataset("ai4bharat/MSMARCO-XI", LANGUAGE, split="train")

print(f"Train split size: {len(dataset)} rows")
print("Column names:", dataset.column_names)

N = 5000
df = dataset.select(range(min(N, len(dataset)))).to_pandas()

print("\n--- Shape ---")
print(df.shape)

print("\n--- dtypes ---")
print(df.dtypes)

print("\n--- Head ---")
print(df.head(3))

sample_passages = df.iloc[0]["passages"]
print("\n--- Sample 'passages' structure ---")
print(type(sample_passages), sample_passages.keys() if hasattr(sample_passages, "keys") else "n/a")

print("\n--- Null counts ---")
print(df.isnull().sum())

all_lengths = []
for passages in df["passages"]:
    field = "Translated_passages" if LANGUAGE != "en" else "English_passages"
    for text in passages[field]:
        all_lengths.append(len(text.split()))

all_lengths = np.array(all_lengths)
print("\n--- Passage length stats (words) ---")
print(f"mean: {all_lengths.mean():.1f}")
print(f"median: {np.median(all_lengths):.1f}")
print(f"max: {all_lengths.max()}")
print(f"min: {all_lengths.min()}")