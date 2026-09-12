from pathlib import Path

import mlflow


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "fraud_model.pkl"
CONFIG_PATH = BASE_DIR / "configs" / "model_config.json"


mlflow.set_tracking_uri(#sets tracking metedata to be stored in the database sqlite
    f"sqlite:///{BASE_DIR / 'mlflow.db'}"
)

mlflow.set_experiment(#groups related runs under one experiment 
    "credit-card-fraud-detection"
)


with mlflow.start_run(run_name="xgboost-production-model"):#creates one specific experiment run.

    mlflow.log_param("model_type", "XGBoost")#stores configuration/settings
    mlflow.log_param("threshold", 0.79)
    mlflow.log_param("feature_count", 30)

    mlflow.log_metric("precision", 0.8730)#stores numerical performance results.
    mlflow.log_metric("recall", 0.7333)
    mlflow.log_metric("f1", 0.7971)
    mlflow.log_metric("pr_auc", 0.7928)

    mlflow.log_artifact(#stores associated files such as the trained model and config.
        str(MODEL_PATH),
        artifact_path="model"
    )

    mlflow.log_artifact(
        str(CONFIG_PATH),
        artifact_path="config"
    )

    print("MLflow run logged successfully")