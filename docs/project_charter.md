# Project Charter — Real Estate Price Prediction (ML)

## 1. Business Context

This project simulates an **enterprise-grade machine learning initiative** focused on real estate price prediction.

The objective is to design a **decision-support model**, not an automated pricing engine.  
The model aims to assist:
- real estate agents in estimating fair and realistic market prices,
- property sellers in understanding expected price ranges,
- internal analytics and product teams in analyzing real estate market trends.

The project intentionally reflects real-world machine learning constraints, including imperfect data, trade-offs between model performance and interpretability, and the need for reproducible and robust pipelines.

---

## 2. Business Problem

In real estate platforms, inaccurate price estimation leads to:
- overvalued properties remaining too long on the market,
- undervalued properties negatively impacting seller confidence,
- reduced trust in digital estimation tools.

The business need is to provide **reliable and explainable price estimates** that support pricing decisions while highlighting cases where predictions may be less reliable.

---

## 3. Machine Learning Problem Formulation

- **Problem type**: Supervised regression  
- **Target variable**: Property sale price  
- **Model output**: Estimated sale price (or log-transformed price)

The model learns a relationship between property characteristics (size, quality indicators, location proxies, etc.) and historical sale prices.  
Predictions are intended to be **accurate enough to support decision-making**, rather than perfectly exact.

---

## 4. Target Users

- **Primary users**: Real estate agents  
- **Secondary users**: Property sellers using estimation tools  
- **Internal users**: Data and product teams

The model is not intended for direct automated decision-making or pricing enforcement.

---

## 5. Key Constraints

- **Data quality**: Missing values, noise, and inconsistencies are expected  
- **Explainability**: Predictions must be interpretable and justifiable  
- **Robustness**: Model performance must be stable across data splits  
- **Data leakage prevention**: Strict separation between training and evaluation data  
- **Reproducibility**: End-to-end pipeline reproducibility is required  

---

## 6. Assumptions

- Historical sale prices reasonably reflect market value  
- Input features used at prediction time are available and consistent with training data  
- The dataset is representative of the target market population  
- External market shocks are considered out of scope  

---

## 7. Scope & Limitations

### In Scope
- Exploratory data analysis and data quality assessment  
- Feature engineering and data preprocessing  
- Model comparison using cross-validation  
- Error analysis and model interpretability  

### Out of Scope
- Model deployment and monitoring  
- Real-time inference  
- Integration with external APIs  
- Legal, regulatory, or compliance considerations  

---

## 8. Key Decisions

- Priority is given to **data quality and feature engineering** over model complexity  
- Cross-validation is preferred over a single train/test split  
- Simpler and interpretable models may be selected if performance differences are marginal  

---

## 9. Success Criteria (High-Level)

- The model demonstrates stable performance across cross-validation folds  
- Error metrics are interpretable from a business perspective  
- Model behavior can be explained and analyzed through error analysis  

---

## 10. Document Status

- **Related Issue**: Issue #1 — Define business context & ML objectives  
- **Status**: Approved  
- **Last updated**: _to be updated_

