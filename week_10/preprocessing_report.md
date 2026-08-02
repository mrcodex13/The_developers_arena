# Preprocessing Report — Customer Churn Prediction

## Dataset
- **Source:** `churn_data.csv` — 500 customer records
- **Columns:** CustomerID, Tenure, MonthlyCharges, TotalCharges, Contract, PaymentMethod, PaperlessBilling, SeniorCitizen, Churn
- **Missing values:** None across any column
- **Churn distribution:** 89.4% retained, 10.6% churned (imbalanced target)

## 1. Categorical Encoding (3 methods implemented)

| Method | Column(s) | Rationale |
|---|---|---|
| **Label Encoding** | PaperlessBilling | Binary category (Yes/No) — a single 0/1 column is sufficient |
| **One-Hot Encoding** | Contract, PaymentMethod | Nominal categories with no inherent order — avoids introducing false ordinal relationships |
| **Ordinal Encoding** | Contract | Applied separately to capture the natural order (Month-to-month < One year < Two year) for models that can exploit ordinal signal |

## 2. Feature Scaling (2 methods implemented)

| Method | Effect | Applied To |
|---|---|---|
| **Min-Max Scaling** | Rescales values into [0, 1] | Tenure, MonthlyCharges, TotalCharges |
| **Standard Scaling (Z-score)** | Centers to mean 0, std 1 | Tenure, MonthlyCharges, TotalCharges |

Both were computed side-by-side to compare distribution shape — Min-Max preserves the original distribution shape but compresses range, while Standard Scaling normalizes spread and is generally preferred for models sensitive to feature magnitude (e.g. logistic regression, distance-based models).

## 3. Outlier Detection & Handling

Two detection methods were applied to Tenure, MonthlyCharges, and TotalCharges:

| Method | Rule |
|---|---|
| **IQR method** | Flag values outside [Q1 − 1.5×IQR, Q3 + 1.5×IQR] |
| **Z-score method** | Flag values where \|z\| > 3 |

**Result:** No outliers were detected in any of the three numeric columns by either method — the dataset's numeric ranges are already well-behaved. The capping (winsorizing) step was still implemented in the pipeline as a safety net for future/unseen data, with 0 values actually capped on this dataset.

## 4. Data Quality Checks
- No missing values.
- No duplicate CustomerIDs.
- All categorical columns have clean, consistent labels with no typos.
- All numeric columns fall within sane, non-negative ranges.

## 5. Final Preprocessing Pipeline
A single `sklearn.pipeline.Pipeline` combining a `ColumnTransformer` was built to apply, in one call:
1. Median imputation (numeric) / most-frequent imputation (categorical) — defensive step for unseen missing data
2. Standard scaling on numeric features
3. One-hot encoding on categorical features
4. Random Forest classification

**Result on held-out test set (20%):**
- Accuracy: 97%
- ROC-AUC: 0.999
- Recall (Churn class): 73%, Precision (Churn class): 100%

See `feature_engineering_documentation.md` for details on the engineered features feeding into this pipeline.