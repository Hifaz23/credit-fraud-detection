# Fraud Detection Model Card

## Model Overview

Purpose:
Detect potentially fraudulent credit-card transactions and support real-time fraud screening.

Primary use:
Generate a fraud probability and an ALLOW / FLAG decision for incoming transactions.

The model should support fraud investigation and risk screening rather than being treated as an unquestionable final decision-maker.

---

## Model and Data

Main fraud model:
XGBoost classifier.

Data:
Credit Card Fraud dataset containing:
- Time
- Amount
- V1-V28 anonymized features
- Fraud label

The dataset is highly imbalanced because fraudulent transactions are rare.

---

## Evaluation

Important evaluation metrics include:

- Precision
- Recall
- F1-score
- PR-AUC

Project test results included approximately:

- Precision: 87.69%
- Recall: 76.0%
- F1-score: 81.43%
- PR-AUC: 0.786

Accuracy alone should not be used because the fraud class is extremely rare.

---

## Intended Use

The model may be used to:

- identify suspicious transactions
- prioritize transactions for investigation
- provide fraud-risk scores
- support real-time fraud screening

The model should be combined with business rules and human review where the consequences of an incorrect decision are significant.

---

## Human Oversight

A FLAG prediction should not automatically be treated as proof of fraud.

High-risk transactions may require:
- fraud analyst review
- additional customer verification
- business-rule checks
- contextual investigation

Human reviewers should be able to override model decisions when appropriate.

---

## Bias and Fairness

The available dataset uses anonymized V1-V28 features.

Meaningful demographic attributes such as age, gender, ethnicity, or other protected characteristics are not available.

Therefore:

- demographic fairness cannot be fully evaluated using this dataset
- absence of protected attributes does not prove the model is unbiased
- production systems should perform fairness analysis when relevant attributes and legal permissions are available

Fairness analysis should compare error rates such as false-positive and false-negative rates across relevant groups when appropriate.

---

## Explainability

Model predictions should be explainable where practical.

Possible techniques include:

- feature importance
- SHAP values
- local explanations for individual transactions

Explainability can help analysts understand why a transaction received a high fraud score.

An explanation should support investigation but should not automatically be treated as proof that the prediction is correct.

---

## Risks and Limitations

Important risks include:

- class imbalance
- changing fraud patterns
- data drift
- model-performance degradation
- false positives affecting legitimate customers
- false negatives allowing fraudulent transactions
- limited demographic fairness analysis
- possible differences between historical and future transaction behavior

---

## Monitoring

Production monitoring should include:

- input data drift
- prediction drift
- Precision
- Recall
- F1
- PR-AUC
- latency
- throughput
- errors and service health

Monitoring signals should trigger investigation before automatic retraining.

---

## Model Governance

The production process should maintain:

- model version history
- candidate and champion models
- validation gates
- deployment approval
- retraining policy
- rollback capability
- audit logs
- security and access controls

A newer model version should not automatically replace the existing champion.

---

## Responsible AI Principle

The model is a decision-support system.

Predictions should be interpreted together with business context, monitoring evidence, and human judgment when the consequences of an incorrect prediction are significant.