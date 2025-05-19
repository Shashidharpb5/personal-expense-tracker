import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os

# === Database path ===
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

# === Add new expense ===
def add_expense(date, category, description, amount):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (date, category, description, amount)
        VALUES (?, ?, ?, ?)
    ''', (date, category, description, amount))
    conn.commit()
    conn.close()

# === Load all data ===
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    return df

# === Streamlit UI ===
def main():
    st.title("💸 Personal Expense Tracker")
    st.sidebar.title("Menu")

    create_table()  # Ensure table exists

    menu = ["Add Expense", "Show Summary", "Bar Plot", "Pie Chart"]
    choice = st.sidebar.radio("Choose an action", menu)

    if choice == "Add Expense":
        st.subheader("➕ Add New Expense")

        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Beverage", "Other"])
        description = st.text_input("Description")
        amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")

        if st.button("Add"):
            add_expense(str(date), category, description, float(amount))
            st.success("✅ Expense Added Successfully!")

    elif choice == "Show Summary":
        st.subheader("📊 Summary of Expenses")
        df = load_data()

        if df.empty:
            st.warning("⚠️ No expenses recorded.")
        else:
            st.write(df)
            total = df["amount"].sum()
            st.info(f"**Total Expenses: ₹{total:.2f}**")

    elif choice == "Bar Plot":
        st.subheader("📈 Bar Plot of Expenses")
        df = load_data()

        if df.empty:
            st.warning("⚠️ No data to show.")
        else:
            df['date'] = pd.to_datetime(df['date'])
            summary = df.groupby(['date', 'category'])['amount'].sum().unstack().fillna(0)

            fig, ax = plt.subplots(figsize=(10, 6))
            summary.plot(kind='bar', stacked=True, ax=ax)

            plt.title('Expenses by Date and Category')
            plt.xlabel('Date')
            plt.ylabel('Amount (₹)')
            plt.xticks(rotation=45)
            plt.legend(title='Category')
            plt.tight_layout()

            # Add value labels
            for container in ax.containers:
                ax.bar_label(container, label_type='edge')

            st.pyplot(fig)

    elif choice == "Pie Chart":
        st.subheader("🥧 Pie Chart of Expenses by Category")
        df = load_data()

        if df.empty:
            st.warning("⚠️ No data to show.")
        else:
            category_summary = df.groupby('category')['amount'].sum()
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(category_summary, labels=category_summary.index, autopct='%1.1f%%', startangle=140, shadow=True)
            ax.set_title("Expense Distribution by Category")
            ax.axis('equal')
            st.pyplot(fig)

if __name__ == '__main__':
    main()
