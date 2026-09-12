#Load our existing trained XGBoost model, attach an example of its 30-feature input schema, and register it as Version 1 under a stable model name.
from pathlib import Path
import json

import joblib
import mlflow
import mlflow.xgboost
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

RUN_ID = "fdc7daf0068748cca0ffc9d212a61908"

MODEL_PATH = BASE_DIR / "models" / "fraud_model.pkl"
CONFIG_PATH = BASE_DIR / "configs" / "model_config.json"
DATA_PATH = BASE_DIR / "creditcard.csv"


model = joblib.load(MODEL_PATH)

with open(CONFIG_PATH, "r") as file:
    config = json.load(file)

features = config["features"]

input_example = pd.read_csv(
    DATA_PATH,
    nrows=1
)[features]


mlflow.set_tracking_uri(
    f"sqlite:///{BASE_DIR / 'mlflow.db'}"
)


with mlflow.start_run(run_id=RUN_ID):

    model_info = mlflow.xgboost.log_model(
        xgb_model=model,
        name="fraud_xgboost_model",
        model_format="json",
        input_example=input_example,
        registered_model_name="fraud-detection-model",
    )


print("Registered model successfully")
print("Model URI:", model_info.model_uri)