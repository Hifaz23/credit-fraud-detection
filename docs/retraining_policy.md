# Fraud Model Retraining Policy

## Strategy
Use a hybrid retraining strategy:
- Perform a formal model evaluation monthly.
- Allow monitoring signals to trigger an earlier investigation.

## Monitoring Triggers
Investigate retraining when:
- PSI >= 0.25 for important production features.
- Precision, Recall, F1, or PR-AUC show sustained degradation across monitoring windows.
- Fraud patterns or business requirements materially change.

A drift alert alone does not automatically trigger retraining.

## Data Requirement
Retraining and performance validation require sufficient recent labeled transactions.
Very small numbers of fraud cases should not be used to make strong retraining decisions.

## Retraining Flow
1. Monitor data, prediction, model, and service metrics.
2. Detect a sustained degradation or significant business change.
3. Collect and validate recent labeled data.
4. Train a candidate model using the reproducible training pipeline.
5. Evaluate the candidate on unseen validation/test data.
6. Compare the candidate with the current champion.
7. Register the candidate model only when validation requirements are satisfied.
8. Promote the candidate after approval.
9. Continue production monitoring.

## Validation Gate
Before promotion, verify:
- PR-AUC does not materially degrade compared with the champion.
- Recall remains acceptable for fraud detection.
- Precision remains acceptable to control false alerts.
- No major data-quality or fairness issue is introduced.
- Training and evaluation complete successfully.

## Rollback
Keep the previous champion model version.
If the newly deployed model causes unacceptable model-performance or service-health degradation, restore the previous champion version.

## Important Principle
Drift is a signal to investigate. It is not, by itself, proof that retraining is required.
