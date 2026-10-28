# AI-Powered Financial Crime Intelligence Platform

**Credit Card Fraud Detection & Risk Analytics**

An end-to-end data science project that uses Machine Learning, Python, SQL Server, and Power BI to identify potentially fraudulent credit card transactions, assign risk levels, and visualize fraud patterns.

## Project Overview

Credit card fraud is a major challenge for financial institutions. This project analyzes transaction data, uses a Machine Learning model to predict potentially fraudulent transactions, stores prediction results in SQL Server, and visualizes fraud patterns through an interactive Power BI dashboard.

The project is being extended into a complete web application that will allow users to submit transaction details and view fraud-risk predictions.

## Objectives

- Analyze credit card transaction data.
- Identify potentially fraudulent transaction patterns.
- Build a Machine Learning model for fraud detection.
- Calculate fraud probability and assign risk levels.
- Store transaction and prediction data in SQL Server.
- Visualize fraud trends using Power BI.
- Develop a web interface for transaction risk prediction.

## Technology Stack

- **Programming Language:** Python
- **Data Analysis:** Pandas, NumPy
- **Machine Learning:** Scikit-learn
- **Database:** Microsoft SQL Server
- **Data Visualization:** Microsoft Power BI
- **Backend Framework (Planned):** Flask
- **Frontend Technologies (Planned):** HTML, CSS, JavaScript

## Dataset

**Dataset Name:** Credit Card Fraud Detection

- Total Transactions: 284,807
- Legitimate Transactions: 284,315
- Fraudulent Transactions: 492
- Fraud Rate: Approximately 0.17%

The dataset contains transaction time, anonymized features (V1–V28), transaction amount, and a target column named `Class`.

- `Class = 0`: Legitimate transaction
- `Class = 1`: Fraudulent transaction

**Dataset Source:** [Credit Card Fraud Detection — Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

## Project Workflow

1. **Data Collection:** Obtain the credit card transaction dataset.
2. **Data Preparation:** Clean and prepare transaction data using Python.
3. **Machine Learning:** Train a Logistic Regression model for fraud prediction.
4. **Risk Scoring:** Calculate fraud probabilities and categorize transaction risk.
5. **Database Management:** Store transaction and prediction results in SQL Server.
6. **Data Visualization:** Develop Power BI dashboards to analyze fraud patterns.
7. **Application Development (Planned):** Build a web interface for transaction risk prediction.

## Machine Learning Model

The current implementation uses Logistic Regression with feature scaling and class balancing to address the highly imbalanced dataset.

### Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion Matrix

Because fraudulent transactions represent a very small proportion of the dataset, accuracy alone is not sufficient to evaluate model performance.

## Power BI Dashboard

The dashboard provides insights into:

- Total transactions
- Fraudulent transactions
- Fraud rate
- Total transaction value
- Risk level distribution
- Fraud transactions by amount range
- Fraud transactions by time range
- High-risk transaction records
- Model performance and methodology

## Current Project Status

- [x] Dataset preparation
- [x] Machine Learning model training and evaluation
- [x] Fraud probability and risk scoring
- [x] SQL Server integration
- [x] Power BI dashboard development
- [ ] Flask web application
- [ ] Transaction prediction interface
- [ ] End-to-end application testing

## Planned Features

- Enter transaction details through a web interface.
- Predict fraud probability using the trained Machine Learning model.
- Display the predicted risk category.
- Store prediction history in SQL Server.
- Integrate prediction records with Power BI analytics.
- Explore automated fraud alerts and model monitoring.

## Limitations

This project is an educational prototype built using historical transaction data. Predictions are not definitive proof of fraud, and the model requires further testing before use in real-world financial systems. Performance on historical data does not guarantee performance on new transactions.

## Future Enhancements

- Real-time transaction risk scoring
- Automated fraud alerts
- Model optimization and improved evaluation
- Model monitoring and retraining
- Secure user authentication
- Cloud deployment

## Author

**Ashin A.**

B.Tech in Artificial Intelligence and Data Science

GitHub: [ashinnn07-afk](https://github.com/ashinnn07-afk)

---

*An end-to-end learning project combining Machine Learning, database management, and business intelligence for credit card fraud detection and risk analytics.*
