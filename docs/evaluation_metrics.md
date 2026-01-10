# Evaluation Metrics & Success Criteria

## Context
The purpose of this issue is to define **how model performance will be evaluated**
in a way that is both **machine-learning sound** and **business-relevant**.

In real estate price prediction, a model is not judged only by raw accuracy,
but by its ability to:
- produce errors that are understandable in monetary terms,
- remain stable across different data splits,
- avoid over-optimistic performance estimates.

---

## Objectives
- Select evaluation metrics aligned with the business use case
- Define a robust validation strategy
- Establish clear and realistic success criteria
- Ensure comparability between different models and feature sets

---

## Primary Evaluation Metrics

### Mean Absolute Error (MAE)
**Definition**: Average absolute difference between predicted and actual prices.

**Justification**:
- Directly interpretable in currency units
- Easy to communicate to non-technical stakeholders
- Reflects average prediction error without over-penalizing outliers

**Role**: **Primary business metric**

---

### Root Mean Squared Error (RMSE)
**Definition**: Square root of the average squared prediction error.

**Justification**:
- Penalizes large errors more strongly
- Useful to detect models that fail badly on some properties

**Role**: Secondary metric for risk assessment

---

### R² Score
**Definition**: Proportion of variance explained by the model.

**Justification**:
- Useful as a relative performance indicator
- Less interpretable from a business standpoint

**Role**: Monitoring / comparison only

---

## Target Transformation
Due to price distribution skewness, model training and evaluation may be performed on:

- `log(price)` or `log1p(price)`

In that case:
- Metrics will be computed in log-space for training stability
- Business interpretation will rely on back-transformed errors when relevant

---

## Validation Strategy

### Cross-Validation
- **Strategy**: K-Fold Cross-Validation
- **Default**: K = 5 (with shuffle and fixed random state)

**Rationale**:
- Reduces dependency on a single train/test split
- Provides a more reliable estimate of generalization performance
- Enables comparison of models under identical conditions

---

### Stability Assessment
For each metric:
- Mean value across folds will be reported
- Standard deviation across folds will be analyzed

High variance across folds will be considered a risk indicator.

---

## Success Criteria

The project will be considered successful if:

- MAE is reasonably low relative to the median property price
- Performance is stable across cross-validation folds
- Improvements over the baseline model are measurable and consistent
- Model behavior can be explained through error analysis

No absolute performance threshold is imposed, as results depend on data quality
and feature availability.

---

## 6. Document Status
- Related Issue: Issue #2 — Define evaluation metrics & success criteria
- Status: Approved
- Last updated: _to be updated_
