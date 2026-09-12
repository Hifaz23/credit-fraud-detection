from pathlib import Path

import mlflow
import mlflow.xgboost
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

mlflow.set_tracking_uri(
    f"sqlite:///{BASE_DIR / 'mlflow.db'}"
)

MODEL_URI = "models:/fraud-detection-model@champion"

model = mlflow.xgboost.load_model(MODEL_URI)

sample = pd.read_csv(
    BASE_DIR / "creditcard.csv",
    nrows=1
)

features = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]

X_sample = sample[features]

probability = model.predict_proba(X_sample)[0, 1]

print("Loaded from:", MODEL_URI)
print("Model type:", type(model).__name__)
print("Fraud probability:", probability)