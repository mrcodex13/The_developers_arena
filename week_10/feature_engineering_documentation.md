# Feature Engineering Documentation — Customer Churn Prediction

## Overview
Six new features were engineered from the raw dataset to capture spend behavior, customer value, billing consistency, and tenure segments — beyond what the original 8 raw columns expose.

## Engineered Features

### 1. AvgMonthlySpend
```
AvgMonthlySpend = TotalCharges / Tenure
```
Normalizes total spend by how long the customer has been active, enabling fair comparison between long-tenure and new customers. **Correlation with Churn: +0.40** (strongest positive correlate) — churned customers tend to have unusually high average monthly spend relative to their short tenure.

### 2. CustomerLifetimeValue (CLV)
```
CustomerLifetimeValue = MonthlyCharges × Tenure
```
A simple proxy for total value extracted from the customer so far, assuming a constant billing rate. **Correlation with Churn: −0.37** — customers with low CLV (short tenure and/or lower charges) churn more.

### 3. PaymentEfficiency
```
PaymentEfficiency = TotalCharges / (MonthlyCharges × Tenure)
```
Measures how closely a customer's actual total billing matches their expected billing under a constant rate. Values far from 1.0 flag billing irregularities or rate changes over the customer's lifetime. **Correlation with Churn: +0.20.**

### 4. TenureGroup
```
Bins: New (0–12 months) | Established (12–36 months) | Loyal (36+ months)
```
Segments customers into intuitive lifecycle stages. **Finding:** churn is entirely concentrated in the "New" segment (63.1% churn rate, 84 customers) — 0% churn in both Established and Loyal segments (416 customers combined). This is the single most actionable pattern found in the dataset.

### 5. HighValueCustomer
```
HighValueCustomer = 1 if MonthlyCharges > median(MonthlyCharges) else 0
```
A simple binary flag identifying above-median spenders, useful for quick segmentation in dashboards or rules-based retention triggers. **Correlation with Churn: +0.09.**

### 6. IsLongTermContract
```
IsLongTermContract = 1 if Contract in ['One year', 'Two year'] else 0
```
Collapses the three-way Contract category into a binary commitment flag. **Correlation with Churn: −0.23** — long-term contract holders churn substantially less.

## Feature Selection Results

Two complementary methods were used to rank features:

**Correlation with Churn (numeric features):**
| Feature | Correlation |
|---|---|
| Tenure | −0.51 |
| AvgMonthlySpend | +0.40 |
| CustomerLifetimeValue | −0.37 |
| IsLongTermContract | −0.23 |
| PaymentEfficiency | +0.20 |
| Contract_Ordinal | −0.18 |
| MonthlyCharges | +0.11 |
| HighValueCustomer | +0.09 |
| TotalCharges | +0.004 |
| SeniorCitizen | −0.02 |

**Random Forest Feature Importance** (top 6 selected for modeling):
1. Tenure
2. CustomerLifetimeValue
3. AvgMonthlySpend
4. PaymentEfficiency
5. MonthlyCharges
6. TotalCharges

Both methods agree: **Tenure, CustomerLifetimeValue, and AvgMonthlySpend are the strongest predictors of churn.** TotalCharges and SeniorCitizen contribute little signal on their own once the engineered features are included — they were retained in the pipeline anyway for completeness, but ranked lowest in importance.

## Takeaway
Feature engineering surfaced a signal invisible in the raw columns alone: churn risk is not spread across the customer base — it is concentrated almost entirely in the first 12 months of the customer relationship. This directly informs the retention strategy (see the Week 8 capstone recommendations for a related analysis).