import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data  # Make sure this function returns your expense dataframe

st.title("Personal Expense Tracker")

df = load_data()

if df.empty:
    st.write("No data found.")
else:
    st.subheader("Expense Summary")
    total_expenses = df["amount"].sum()
    st.write(f"**Total Expenses:** ₹ {total_expenses}")

    st.subheader("Expenses Data")
    st.dataframe(df)

    st.subheader("Bar Plot of Expenses by Date and Category")
    df['date'] = pd.to_datetime(df['date'])
    summary = df.groupby(['date', 'category'])['amount'].sum().unstack().fillna(0)
    fig, ax = plt.subplots(figsize=(10, 6))
    summary.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Expenses by Date and Category')
    ax.set_xlabel('Date')
    ax.set_ylabel('Amount (₹)')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Pie Chart of Expenses by Category")
    category_summary = df.groupby('category')['amount'].sum()
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    ax2.pie(category_summary, labels=category_summary.index, autopct='%1.1f%%', startangle=140, shadow=True)
    ax2.set_title('Expense Distribution by Category')
    ax2.axis('equal')
    st.pyplot(fig2)
