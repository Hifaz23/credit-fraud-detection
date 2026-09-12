# Credit Card Fraud Detection — Production ML System

A production-oriented fraud detection system built around an XGBoost classifier and extended with API serving, validation, testing, experiment tracking, model registry, Docker, CI, and deployment validation.

## Project Overview

The model predicts whether a credit-card transaction should be flagged as fraudulent.

The original model was developed using the Kaggle Credit Card Fraud Detection dataset containing highly imbalanced transaction data.

Main production components:

- XGBoost fraud classifier
- FastAPI prediction API
- Pydantic request/response validation
- SQLite prediction logging
- Automated pytest test suite
- ML/data/model validation tests
- MLflow experiment tracking
- MLflow Model Registry
- Docker containerization
- GitHub Actions CI
- Deployment validation workflow

## Project Structure

```text
.
├── configs/
│   └── model_config.json
├── models/
│   └── fraud_model.pkl
├── notebooks/
├── scripts/
├── src/
│   ├── app.py
│   ├── database.py
│   ├── logging_config.py
│   ├── model_service.py
│   └── schemas.py
├── tests/
│   ├── fixtures/
│   ├── test_api.py
│   ├── test_database.py
│   ├── test_ml_validation.py
│   └── test_model_service.py
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── requirements-lock.txt
└── README.md
```

## Local Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

## Run the API

Start the FastAPI application:

```bash
uvicorn src.app:app --host 127.0.0.1 --port 8000
```

Health endpoint:

```text
GET /
```

Prediction endpoint:

```text
POST /predict
```

The prediction request expects 30 numerical features:

- Time
- V1 through V28
- Amount

The API returns:

- fraud probability
- classification threshold
- binary prediction
- ALLOW or FLAG decision

## Testing

Run the full automated test suite:

```bash
python -m pytest tests -q
```

The project currently contains 24 automated tests covering:

- API behavior
- request validation
- error handling
- model service behavior
- database operations
- dataset/schema validation
- model/config compatibility

A lightweight dataset fixture is stored under `tests/fixtures/` so CI does not depend on the full local dataset.

## MLflow Experiment Tracking

The project uses MLflow to track:

- parameters
- metrics
- model artifacts
- configuration artifacts
- dependency/environment information

MLflow experiment:

```text
credit-card-fraud-detection
```

Tracked run:

```text
xgboost-production-model
```

The tracked run includes:

- model type
- threshold
- feature count
- Precision
- Recall
- F1 score
- PR-AUC
- trained model artifact
- configuration artifact
- requirements lockfile

## MLflow Model Registry

Registered model:

```text
fraud-detection-model
```

The current approved model version is referenced using the alias:

```text
champion
```

The model can be loaded using:

```text
models:/fraud-detection-model@champion
```

Using an alias avoids hardcoding a specific version number and allows the approved model version to change without changing the application URI.

## Model Lineage

MLflow model lineage allows a registered model version to be traced back to the source MLflow run that produced it.

This provides visibility into:

- source run
- parameters
- metrics
- model artifacts
- configuration
- environment information

This improves debugging, auditing, and model-version traceability.

## Continuous Integration

GitHub Actions runs automatically on:

- pushes to `main`
- pull requests targeting `main`

The CI workflow:

1. checks out the repository
2. installs Python
3. installs project and test dependencies
4. runs the automated test suite
5. verifies that the Docker image builds successfully

The CI pipeline was validated by deliberately introducing a defect.

The workflow correctly changed from:

```text
Green ✅
Red ❌
Green ✅
```

after:

1. confirming the original code passed
2. introducing an API response defect
3. observing CI failure
4. fixing the defect
5. confirming CI passed again

## Docker

The project contains a Dockerfile that packages the FastAPI application and its required production files.

The Docker image contains:

- application source code
- trained model
- model configuration
- runtime dependencies

The Docker image is built automatically inside GitHub Actions CI to verify that the project remains container-buildable after code changes.

## Deployment Workflow

A separate GitHub Actions deployment workflow is stored in:

```text
.github/workflows/deploy.yml
```

The deployment workflow is manually triggered using `workflow_dispatch`.

It performs the following steps:

1. checks out the repository
2. builds the production Docker image
3. starts a Docker container
4. maps the API port
5. performs an HTTP health check
6. verifies that the running FastAPI application responds
7. displays container status
8. cleans up the temporary container

The deployment validation workflow currently passes successfully.

Because deployment requires a manual trigger, the current setup is closer to Continuous Delivery than fully automated Continuous Deployment.

## API Validation

Pydantic is used to validate incoming prediction requests.

The API validates:

- required features
- numerical input types
- unexpected extra fields

Invalid schema requests return meaningful HTTP `422` responses before reaching the prediction logic.

Unexpected internal prediction errors are logged and return a controlled HTTP `500` response rather than exposing internal implementation details.

## Logging and Error Handling

The application uses centralized logging.

Prediction requests record events such as:

```text
event=prediction_request_received
```

Successful predictions record:

```text
event=prediction_completed
```

Unexpected failures are logged using exception logging:

```text
event=prediction_failed
```

This allows failures to be investigated without exposing internal tracebacks to API clients.

## Local Runtime Storage

Prediction results are stored locally using SQLite.

The database records:

- transaction data
- fraud probability
- prediction
- decision
- timestamp

The SQLite database is runtime state and is therefore excluded from Git.

## Git Ignore Policy

The following local/runtime files are intentionally excluded from version control:

- `.venv/`
- `creditcard.csv`
- `fraud_predictions.db`
- `mlflow.db`
- `mlruns/`
- `.env`
- secret/key files
- Python cache files

This prevents large local data, runtime state, virtual environments, and sensitive configuration from being committed.

## Dependency Files

The project uses three dependency files.

### `requirements.txt`

Contains runtime dependencies required to run the application.

### `requirements-dev.txt`

Contains runtime requirements plus development/testing dependencies such as:

- pytest
- httpx

### `requirements-lock.txt`

Contains the package versions installed in the current Phase 6 environment for improved traceability and reproducibility.

## Reproducibility Note

The fraud model was originally trained before MLflow tracking and environment locking were added.

The current MLflow run provides strong traceability through:

- model artifact
- configuration
- parameters
- metrics
- current dependency lockfile

However, the run should not be considered a perfect reconstruction of the original training environment.

The exact original package versions, complete training execution, and all historical training conditions were not captured when the original model was trained.

For full reproducibility, future training runs should capture:

- exact dataset version
- preprocessing code
- training code
- model hyperparameters
- random seeds
- dependency versions
- evaluation logic
- model artifacts

## Known Limitations

- The historical model-training environment was not fully preserved.
- SQLite is used as local runtime storage instead of a managed production database.
- The deployment workflow validates the application inside GitHub Actions but does not deploy to a persistent cloud service.
- Monitoring currently relies on previously implemented drift and performance analysis rather than a continuously running monitoring platform.
- The current model artifact originated from an older XGBoost environment and produces a compatibility warning when loaded in the newer environment.
- This project is an educational productionization workflow and should not be used as a real financial decision system without additional security, monitoring, governance, compliance, and business validation.