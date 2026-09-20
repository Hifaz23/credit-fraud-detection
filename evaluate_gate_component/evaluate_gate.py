import argparse
import os
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

parser = argparse.ArgumentParser()
parser.add_argument("--predictions", required=True)
args = parser.parse_args()

pred_path = os.path.join(args.predictions, "predictions.csv")
df = pd.read_csv(pred_path)

precision = precision_score(df["actual"], df["predicted"], zero_division=0)
recall = recall_score(df["actual"], df["predicted"], zero_division=0)
f1 = f1_score(df["actual"], df["predicted"], zero_division=0)

print("Precision:", precision)
print("Recall:", recall)
print("F1:", f1)

# G9 demo acceptance gate
MIN_RECALL = 0.40
MIN_F1 = 0.60

if recall < MIN_RECALL or f1 < MIN_F1:
    raise RuntimeError(
        f"Model rejected: recall={recall:.4f}, f1={f1:.4f}"
    )

print("VALIDATION PASSED")
print("Candidate is eligible for registration.")