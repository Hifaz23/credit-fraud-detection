@"
# G9 Azure MLOps Scrum Backlog

## Sprint Goal

Build and document a reproducible fraud-detection MLOps workflow covering data, training, evaluation, model versioning, monitoring, retraining, and governance.

## User Story 1 - Cloud Data Storage

As a data scientist,
I want fraud sample data stored in Azure Blob Storage,
so that Azure ML jobs can access a reproducible cloud data source.

### Acceptance Criteria
- Azure Storage account exists.
- Private Blob container exists.
- Fraud sample dataset is uploaded.
- Dataset can be referenced from Azure ML.

---

## User Story 2 - Reproducible Training

As a data scientist,
I want the fraud model training process to run as an Azure ML job,
so that training can be reproduced outside my local machine.

### Acceptance Criteria
- Training script accepts the dataset path as an argument.
- Azure ML training job completes successfully.
- Training environment and compute are recorded.
- Model evaluation metrics are produced.

---

## User Story 3 - ML Pipeline

As an ML engineer,
I want training and evaluation separated into reusable pipeline components,
so that the workflow can be executed consistently and independently.

### Acceptance Criteria
- Train component is registered.
- Evaluate component is registered.
- Training output is passed to evaluation as an artifact.
- Azure ML pipeline completes successfully.

---

## User Story 4 - Model Governance

As an ML engineer,
I want trained models stored with versions,
so that candidates can be compared and previous models can be restored.

### Acceptance Criteria
- Model is registered in Azure ML.
- At least two model versions exist.
- Candidate and champion concepts are documented.
- Rollback to an older approved version is possible.

---

## User Story 5 - Production Monitoring and Retraining

As an ML operations engineer,
I want drift, model performance, and service health monitored,
so that degradation can be detected and retraining decisions can be made safely.

### Acceptance Criteria
- Input drift monitoring is defined.
- Model performance monitoring is defined.
- Service-health metrics are identified.
- Retraining triggers are documented.
- Candidate validation gate is defined.
- Rollback policy is documented.

## Sprint Definition of Done

The sprint is complete when the required artifacts are created, practical outputs are validated, and the documented acceptance criteria are satisfied.
"@ | Set-Content .\docs\scrum_backlog.md