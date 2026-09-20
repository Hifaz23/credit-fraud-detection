# G9 Fraud ML System Design

## Goal

Design a production-oriented fraud detection system that supports:

- real-time transaction scoring
- offline training and evaluation
- model versioning
- monitoring
- retraining
- rollback

---

## Real-Time Inference Path

Transaction
-> FastAPI /predict
-> Pydantic input validation
-> feature preparation
-> fraud model
-> fraud probability
-> decision threshold
-> ALLOW / FLAG
-> prediction logging / storage

This path prioritizes low latency because transaction decisions may be time-sensitive.

---

## Offline ML Path

Historical + newly labeled transactions
-> data validation
-> feature preparation
-> training
-> evaluation
-> candidate/champion comparison
-> model registry
-> approved model version

The offline path prioritizes reproducibility and model quality rather than immediate response time.

---

## System Architecture

~~~mermaid
flowchart LR

    A[Incoming Transaction] --> B[FastAPI /predict]
    B --> C[Input Validation]
    C --> D[Feature Processing]
    D --> E[Production Fraud Model]
    E --> F[Fraud Probability]
    F --> G[Decision Threshold]
    G --> H[ALLOW / FLAG]
    H --> I[Prediction Database / Logs]

    I --> J[Monitoring]

    J --> K[Drift / Performance / Service Health]
    K --> L[Retraining Investigation]

    M[Historical + Labeled Data] --> N[Training Pipeline]
    L --> N

    N --> O[Evaluation]
    O --> P[Validation Gate]
    P --> Q[Azure ML Model Registry]
    Q --> E
~~~

---

## Online vs Batch

### Online Inference

Used for individual transactions requiring an immediate fraud decision.

Primary concerns:

- low latency
- availability
- request validation
- throughput
- service reliability

### Batch Processing

Useful for:

- historical rescoring
- investigation datasets
- monitoring calculations
- large offline evaluations
- retraining-data preparation

Batch processing tolerates higher latency and focuses more on throughput.

---

## Feature / Data Pipeline

Training and serving should apply compatible feature-processing logic.

Important controls include:

- schema validation
- missing-value handling
- data-type validation
- feature ordering
- preprocessing consistency
- versioned training data where practical

Training-serving skew should be avoided.

---

## Monitoring Layer

### Data Monitoring

- feature PSI
- unusual missing values
- schema changes
- data-quality failures

### Prediction / Model Monitoring

- prediction PSI
- Precision
- Recall
- F1
- PR-AUC
- chronological performance changes

### Service Monitoring

- average latency
- P95 latency
- throughput
- HTTP errors
- failed predictions
- availability

---

## Retraining Path

Monitor
-> investigate
-> obtain sufficient labeled data
-> train candidate
-> evaluate
-> compare with champion
-> validation gate
-> register / promote approved version
-> monitor

The previous approved model should remain available for rollback.

---

## Key Trade-Offs

### Latency vs Throughput

Very low single-request latency does not guarantee that the service can handle high traffic.

### Real-Time vs Batch

Real-time inference provides immediate decisions but requires more operational infrastructure.

Batch inference is simpler for large offline workloads but cannot provide immediate transaction decisions.

### Model Complexity vs Serving Speed

A more complex model may improve predictive performance but increase latency and compute requirements.

### Fraud Recall vs Customer Friction

Lowering the decision threshold may catch more fraud but can increase false positives and inconvenience legitimate customers.

### Freshness vs Stability

Frequent retraining can adapt to new fraud patterns but may introduce unstable or poorly validated models.

### Cost vs Scalability

More compute and always-on services can improve capacity and availability but increase cloud cost.

---

## Current Implementation

Implemented:

- XGBoost fraud model
- FastAPI online prediction endpoint
- Pydantic validation
- Docker support
- SQLite prediction persistence
- latency and throughput benchmarking
- PSI drift monitoring
- chronological performance monitoring
- Azure ML training demonstration
- Azure ML Train -> Evaluate pipeline
- Azure ML model registry versions
- retraining policy
- rollback design

Not claimed as implemented:

- Azure Managed Online Endpoint
- continuously running enterprise monitoring platform

---

## Design Principle

The production system should balance:

model quality,
latency,
throughput,
reliability,
security,
cost,
monitoring,
and maintainability.

The best ML model alone is not enough; the complete system must operate reliably around it.