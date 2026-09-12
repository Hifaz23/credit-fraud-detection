from pathlib import Path

import mlflow
from mlflow.tracking import MlflowClient


BASE_DIR = Path(__file__).resolve().parent.parent

mlflow.set_tracking_uri(
    f"sqlite:///{BASE_DIR / 'mlflow.db'}"
)

experiment = mlflow.get_experiment_by_name(
    "credit-card-fraud-detection"
)

runs = mlflow.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["start_time DESC"],
    max_results=1
)

run_id = runs.iloc[0]["run_id"]

client = MlflowClient()

client.log_artifact(
    run_id,
    str(BASE_DIR / "requirements-lock.txt"),
    artifact_path="environment"
)

print("Lockfile attached to run:", run_id)