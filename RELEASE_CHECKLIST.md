# Fraud Detection Release Checklist

Use this checklist before approving a new production release.

## Code and Tests

- [ ] Working tree is clean.
- [ ] All intended changes are committed.
- [ ] `python -m pytest tests -q` passes.
- [ ] API validation tests pass.
- [ ] ML/data/model validation tests pass.
- [ ] Error-handling tests pass.

## Model

- [ ] Correct model artifact is present.
- [ ] `model_config.json` matches the model.
- [ ] Expected feature count is 30.
- [ ] Classification threshold is verified.
- [ ] Registered MLflow model version is correct.
- [ ] `champion` alias points to the approved model version.
- [ ] Model lineage is available for the approved version.

## MLflow

- [ ] Parameters are recorded.
- [ ] Metrics are recorded.
- [ ] Model/config artifacts are available.
- [ ] Dependency/environment information is available.
- [ ] Reproducibility limitations are documented.

## API

- [ ] FastAPI application starts successfully.
- [ ] `GET /` health endpoint responds successfully.
- [ ] `POST /predict` returns the expected response structure.
- [ ] Missing/invalid fields return meaningful `422` responses.
- [ ] Internal failures return controlled `500` responses.
- [ ] Internal tracebacks are not exposed to clients.

## Logging and Storage

- [ ] Prediction request/completion events are logged.
- [ ] Prediction failures are logged with exception details.
- [ ] SQLite prediction storage works.
- [ ] Local runtime databases are not committed to Git.

## Security and Configuration

- [ ] No passwords, tokens, API keys, or credentials are committed.
- [ ] `.env` and secret files are ignored by Git.
- [ ] Local datasets and runtime state are ignored.
- [ ] Configuration files contain no sensitive values.

## CI

- [ ] GitHub Actions CI is green.
- [ ] CI runs automatically on pushes to `main`.
- [ ] CI runs on pull requests targeting `main`.
- [ ] Docker image builds successfully in CI.
- [ ] A deliberate defect has previously been confirmed to make CI fail.

## Deployment Validation

- [ ] Deployment workflow is triggered from the intended branch.
- [ ] Docker image builds successfully.
- [ ] Container starts successfully.
- [ ] FastAPI health check succeeds.
- [ ] Container cleanup succeeds.
- [ ] Deployment workflow finishes green.

## Documentation

- [ ] `README.md` is up to date.
- [ ] `RUNBOOK.md` is up to date.
- [ ] Known limitations are documented.
- [ ] Reproducibility limitations are documented.

## Final Approval

- [ ] CI is green.
- [ ] Deployment validation is green.
- [ ] Approved MLflow model/version is confirmed.
- [ ] No unresolved critical issues remain.
- [ ] Release is ready for approval.