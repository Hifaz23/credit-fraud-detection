# Fraud Detection Service Runbook

## Start the API Locally

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Start the API:

```powershell
uvicorn src.app:app --host 127.0.0.1 --port 8000
```

Verify the service:

```text
GET http://127.0.0.1:8000/
```

Expected response:

```json
{
  "message": "Fraud Detection API is running"
}
```

## Run Automated Tests

```powershell
python -m pytest tests -q
```

Expected result:

```text
24 passed
```

## MLflow UI

Start MLflow:

```powershell
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

Open:

```text
http://127.0.0.1:5000
```

Main experiment:

```text
credit-card-fraud-detection
```

Registered model:

```text
fraud-detection-model
```

Current alias:

```text
champion
```

## CI Failure Investigation

If GitHub Actions CI fails:

1. Open the failed workflow in GitHub Actions.
2. Identify the failed step.
3. Inspect the step logs.
4. Reproduce the failure locally.
5. Run:

```powershell
python -m pytest tests -q
```

6. Fix the issue.
7. Commit and push the correction.
8. Confirm CI returns to green.

## API Validation Errors

HTTP `422` usually means the request schema is invalid.

Check for:

- missing features
- non-numeric values
- unexpected extra fields

## Internal Prediction Errors

HTTP `500` indicates an unexpected internal application failure.

Check application logs for:

```text
event=prediction_failed
```

The internal traceback is logged but is not returned to the client.

## Model Loading Issues

If the model fails to load:

1. Confirm `models/fraud_model.pkl` exists.
2. Confirm `configs/model_config.json` exists.
3. Confirm the feature count is 30.
4. Check the XGBoost version.

The current historical model may produce an XGBoost serialization compatibility warning because it originated from an older environment.

## Database Issues

The API uses:

```text
fraud_predictions.db
```

This SQLite database is created locally at runtime and is not stored in Git.

If the database does not exist, the application initialization creates the required table.

## Deployment Validation

Open:

```text
GitHub Actions → Fraud Detection Deployment
```

Trigger the workflow manually from `main`.

A successful workflow confirms:

- Docker image builds
- container starts
- FastAPI loads
- port mapping works
- HTTP health check succeeds

## Rollback Concept

If a newer registered model version performs poorly, move the `champion` alias back to the previous approved version.

For example:

```text
champion → Version 1
```

This allows the approved model reference to change without changing the application model URI.