# Data Quality & Leakage Analysis

## 1. Purpose

This document formalizes the data quality and leakage-related decisions
for the real estate price prediction project.

Its goal is to ensure that:
- only valid and prediction-time-available information is used,
- data quality issues are handled consistently,
- modeling results remain reliable and interpretable.

All decisions documented here will guide subsequent data preparation
and feature engineering steps.

---

## 2. Decision Principles

The following principles guide all data quality and leakage-related decisions
made in this project.

1. **Prediction-time availability**  
   A variable must be available at the time a price estimation is produced.
   Any information derived from or dependent on the sale transaction itself
   is considered potential data leakage.

2. **Business plausibility**  
   Decisions must be consistent with real estate domain logic.
   Data artifacts or values that contradict real-world property characteristics
   are treated as data quality issues.

3. **Minimal irreversible decisions**  
   Variables are only permanently excluded when strongly justified.
   When uncertainty exists, variables are flagged for careful handling
   rather than immediately dropped.

4. **Separation of observation and action**  
   Observations from EDA are used to inform decisions, but transformations
   and modeling actions are deferred to later stages of the pipeline.

5. **Traceability and reproducibility**  
   All decisions must be explicitly documented and reproducible,
   allowing future reviewers to understand and challenge the rationale.

---

## 3. Missing Values — High-Level Assessment

The exploratory data analysis revealed heterogeneous patterns of missing values
across variables. These patterns are not treated uniformly, as missingness may
reflect different underlying causes.

At a high level, variables are grouped into three categories:

- **Very high missingness (>80%)**  
  Variables that are absent for the majority of properties, often because the
  corresponding feature is rare or optional.

- **Moderate missingness (10–30%)**  
  Variables that contain meaningful information but are partially missing,
  potentially reflecting real-world absence or incomplete records.

- **Low or no missingness (<5%)**  
  Variables that are largely complete and considered reliable from a data
  availability standpoint.

This categorization serves as a framework for subsequent variable-level decisions
and ensures that missing-value handling strategies are applied consistently.

---

## 4. Variables with Very High Missingness

The following variables exhibit extremely high proportions of missing values
(typically greater than 80% of observations):

- `PoolQC`
- `Alley`
- `Fence`
- `MiscFeature`

### Decision
These variables will be **excluded from the modeling pipeline**.

### Justification
- Missingness is largely structural, reflecting the absence of the corresponding
  feature rather than random data loss.
- The small number of non-missing observations limits the statistical usefulness
  of these variables.
- Including them would introduce additional complexity (encoding, imputation)
  with limited expected performance gains.
- Their exclusion reduces noise and simplifies the preprocessing pipeline
  without materially impacting predictive power.

These variables may still be referenced for exploratory or descriptive analysis,
but they will not be used as model inputs.

---

## 5. Variables with Moderate or Low Missingness (Semantically Meaningful)

Several variables exhibit moderate or low proportions of missing values while
remaining highly informative. In these cases, missingness is not random but
reflects the absence of a structural component of the property.

This category includes:

- `MasVnrType`, `FireplaceQu` (moderate to high missingness)
- `GarageType`, `GarageFinish`, `GarageYrBlt`, `GarageQual`, `GarageCond`
- `BsmtExposure`, `BsmtFinType1`, `BsmtFinType2`, `BsmtQual`, `BsmtCond`
- `LotFrontage`

### Decision
These variables will be **retained** and treated using explicit, semantics-aware
missing-value strategies.

### Rationale
- Missing values encode meaningful information such as the absence of a garage,
  basement, fireplace, or masonry veneer.
- The proportion of missing values is sufficiently low to preserve statistical
  robustness.
- Retaining these variables allows the model to capture important structural
  property characteristics.

### Handling Strategy (High-Level)
- Missing categorical values will be encoded as a dedicated "None" or "No" category.
- For numerical variables, missingness indicators may be introduced where relevant.
- Imputation strategies will be designed to preserve semantic meaning rather than
  relying on global statistics.

Final handling choices will be validated during preprocessing and modeling.

---

## 6. Leakage Risk Assessment

Data leakage occurs when information that would not be available at prediction time
is used during model training, resulting in overly optimistic performance estimates.

At this stage, leakage risks are assessed at a **conceptual and categorical level**.
This analysis is not an exhaustive column-by-column audit, but a targeted identification
of high-risk variable groups based on domain knowledge and dataset structure.

A detailed, feature-level leakage review will be conducted during the feature
engineering phase.

---

### 6.1 Transaction-related variables

Examples include:
- `SaleType`
- `SaleCondition`

**Assessment**  
These variables describe characteristics of the sale transaction itself and are
typically determined at or after the sale is finalized.

**Decision**  
These variables are **excluded from the baseline modeling pipeline** to prevent
direct transaction-level leakage.

---

### 6.2 Temporal variables

Examples include:
- `YearSold`
- `MoSold`

**Assessment**  
These variables encode the timing of the sale and may indirectly capture market
conditions or temporal trends.

While technically known at sale time, their inclusion may bias evaluation results
when using random cross-validation strategies.

**Decision**  
These variables are **excluded from baseline models**.
Their inclusion may be reconsidered only under a time-aware validation framework.

---

### 6.3 Subjective assessments and target proxies

Examples include:
- `OverallQual`
- `OverallCond`

**Assessment**  
These variables represent human-assigned assessments of property quality and condition.
They may act as indirect proxies for value, but such information is typically available
to agents or sellers prior to price estimation.

**Decision**  
These variables are **retained**, with the understanding that their impact will be
closely monitored during modeling and error analysis.

---

### 6.4 Scope limitation

This section intentionally focuses on **high-level leakage risks**.
No definitive keep/drop decision is made here for all variables.

A comprehensive, feature-by-feature leakage assessment will be performed as part of
the preprocessing and feature engineering phase, where each variable will be evaluated
in the context of the full modeling pipeline.

---

## 8. Summary of Decisions

The table below summarizes the key data quality and leakage-related decisions
made during this phase of the project.

| Category | Variables (examples) | Decision | Rationale |
|---------|----------------------|----------|-----------|
| Very high missingness (>80%) | `PoolQC`, `Alley`, `Fence`, `MiscFeature` | Drop | Structural absence, extremely sparse signal |
| Moderate to high missingness (informative absence) | `MasVnrType`, `FireplaceQu` | Keep | Missingness encodes meaningful absence |
| Low missingness with semantic meaning | `Garage*`, `Bsmt*`, `LotFrontage` | Keep | Informative features with manageable missingness |
| Transaction-related variables | `SaleType`, `SaleCondition` | Exclude | Post-sale or transaction-specific information |
| Temporal variables | `YearSold`, `MoSold` | Exclude (baseline) | Risk of temporal leakage under random CV |
| Subjective assessments / proxies | `OverallQual`, `OverallCond` | Keep (monitor) | Available at prediction time, potential value proxy |

These decisions apply to the baseline modeling pipeline and may be revisited
during feature engineering if justified by validation results.

## 9. Next Steps

The decisions documented in this section define the scope and constraints for
subsequent data preparation and modeling activities.

The next phase of the project will focus on:
- implementing preprocessing pipelines consistent with the documented decisions,
- defining explicit imputation and encoding strategies for retained variables,
- performing a comprehensive, feature-level review during feature engineering,
- validating data quality and leakage assumptions through model evaluation.

No modeling or feature transformation should be performed without adhering
to the guidelines established in this document.

