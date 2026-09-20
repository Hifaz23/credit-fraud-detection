import argparse
import os
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

parser = argparse.ArgumentParser()
parser.add_argument("--predictions", type=str, required=True)
args = parser.parse_args()

file_path = os.path.join(args.predictions, "predictions.csv")
df = pd.read_csv(file_path)

accuracy = accuracy_score(df["actual"], df["predicted"])
precision = precision_score(df["actual"], df["predicted"], zero_division=0)
recall = recall_score(df["actual"], df["predicted"], zero_division=0)
f1 = f1_score(df["actual"], df["predicted"], zero_division=0)

print("Evaluation complete")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1:", f1)