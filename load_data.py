import pandas as pd
from sqlalchemy import create_engine
import urllib


# ============================================================
# 1. EXCEL FILE PATH
# ============================================================

file_path = r"C:\Users\DELL\Desktop\AI_Financial_Crime_Intelligence_Platform\creditcard_project.xlsx"


# ============================================================
# 2. READ EXCEL FILE
# ============================================================

print("Reading Excel file...")

df = pd.read_excel(file_path)

print("Excel file loaded successfully!")
print("Rows:", len(df))
print("Columns before cleaning:", len(df.columns))


# ============================================================
# 3. CLEAN COLUMN NAMES
# ============================================================

print("\nOriginal Columns:")
print(df.columns.tolist())


# Fix TransactionID spelling
df.rename(
    columns={
        "TransctionID": "TransactionID"
    },
    inplace=True
)


# Remove unnecessary Excel columns
df = df[
    [
        "TransactionID",
        "Time",
        "V1",
        "V2",
        "V3",
        "V4",
        "V5",
        "V6",
        "V7",
        "V8",
        "V9",
        "V10",
        "V11",
        "V12",
        "V13",
        "V14",
        "V15",
        "V16",
        "V17",
        "V18",
        "V19",
        "V20",
        "V21",
        "V22",
        "V23",
        "V24",
        "V25",
        "V26",
        "V27",
        "V28",
        "Amount",
        "Class"
    ]
]


print("\nColumns after cleaning:")
print(df.columns.tolist())

print("Rows after cleaning:", len(df))
print("Columns after cleaning:", len(df.columns))


# ============================================================
# 4. SQL SERVER CONNECTION
# ============================================================

server = r"localhost\SQLEXPRESS"
database = "FinancialCrimeDB"

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

params = urllib.parse.quote_plus(connection_string)

engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params}"
)

print("\nConnected to SQL Server successfully!")


# ============================================================
# 5. LOAD DATA INTO SQL SERVER
# ============================================================

print("\nStarting data import...")

df.to_sql(
    name="Transactions",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=5000
)

print("\nData imported successfully!")


# ============================================================
# 6. FINAL MESSAGE
# ============================================================

print("\n====================================")
print("ETL PROCESS COMPLETED SUCCESSFULLY")
print("====================================")

print("Rows imported:", len(df))
print("Target table: Transactions")
print("Database: FinancialCrimeDB")