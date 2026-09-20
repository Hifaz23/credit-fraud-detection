# G9 Fraud MLOps Security Checklist

## 1. Identity and Access Management

- [x] Azure resources are accessed through authenticated identities.
- [x] Storage access was granted using Azure RBAC.
- [x] Storage Blob Data Contributor was used instead of unnecessarily broad Owner permissions.
- [ ] Production services should use managed identities wherever possible.
- [ ] Periodically review and remove unnecessary permissions.

## 2. Least Privilege

- Grant users and services only the permissions required for their task.
- Avoid giving Contributor or Owner roles when a narrower role is sufficient.
- Separate development, deployment, and administrative permissions where possible.

## 3. Secrets Management

- [x] Azure ML workspace includes Azure Key Vault support.
- [ ] Do not hard-code passwords, API keys, account keys, or connection strings in source code.
- [ ] Do not commit secrets to Git.
- [ ] Prefer Azure Key Vault and managed identity for production credentials.

### Current G9 Note

The Azure ML datastore was configured using a storage account key for the learning exercise.

For a production system, prefer managed identity / RBAC to reduce long-lived credential exposure.

## 4. Data Privacy / PII

- The fraud dataset uses anonymized V1-V28 features and does not expose obvious direct customer identifiers.
- Transaction data should still be treated as sensitive financial data.
- Collect only data required for the fraud-detection purpose.
- Restrict access to raw transaction data.
- Avoid logging sensitive transaction information unnecessarily.

## 5. Storage Security

- [x] Fraud Blob container is private.
- [x] Anonymous public Blob access is not required.
- [ ] Production storage should restrict unnecessary network access.
- [ ] Use separate raw, processed, and model locations with appropriate access permissions.

## 6. Encryption

- Protect stored data using encryption at rest.
- Use encrypted network connections such as HTTPS/TLS for data in transit.
- Protect model artifacts, datasets, logs, and backups.

## 7. API Security

- Validate all incoming requests.
- Reject unexpected fields and invalid data types.
- Use authentication/authorization before exposing a production fraud API publicly.
- Use HTTPS in production.
- Apply rate limiting and abuse protection where appropriate.
- Avoid returning internal exception details to clients.

## 8. Model and Registry Security

- Restrict who can register, promote, or delete model versions.
- Preserve model version history for traceability and rollback.
- Validate candidate models before production promotion.
- Record model metadata and approval information.

## 9. Logging and Audit

Monitor and retain relevant records for:

- authentication and access attempts
- permission changes
- model registration and promotion
- training jobs
- deployment changes
- prediction-service errors
- security incidents

Logs should not expose secrets or unnecessary sensitive data.

## 10. Production Security Principle

Security must cover the complete ML lifecycle:

Data -> Training -> Registry -> Deployment -> Monitoring -> Retraining

The core rule is least privilege:
give each identity only the access required to perform its job.