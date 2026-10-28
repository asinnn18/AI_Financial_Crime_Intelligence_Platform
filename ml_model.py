# ============================================================
# AI-POWERED FINANCIAL CRIME INTELLIGENCE PLATFORM
# MACHINE LEARNING - FRAUD DETECTION
# ============================================================

import pandas as pd
import numpy as np
import pyodbc
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_auc_score,
    roc_curve
)


# ============================================================
# 1. SQL SERVER CONNECTION
# ============================================================

server = r"localhost\SQLEXPRESS"
database = "FinancialCrimeDB"

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
    "Connection Timeout=30;"
)

conn = pyodbc.connect(connection_string)

print("SQL Server connection successful!")


# ============================================================
# 2. LOAD DATA
# ============================================================

query = """
SELECT *
FROM Transactions
"""

print("\nLoading data from SQL Server...")

chunks = []

for chunk in pd.read_sql_query(
    query,
    conn,
    chunksize=10000
):
    chunks.append(chunk)

df = pd.concat(
    chunks,
    ignore_index=True
)

print("Data loaded successfully!")

print("Rows    :", len(df))
print("Columns :", len(df.columns))


# ============================================================
# 3. CLOSE DATABASE CONNECTION
# ============================================================

conn.close()

print("SQL Server connection closed.")


# ============================================================
# 4. CHECK ACTUAL COLUMN NAMES
# ============================================================

print("\n" + "=" * 60)
print("CHECKING COLUMN NAMES")
print("=" * 60)

print(df.columns.tolist())


# ============================================================
# 5. PREPARE FEATURES AND TARGET
# ============================================================

print("\n" + "=" * 60)
print("PREPARING DATA")
print("=" * 60)

# Remove extra spaces from column names
df.columns = df.columns.astype(str).str.strip()

# Convert SQL column names to standard format
df.rename(
    columns={
        "TIME": "Time",
        "amount": "Amount",
        "class": "Class"
    },
    inplace=True
)

# Check target column
if "Class" not in df.columns:
    raise ValueError(
        "ERROR: 'Class' column was not found in the Transactions table."
    )

# Target variable
y = df["Class"]

# TransactionID is an identifier,
# so it should not be used as an ML feature.

if "TransactionID" in df.columns:

    X = df.drop(
        columns=["TransactionID"]
    )

else:

    X = df.copy()

# Remove target column from features
if "Class" in X.columns:

    X = X.drop(
        columns=["Class"]
    )

print("Features:", X.shape)
print("Target  :", y.shape)

print("\nFeature columns:")
print(X.columns.tolist())


# ============================================================
# 6. CHECK CLASS DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("CLASS DISTRIBUTION")
print("=" * 60)

print(y.value_counts())

print("\nClass 0 = Legitimate")
print("Class 1 = Fraud")


# ============================================================
# 7. TRAIN / TEST SPLIT
# ============================================================

print("\n" + "=" * 60)
print("TRAIN / TEST SPLIT")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training rows :", len(X_train))
print("Testing rows  :", len(X_test))

print("\nTraining fraud transactions:")
print(y_train.value_counts())

print("\nTesting fraud transactions:")
print(y_test.value_counts())


# ============================================================
# 8. FEATURE SCALING
# ============================================================

print("\n" + "=" * 60)
print("FEATURE SCALING")
print("=" * 60)

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(
    X_train
)

X_test_scaled = scaler.transform(
    X_test
)

print("Feature scaling completed.")


# ============================================================
# 9. CREATE LOGISTIC REGRESSION MODEL
# ============================================================

print("\n" + "=" * 60)
print("CREATING MACHINE LEARNING MODEL")
print("=" * 60)

model = LogisticRegression(
    class_weight="balanced",
    max_iter=1000,
    random_state=42
)

print("Model: Logistic Regression")
print("Class balancing: Enabled")


# ============================================================
# 10. TRAIN MODEL
# ============================================================

print("\n" + "=" * 60)
print("TRAINING MODEL")
print("=" * 60)

model.fit(
    X_train_scaled,
    y_train
)

print("Model training completed successfully!")


# ============================================================
# 11. MAKE PREDICTIONS
# ============================================================

print("\n" + "=" * 60)
print("MAKING PREDICTIONS")
print("=" * 60)

y_pred = model.predict(
    X_test_scaled
)

y_probability = model.predict_proba(
    X_test_scaled
)[:, 1]

print("Predictions generated successfully.")


# ============================================================
# 12. CLASSIFICATION REPORT
# ============================================================

print("\n" + "=" * 60)
print("CLASSIFICATION REPORT")
print("=" * 60)

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Legitimate",
            "Fraud"
        ]
    )
)


# ============================================================
# 13. CONFUSION MATRIX
# ============================================================

print("\n" + "=" * 60)
print("CONFUSION MATRIX")
print("=" * 60)

cm = confusion_matrix(
    y_test,
    y_pred
)

print(cm)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=[
        "Legitimate",
        "Fraud"
    ]
)

disp.plot()

plt.title(
    "Fraud Detection - Confusion Matrix"
)

plt.tight_layout()
plt.show()


# ============================================================
# 14. ROC-AUC SCORE
# ============================================================

