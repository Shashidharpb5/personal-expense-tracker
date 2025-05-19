# utils.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import fetch_expenses

def load_data():
    conn = sqlite3.connect('expenses.db')
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
    return df


def show_summary(df):
    print("\n=== Summary ===")
    print(df.groupby("Category")["Amount"].sum())

def plot_expenses(df):
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Category", y="Amount", data=df.groupby("Category")["Amount"].sum().reset_index(), palette="Set2")
    plt.title("Total Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()