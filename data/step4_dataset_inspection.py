import pandas as pd
import numpy as np
from datasets import load_dataset

LANGUAGE = "hi"

print("Loading dataset (streaming)...")

dataset = load_dataset(
    "ai4bharat/MSMARCO-XI",
    data_files={"validation": "validation/hinval.parquet"},
    streaming=True,
)

print("Pulling a slice into memory...")

N = 2000
rows = []
for i, example in enumerate(dataset["validation"]):
    if i >= N:
        break
    rows.append(example)

df = pd.DataFrame(rows)
print(f"\nSlice shape: {df.shape}")
print("Column names:", df.columns.tolist())

sample_passages = df.iloc[0]["passages"]
print("\n--- Sample 'passages' structure ---")
print(type(sample_passages), sample_passages.keys() if hasattr(sample_passages, "keys") else "n/a")
print("Num English passages:", len(sample_passages["English_passages"]))
print("Num Translated passages:", len(sample_passages["Translated_passages"]))

print("\n--- Null counts ---")
print(df.isnull().sum())

all_lengths = []
for passages in df["passages"]:
    for text in passages["Translated_passages"]:
        all_lengths.append(len(text.split()))

all_lengths = np.array(all_lengths)
print("\n--- Passage length stats (Translated_passages, words) ---")
print(f"mean: {all_lengths.mean():.1f}")
print(f"median: {np.median(all_lengths):.1f}")
print(f"max: {all_lengths.max()}")
print(f"min: {all_lengths.min()}")

df.to_pickle("data/msmarco_slice.pkl")
print("\nSaved slice to data/msmarco_slice.pkl")