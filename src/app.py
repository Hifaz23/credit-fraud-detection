from fastapi import FastAPI, HTTPException

from src.database import initialize_database, save_prediction
from src.model_service import FraudModelService
from src.schemas import TransactionInput, PredictionResponse
import logging

from src.logging_config import configure_logging

configure_logging()#sets common logging format
logger = logging.getLogger(__name__)#creates logger named "src.app"

app = FastAPI(title="Real-Time Fraud Detection API")

model_service = FraudModelService()
initialize_database()


@app.get("/")
def home():
    return {"message": "BROKEN API"}


@app.post("/predict", response_model=PredictionResponse)
def predict(transaction: TransactionInput):

    logger.info("event=prediction_request_received")

    transaction_dict = transaction.model_dump()

    try:
        result = model_service.predict(transaction_dict)

        save_prediction(
            transaction=transaction_dict,
            fraud_probability=result["fraud_probability"],
            prediction=result["prediction"],
            decision=result["decision"]
        )

    except Exception:
        logger.exception(
            "event=prediction_failed"
        )

        raise HTTPException(
            status_code=500,
            detail="Prediction service failed"
        )

    logger.info(
        "event=prediction_completed decision=%s probability=%.6f",
        result["decision"],
        result["fraud_probability"]
    )

    return result