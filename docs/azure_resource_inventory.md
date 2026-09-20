# G9 Azure Resource Inventory and Cost Note

## Resource Group

Name: rg-fraud-mlops-g9
Region: Central India

Purpose:
Logical container for the G9 Azure MLOps resources.

---

## Cost Control

Monthly Azure budget:
USD 10

Purpose:
Monitor spending during the learning project and avoid unnecessary Azure usage.

A budget provides alerts but does not automatically stop Azure resources.

---

## Storage Account

Name: stfraudmlopsg9
Region: Central India
Performance: Standard
Replication: LRS

Purpose:
Store datasets and model artifacts.

Blob container:
fraud-data

Current layout:

- raw/creditcard_sample.csv
- processed/creditcard_sample.csv
- models/fraud_lr_model.pkl

Cost drivers:
- amount of stored data
- read/write operations
- data transfer

The project uses only small files, so storage usage is intentionally minimal.

---

## Azure Machine Learning Workspace

Name: mlw-fraud-mlops-g9
Region: Central India

Purpose:
Manage Azure ML jobs, pipelines, environments, components, datasets, and model versions.

Supporting resources include:

- Azure Key Vault
- Application Insights
- Log Analytics

Container Registry was not required for the current learning workflow.

---

## Azure ML Compute

Training jobs used:
Serverless CPU compute.

Purpose:
Run small Azure ML training and pipeline workloads without maintaining a dedicated VM.

Cost driver:
Compute duration and machine resources used by training/pipeline jobs.

Cost-control approach:

- use a very small fraud sample
- use Logistic Regression for the Azure demonstration
- use CPU instead of GPU
- avoid persistent dedicated compute
- run only the jobs required for the capstone

---

## Azure ML Data / Datastore

Datastore:
frauddatastore

Storage:
stfraudmlopsg9 / fraud-data

Purpose:
Allow Azure ML jobs to access Blob-hosted project data.

For the learning exercise, account-key authentication was used.

A production design should prefer managed identity / RBAC where practical.

---

## Azure ML Pipeline

Implemented pipeline:

Train -> Evaluate

Components:

- fraud_train_component
- fraud_evaluate_component

Purpose:
Provide reproducible and reusable ML workflow steps.

---

## Azure ML Model Registry

Model:
fraud-lr-azure-demo

Versions:
- Version 1
- Version 2

Purpose:
Maintain model versions for traceability, comparison, promotion, and rollback.

---

## Cost Summary

The main potential cost driver in this project is Azure ML compute.

Storage usage is very small.

No dedicated always-on ML compute or Azure Managed Online Endpoint was created.

The project deliberately uses small datasets, serverless CPU jobs, and limited executions to reduce cost.

At project completion, unnecessary billable resources should be stopped or deleted and cleanup evidence recorded.
