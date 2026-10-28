# ============================================================
# AI-POWERED FINANCIAL CRIME INTELLIGENCE PLATFORM
# EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================

import pandas as pd
import pyodbc
import matplotlib.pyplot as plt


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
# 2. LOAD DATA FROM SQL SERVER
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


# ============================================================
# 3. BASIC DATASET INFORMATION
# ============================================================

print("\n" + "=" * 60)
print("DATASET INFORMATION")
print("=" * 60)

print("Rows    :", len(df))
print("Columns :", len(df.columns))


# ============================================================
# 4. FIRST 5 ROWS
# ============================================================

print("\n" + "=" * 60)
print("FIRST 5 ROWS")
print("=" * 60)

print(df.head())


# ============================================================
# 5. COLUMN NAMES
# ============================================================

print("\n" + "=" * 60)
print("COLUMN NAMES")
print("=" * 60)

print(df.columns.tolist())


# ============================================================
# 6. DATA TYPES AND NON-NULL VALUES
# ============================================================

print("\n" + "=" * 60)
print("DATASET STRUCTURE")
print("=" * 60)

df.info()


# ============================================================
# 7. STATISTICAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("STATISTICAL SUMMARY")
print("=" * 60)

print(df.describe())


# ============================================================
# 8. NULL VALUE CHECK
# ============================================================

print("\n" + "=" * 60)
print("NULL VALUE CHECK")
print("=" * 60)

null_values = df.isnull().sum()

print(null_values)


# ============================================================
# 9. FRAUD VS LEGITIMATE TRANSACTIONS
# ============================================================

print("\n" + "=" * 60)
print("FRAUD VS LEGITIMATE TRANSACTIONS")
print("=" * 60)

transaction_counts = df["Class"].value_counts().sort_index()

print(transaction_counts)

print("\n0 = Legitimate")
print("1 = Fraud")


# ============================================================
# 10. FRAUD PERCENTAGE
# ============================================================

print("\n" + "=" * 60)
print("TRANSACTION PERCENTAGE")
print("=" * 60)

transaction_percentage = (
    df["Class"]
    .value_counts(normalize=True)
    .sort_index()
    * 100
)

print(transaction_percentage)


# ============================================================
# 11. FRAUD AND LEGITIMATE COUNT SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("TRANSACTION SUMMARY")
print("=" * 60)

total_transactions = len(df)

legitimate_transactions = (
    (df["Class"] == 0).sum()
)

fraud_transactions = (
    (df["Class"] == 1).sum()
)

fraud_percentage = (
    fraud_transactions
    / total_transactions
    * 100
)

print("Total Transactions      :", total_transactions)
print("Legitimate Transactions :", legitimate_transactions)
print("Fraud Transactions      :", fraud_transactions)
print("Fraud Percentage        :", round(fraud_percentage, 4), "%")


# ============================================================
# 12. TRANSACTION AMOUNT ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("TRANSACTION AMOUNT ANALYSIS")
print("=" * 60)

amount_analysis = (
    df.groupby("Class")["Amount"]
    .agg(
        Count="count",
        Mean="mean",
        Median="median",
        Minimum="min",
        Maximum="max"
    )
)

print(amount_analysis)


# ============================================================
# 13. FRAUD TRANSACTION AMOUNT ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("FRAUD TRANSACTION AMOUNT ANALYSIS")
print("=" * 60)

fraud_amount = df.loc[
    df["Class"] == 1,
    "Amount"
]

print("Minimum Fraud Amount :", fraud_amount.min())
print("Maximum Fraud Amount :", fraud_amount.max())
print("Average Fraud Amount :", fraud_amount.mean())
print("Median Fraud Amount  :", fraud_amount.median())


# ============================================================
# 14. LEGITIMATE TRANSACTION AMOUNT ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("LEGITIMATE TRANSACTION AMOUNT ANALYSIS")
print("=" * 60)

legitimate_amount = df.loc[
    df["Class"] == 0,
    "Amount"
]

print("Minimum Legitimate Amount :", legitimate_amount.min())
print("Maximum Legitimate Amount :", legitimate_amount.max())
print("Average Legitimate Amount :", legitimate_amount.mean())
print("Median Legitimate Amount  :", legitimate_amount.median())


# ============================================================
# 15. AMOUNT RANGE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("FRAUD BY AMOUNT RANGE")
print("=" * 60)

amount_bins = [
    -1,
    50,
    100,
    500,
    1000,
    float("inf")
]

amount_labels = [
    "Below 50",
    "50 - 99.99",
    "100 - 499.99",
    "500 - 999.99",
    "1000 and Above"
]

fraud_data = df[df["Class"] == 1].copy()

fraud_data["AmountRange"] = pd.cut(
    fraud_data["Amount"],
    bins=amount_bins,
    labels=amount_labels,
    include_lowest=True
)

fraud_amount_range = (
    fraud_data["AmountRange"]
    .value_counts()
    .reindex(amount_labels, fill_value=0)
)

print(fraud_amount_range)


# ============================================================
# 16. TIME RANGE CREATION
# ============================================================

print("\n" + "=" * 60)
print("CREATING TIME RANGES")
print("=" * 60)

time_bins = [
    -1,
    21600,
    43200,
    64800,
    86400,
    108000,
    129600,
    151200,
    172793
]

