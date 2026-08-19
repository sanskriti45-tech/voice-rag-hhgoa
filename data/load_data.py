from datasets import load_dataset
import pandas as pd

print("Loading dataset (streaming)...")

dataset = load_dataset(
    "ai4bharat/MSMARCO-XI",
    data_files={"validation": "validation/hinval.parquet"},
    streaming=True,
)

print("Pulling a slice into memory...")

N = 2000  # adjust based on how much you want to index
rows = []
for i, example in enumerate(dataset["validation"]):
    if i >= N:
        break
    rows.append(example)

df = pd.DataFrame(rows)
print(f"\nSlice shape: {df.shape}")
print(df.iloc[0]["passages"])

df.to_pickle("data/msmarco_slice.pkl")
print("\nSaved slice to data/msmarco_slice.pkl")