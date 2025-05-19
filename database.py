import sqlite3
import os
import pandas as pd

# === Get absolute database path ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "expenses.db")

# === Create table if not exists ===
def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# === Add a new expense ===
def add_expense(date, category, description, amount):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (date, category, description, amount)
        VALUES (?, ?, ?, ?)
    ''', (date, category, description, amount))
    conn.commit()
    conn.close()

# === Load all data as DataFrame ===
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    return df
