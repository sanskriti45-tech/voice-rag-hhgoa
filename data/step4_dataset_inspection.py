import pandas as pd
import numpy as np
from datasets import load_dataset
dataset = load_dataset("microsoft/ms_marco", "v1.1")

print("Available splits:", list(dataset.keys()))

train = dataset["train"]
print(f"\nTrain split size: {len(train)} rows")
print("Column names:", train.column_names)
N = 5000
df = train.select(range(N)).to_pandas()

print("\n--- Shape ---")
print(df.shape)

print("\n--- dtypes ---")
print(df.dtypes)

print("\n--- Head ---")
print(df.head(3))

sample_passages = df.iloc[0]["passages"]
print("\n--- Sample 'passages' structure ---")
print(type(sample_passages), sample_passages.keys() if hasattr(sample_passages, "keys") else "n/a")
print("Num passages in this example:", len(sample_passages["passage_text"]))

print("\n--- Null counts ---")
print(df.isnull().sum())

print("\n--- Query type distribution ---")
if "query_type" in df.columns:
    print(df["query_type"].value_counts())

all_lengths = []
for passages in df["passages"]:
    for text in passages["passage_text"]:
        all_lengths.append(len(text.split()))

all_lengths = np.array(all_lengths)
print("\n--- Passage length stats (words) ---")
print(f"mean: {all_lengths.mean():.1f}")
print(f"median: {np.median(all_lengths):.1f}")
print(f"max: {all_lengths.max()}")
print(f"min: {all_lengths.min()}")

df.to_pickle("msmarco_slice.pkl")
print("\nSaved slice to msmarco_slice.pkl for use in Step 5.")