print("\n" + "=" * 60)
print("ROC-AUC SCORE")
print("=" * 60)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)

print(
    "ROC-AUC:",
    round(roc_auc, 4)
)


# ============================================================
# 15. ROC CURVE
# ============================================================

print("\nCreating ROC Curve...")

fpr, tpr, thresholds = roc_curve(
    y_test,
    y_probability
)

plt.figure(figsize=(8, 6))

plt.plot(
    fpr,
    tpr,
    label=f"ROC-AUC = {roc_auc:.4f}"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title(
    "ROC Curve - Fraud Detection"
)

plt.legend()

plt.tight_layout()
plt.show()


# ============================================================
# 16. FRAUD PROBABILITY
# ============================================================

print("\n" + "=" * 60)
print("FRAUD PROBABILITY")
print("=" * 60)

# Get TransactionID for the test transactions
test_transaction_ids = df.loc[
    X_test.index,
    "TransactionID"
].values

# Create results dataframe
results = X_test.copy()

# Add TransactionID
results.insert(
    0,
    "TransactionID",
    test_transaction_ids
)

# Add actual class
results["ActualClass"] = y_test.values

# Add predicted class
results["PredictedClass"] = y_pred

# Add fraud probability
results["FraudProbability"] = (
    y_probability * 100
)

print(
    results[
        [
            "TransactionID",
            "ActualClass",
            "PredictedClass",
            "FraudProbability"
        ]
    ].head(20)
)


# ============================================================
# 17. RISK SCORE
# ============================================================

print("\n" + "=" * 60)
print("RISK SCORE")
print("=" * 60)

results["RiskScore"] = (
    results["FraudProbability"]
).round(2)

print(
    results[
        [
            "TransactionID",
            "ActualClass",
            "PredictedClass",
            "FraudProbability",
            "RiskScore"
        ]
    ].head(20)
)


# ============================================================
# 18. RISK LEVEL
# ============================================================

def assign_risk_level(score):

    if score >= 80:
        return "High Risk"

    elif score >= 50:
        return "Medium Risk"

    elif score >= 20:
        return "Low Risk"

    else:
        return "Minimal Risk"


results["RiskLevel"] = (
    results["RiskScore"]
    .apply(assign_risk_level)
)


# ============================================================
# 19. RISK LEVEL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("RISK LEVEL SUMMARY")
print("=" * 60)

print(
    results["RiskLevel"]
    .value_counts()
)


# ============================================================
# 20. SAVE ML RESULTS TO SQL SERVER
# ============================================================

print("\n" + "=" * 60)
print("SAVING ML RESULTS TO SQL SERVER")
print("=" * 60)

# Reconnect to SQL Server
conn = pyodbc.connect(
    connection_string
)

cursor = conn.cursor()

# Clear previous ML results.
# This makes the script safe to run again.
cursor.execute(
    "TRUNCATE TABLE ML_Fraud_Predictions"
)

# SQL insert query
insert_query = """
INSERT INTO ML_Fraud_Predictions
(
    TransactionID,
    ActualClass,
    PredictedClass,
    FraudProbability,
    RiskScore,
    RiskLevel
)
VALUES (?, ?, ?, ?, ?, ?)
"""

# Prepare data for insertion
data_to_insert = list(
    results[
        [
            "TransactionID",
            "ActualClass",
            "PredictedClass",
            "FraudProbability",
            "RiskScore",
            "RiskLevel"
        ]
    ].itertuples(
        index=False,
        name=None
    )
)

print(
    "Rows ready for SQL:",
    len(data_to_insert)
)

# Faster bulk insertion
cursor.fast_executemany = True

cursor.executemany(
    insert_query,
    data_to_insert
)

# Save changes
conn.commit()

print(
    "ML results inserted successfully!"
)


# Verify number of rows
cursor.execute(
    "SELECT COUNT(*) FROM ML_Fraud_Predictions"
)

sql_result_count = cursor.fetchone()[0]

print(
    "Rows stored in SQL Server:",
    sql_result_count
)

cursor.close()

conn.close()

print("SQL Server connection closed.")


# ============================================================
# 21. TOP 20 HIGHEST-RISK TRANSACTIONS
# ============================================================

print("\n" + "=" * 60)
print("TOP 20 HIGHEST-RISK TRANSACTIONS")
print("=" * 60)

top_risk = (
    results
    .sort_values(
        by="RiskScore",
        ascending=False
    )
    .head(20)
)

print(
    top_risk[
        [
            "TransactionID",
            "ActualClass",
            "PredictedClass",
            "FraudProbability",
            "RiskScore",
            "RiskLevel"
        ]
    ]
)


# ============================================================
# 22. MODEL COMPLETED
# ============================================================

print("\n" + "=" * 60)
print("MACHINE LEARNING COMPLETED SUCCESSFULLY")
print("=" * 60)

print("Model              : Logistic Regression")
print("Training rows      :", len(X_train))
print("Testing rows       :", len(X_test))
print("ROC-AUC            :", round(roc_auc, 4))
print("Fraud probabilities: Generated")
print("Risk scores        : Generated")
print("Risk levels        : Generated")
print("SQL predictions    :", sql_result_count)