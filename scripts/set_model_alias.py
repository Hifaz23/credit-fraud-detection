from pathlib import Path

import mlflow
from mlflow import MlflowClient


BASE_DIR = Path(__file__).resolve().parent.parent

mlflow.set_tracking_uri(
    f"sqlite:///{BASE_DIR / 'mlflow.db'}"
)

client = MlflowClient()#helps to communicate the mlflow server 

MODEL_NAME = "fraud-detection-model"
ALIAS = "champion"
VERSION = "1"

client.set_registered_model_alias(
    MODEL_NAME,
    ALIAS,
    VERSION
)

model_version = client.get_model_version_by_alias(
    MODEL_NAME,
    ALIAS
)

print("Alias:", ALIAS)
print("Points to version:", model_version.version)
