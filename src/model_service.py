from pathlib import Path
import json

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent


class FraudModelService:
    def __init__(self):
        self.model = joblib.load(
            BASE_DIR / "models" / "fraud_model.pkl"
        )

        with open(
            BASE_DIR / "configs" / "model_config.json",
            "r"
        ) as f:
            config = json.load(f)

        self.features = config["features"]
        self.threshold = config["threshold"]

    def predict(self, transaction: dict[str, float]) -> dict:
        input_df = pd.DataFrame(
            [[transaction[feature] for feature in self.features]],
            columns=self.features
        )

        fraud_probability = float(
            self.model.predict_proba(input_df)[0, 1]
        )

        prediction = int(
            fraud_probability >= self.threshold
        )

        decision = "FLAG" if prediction == 1 else "ALLOW"

        return {
            "fraud_probability": fraud_probability,
            "threshold": self.threshold,
            "prediction": prediction,
            "decision": decision
        }