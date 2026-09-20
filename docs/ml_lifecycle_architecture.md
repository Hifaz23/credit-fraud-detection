# G9 Fraud ML Lifecycle Architecture

## End-to-End Lifecycle

~~~mermaid
flowchart LR
    A[Scope: Real-time Fraud Detection]
    B[Data: Credit Card Transactions]
    C[Storage: Azure Blob / Local Dataset]
    D[Features: Time, Amount, V1-V28]
    E[Training: XGBoost / Azure LR Demo]
    F[Evaluation: Precision, Recall, F1, PR-AUC]
    G[Azure ML Model Registry]
    H[Serving: FastAPI /predict + Docker]
    I[Monitoring: PSI + Performance + Service Health]
    J[Retraining Investigation]
    K[Candidate Validation Gate]
    L[Promote New Version or Keep Champion]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> E
    F --> K
    K --> L
    L --> G
~~~

## Inner Loop

The inner loop covers model development:

Data -> Features -> Train -> Evaluate -> Improve

Activities include:
- data preparation
- feature processing
- model training
- hyperparameter changes
- metric comparison
- error analysis

## Outer Loop

The outer loop covers production ML operations:

Register -> Deploy -> Monitor -> Detect degradation -> Retrain -> Validate -> Register new version -> Redeploy

Activities include:
- model versioning
- deployment
- service monitoring
- drift monitoring
- performance monitoring
- retraining triggers
- validation gates
- rollback

## Actual G9 / Fraud Components

### Scope
Detect fraudulent card transactions and return an ALLOW/FLAG decision.

### Data
Credit Card Fraud dataset.
A small sample is stored in Azure Blob Storage for G9 Azure experimentation.

### Training
- Main project: XGBoost fraud model.
- G9 Azure demonstration: Logistic Regression training job.

### Evaluation
Metrics include:
- Precision
- Recall
- F1
- PR-AUC

The Azure ML pipeline currently contains separate Train and Evaluate components.

### Registry
Azure ML model: fraud-lr-azure-demo

Registered versions:
- Version 1
- Version 2

### Deployment
The implemented serving layer is the existing FastAPI /predict endpoint with Docker support.

An Azure Managed Online Endpoint has not been deployed in this project.

### Monitoring
Existing monitoring includes:
- feature PSI
- prediction PSI
- chronological performance windows
- average and P95 latency
- throughput
- error/service-health concepts

### Retraining
A hybrid retraining policy is used:
- scheduled model evaluation
- trigger-based investigation
- sufficient labeled data
- candidate vs champion validation
- promotion only after validation
- rollback to previous approved version when required

## Important Principle

The ML lifecycle does not end after model training.

A production ML system must continue through:

Evaluation -> Registration -> Deployment -> Monitoring -> Retraining / Rollback
