# Technical Documentation

## 1. Introduction
Customer churn prediction is a supervised classification problem in which a business seeks to identify customers who are likely to end a subscription. This project demonstrates a complete data science workflow using a real customer churn dataset.

## 2. Methodology
The workflow included:
- dataset loading and inspection
- data cleaning and type correction
- exploratory data analysis
- preprocessing using one-hot encoding and scaling
- training multiple machine learning models
- comparing evaluation metrics
- tuning the strongest model
- saving the final model for deployment

## 3. Dataset
The dataset contains the following fields:
- CustomerID
- Tenure
- MonthlyCharges
- TotalCharges
- Contract
- PaymentMethod
- PaperlessBilling
- SeniorCitizen
- Churn

## 4. Preprocessing
The preprocessing pipeline used:
- duplicate removal
- missing-value cleanup
- numeric conversion for charge fields
- one-hot encoding for categorical variables
- standard scaling for numeric variables

## 5. Algorithms
The model comparison included:
- Logistic Regression
- Decision Tree
- Random Forest
- Support Vector Machine
- KNN

## 6. Evaluation
Model quality was measured by accuracy, precision, recall, F1-score, ROC-AUC, and confusion matrix values.

## 7. Deployment
The final model was serialized using pickle and deployed via a Flask API with a lightweight HTML interface.

## 8. Results
The random forest classifier can be used as the final predictive model after tuning.

## 9. Future Work
Potential improvements include using more advanced boosting algorithms, adding customer interaction features, and creating an automated retraining pipeline.
