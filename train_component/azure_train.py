import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--data", type=str, required=True)
parser.add_argument("--predictions", type=str, required=True)
parser.add_argument("--model_output", type=str, required=True)
args = parser.parse_args()

df = pd.read_csv(args.data)

X = df.drop(columns=["Class"])
y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000)
)

model.fit(X_train, y_train)

import joblib
import os

os.makedirs(args.model_output, exist_ok=True)

joblib.dump(
    model,
    os.path.join(args.model_output, "fraud_lr_model.pkl")
)

preds = model.predict(X_test)

import os

os.makedirs(args.predictions, exist_ok=True)

results = pd.DataFrame({
    "actual": y_test.values,
    "predicted": preds
})

results.to_csv(
    os.path.join(args.predictions, "predictions.csv"),
    index=False
)

print("Training complete")
print("Accuracy:", accuracy_score(y_test, preds))
print("Precision:", precision_score(y_test, preds, zero_division=0))
print("Recall:", recall_score(y_test, preds, zero_division=0))
print("F1:", f1_score(y_test, preds, zero_division=0))