time_labels = [
    "0-6 hrs",
    "6-12 hrs",
    "12-18 hrs",
    "18-24 hrs",
    "24-30 hrs",
    "30-36 hrs",
    "36-42 hrs",
    "42-48 hrs"
]

df["TimeRange"] = pd.cut(
    df["Time"],
    bins=time_bins,
    labels=time_labels,
    include_lowest=True
)

print("Time ranges created successfully!")


# ============================================================
# 17. FRAUD TRANSACTIONS BY TIME RANGE
# ============================================================

print("\n" + "=" * 60)
print("FRAUD TRANSACTIONS BY TIME RANGE")
print("=" * 60)

fraud_time_analysis = (
    df[df["Class"] == 1]
    .groupby(
        "TimeRange",
        observed=False
    )
    .size()
    .reindex(time_labels, fill_value=0)
)

print(fraud_time_analysis)


# ============================================================
# 18. FRAUD PERCENTAGE BY TIME RANGE
# ============================================================

print("\n" + "=" * 60)
print("FRAUD PERCENTAGE BY TIME RANGE")
print("=" * 60)

time_analysis = (
    df.groupby(
        "TimeRange",
        observed=False
    )
    .agg(
        TotalTransactions=("Class", "count"),
        FraudTransactions=("Class", "sum")
    )
    .reindex(time_labels)
)

time_analysis["FraudPercentage"] = (
    time_analysis["FraudTransactions"]
    / time_analysis["TotalTransactions"]
    * 100
)

print(time_analysis)


# ============================================================
# 19. TOP 10 FRAUD TRANSACTIONS
# ============================================================

print("\n" + "=" * 60)
print("TOP 10 FRAUD TRANSACTIONS BY AMOUNT")
print("=" * 60)

top_fraud = (
    df[df["Class"] == 1]
    .sort_values(
        by="Amount",
        ascending=False
    )
    .head(10)
)

print(
    top_fraud[
        [
            "TransactionID",
            "Time",
            "Amount",
            "Class"
        ]
    ]
)


# ============================================================
# 20. HIGH-VALUE FRAUD TRANSACTIONS
# ============================================================

print("\n" + "=" * 60)
print("HIGH-VALUE FRAUD TRANSACTIONS")
print("=" * 60)

high_value_fraud = (
    df[
        (df["Class"] == 1)
        &
        (df["Amount"] > 500)
    ]
    .sort_values(
        by="Amount",
        ascending=False
    )
)

print(
    high_value_fraud[
        [
            "TransactionID",
            "Time",
            "Amount",
            "Class"
        ]
    ].head(20)
)


# ============================================================
# 21. AVERAGE AMOUNT: FRAUD VS LEGITIMATE
# ============================================================

print("\n" + "=" * 60)
print("AVERAGE AMOUNT: FRAUD VS LEGITIMATE")
print("=" * 60)

average_amount = (
    df.groupby("Class")["Amount"]
    .mean()
)

print(average_amount)


# ============================================================
# 22. FRAUD VS LEGITIMATE COUNT GRAPH
# ============================================================

print("\nCreating Fraud vs Legitimate Count Graph...")

plt.figure(figsize=(8, 5))

plt.bar(
    ["Legitimate", "Fraud"],
    [
        legitimate_transactions,
        fraud_transactions
    ]
)

plt.xlabel("Transaction Type")
plt.ylabel("Number of Transactions")
plt.title("Fraud vs Legitimate Transactions")

plt.tight_layout()
plt.show()


# ============================================================
# 23. TRANSACTION AMOUNT DISTRIBUTION
# ============================================================

print("\nCreating Transaction Amount Distribution Graph...")

plt.figure(figsize=(10, 6))

plt.hist(
    legitimate_amount,
    bins=50,
    alpha=0.6,
    label="Legitimate"
)

plt.hist(
    fraud_amount,
    bins=50,
    alpha=0.6,
    label="Fraud"
)

plt.xlabel("Transaction Amount")
plt.ylabel("Number of Transactions")

plt.title(
    "Transaction Amount Distribution: "
    "Fraud vs Legitimate"
)

plt.legend()

plt.tight_layout()
plt.show()


# ============================================================
# 24. FRAUD AMOUNT RANGE GRAPH
# ============================================================

print("\nCreating Fraud Amount Range Graph...")

plt.figure(figsize=(10, 6))

plt.bar(
    fraud_amount_range.index.astype(str),
    fraud_amount_range.values
)

plt.xlabel("Amount Range")
plt.ylabel("Number of Fraud Transactions")

plt.title("Fraud Transactions by Amount Range")

plt.xticks(rotation=20)

plt.tight_layout()
plt.show()


# ============================================================
# 25. FRAUD TIME RANGE GRAPH
# ============================================================

print("\nCreating Fraud Time Range Graph...")

plt.figure(figsize=(10, 6))

plt.bar(
    fraud_time_analysis.index.astype(str),
    fraud_time_analysis.values
)

plt.xlabel("Time Range")
plt.ylabel("Number of Fraud Transactions")

plt.title("Fraud Transactions by Time Range")

plt.xticks(rotation=20)

plt.tight_layout()
plt.show()


# ============================================================
# 26. CLOSE SQL CONNECTION
# ============================================================

conn.close()

print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 60)