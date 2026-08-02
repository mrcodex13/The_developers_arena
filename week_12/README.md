# 📊 Customer Churn Prediction using Machine Learning

## 📌 Project Overview

Customer retention is one of the most important challenges for subscription-based businesses. Acquiring a new customer costs significantly more than retaining an existing one. This project develops a machine learning model that predicts whether a customer is likely to churn based on customer demographics, account information, and service usage.

The project demonstrates the complete end-to-end data science workflow, including data collection, preprocessing, exploratory data analysis, feature engineering, model development, evaluation, and deployment.

---

# 🎯 Problem Statement

The objective of this project is to predict customer churn using historical customer data so that businesses can identify customers at risk of leaving and take proactive retention measures.

---

# 🎯 Objectives

- Perform data cleaning and preprocessing
- Conduct exploratory data analysis (EDA)
- Visualize customer behavior patterns
- Build multiple machine learning models
- Compare model performance
- Select the best-performing model
- Deploy the trained model using Flask
- Present business insights and recommendations

---

# 📂 Project Structure

```
Customer-Churn-Prediction/
│
├── README.md
├── capstone_project.ipynb
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── customer_churn.csv
│
├── src/
│   ├── data_preprocessing.py
│   ├── model.py
│   └── utils.py
│
├── deployment/
│   ├── app.py
│   ├── requirements.txt
│   └── saved_model.pkl
│
├── reports/
│   ├── technical_documentation.md
│   └── business_report.md
│
└── presentation/
    └── Customer_Churn_Presentation.pptx
```

---

# 🛠 Technologies Used

- Python
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Flask
- Pickle
- Git
- GitHub

---

# 📊 Dataset

The project uses a customer churn dataset containing customer demographic information, account details, service usage, and churn status.

Example features include:

- Customer ID
- Gender
- Senior Citizen
- Tenure
- Monthly Charges
- Total Charges
- Internet Service
- Contract Type
- Payment Method
- Churn

Target Variable:

```
Churn
```

- Yes
- No

---

# 🔄 Machine Learning Workflow

## 1. Data Collection

- Load customer dataset
- Inspect data types
- Identify missing values

---

## 2. Data Preprocessing

- Remove unnecessary columns
- Handle missing values
- Encode categorical variables
- Scale numerical features
- Split training and testing datasets

---

## 3. Exploratory Data Analysis

Performed:

- Distribution Analysis
- Correlation Heatmap
- Churn Distribution
- Contract Type Analysis
- Monthly Charges Distribution
- Tenure Analysis
- Service Usage Analysis

---

## 4. Feature Engineering

- Label Encoding
- One-Hot Encoding
- Feature Scaling
- Train-Test Split

---

## 5. Model Building

Models trained:

- Logistic Regression
- Decision Tree
- Random Forest
- Support Vector Machine

---

## 6. Model Evaluation

Evaluation Metrics:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC Score
- Confusion Matrix

---

## 7. Model Deployment

The final trained model is deployed using Flask.

The web application accepts customer information and predicts whether the customer is likely to churn.

---

# 📈 Results

Best Performing Model:

Random Forest Classifier

Example Performance:

| Metric | Score |
|---------|--------|
| Accuracy | 89% |
| Precision | 88% |
| Recall | 86% |
| F1 Score | 87% |
| ROC-AUC | 0.91 |

---

# 💼 Business Insights

Key findings include:

- Customers with month-to-month contracts have higher churn rates.
- High monthly charges increase the likelihood of churn.
- Customers with longer tenure are more likely to remain loyal.
- Fiber internet users showed relatively higher churn.
- Automatic payment methods reduce customer churn.

---

# 💡 Recommendations

- Offer discounts for long-term contracts.
- Improve customer engagement during the first six months.
- Provide loyalty rewards.
- Encourage automatic payment enrollment.
- Monitor customers with high monthly charges.

---

# 🚀 Deployment

Run the Flask application:

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

# 📦 Installation

Clone repository

```bash
git clone https://github.com/yourusername/customer-churn-prediction.git
```

Navigate to project

```bash
cd customer-churn-prediction
```

Install dependencies

```bash
pip install -r deployment/requirements.txt
```

Run application

```bash
python deployment/app.py
```

---

# 📚 Future Improvements

- Deploy using Streamlit
- Deploy on Render or Railway
- Hyperparameter optimization
- XGBoost implementation
- Deep Learning approach
- Real-time prediction API

---

# 👨‍💻 Author

**Name:** Kartik Singh

Final Capstone Project

Data Science & Machine Learning

---

# 📜 License

This project is developed for educational purposes as part of a Data Science Capstone Project.
