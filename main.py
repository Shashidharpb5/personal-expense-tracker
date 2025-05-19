import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    conn = sqlite3.connect('expenses.db')
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    return df

def main():
    while True:
        print("\nChoose an option:")
        print("1. Add Expense")
        print("2. Show Summary")
        print("3. Show Bar Plot of Expenses")
        print("4. Show Pie Chart of Expenses by Category")
        print("5. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            # Add Expense
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            description = input("Enter description: ")
            while True:
                try:
                    amount = float(input("Enter amount: "))
                    break
                except ValueError:
                    print("Invalid amount. Please enter a numeric value.")
            
            conn = sqlite3.connect("expenses.db")
            c = conn.cursor()
            c.execute("INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
                      (date, category, description, amount))
            conn.commit()
            conn.close()
            print("Expense added successfully!")

        elif choice == "2":
            df = load_data()
            if df.empty:
                print("No data found.")
            else:
                print("\n=== Summary ===")
                print("Total Expenses: ₹", df["amount"].sum())

        elif choice == "3":
            df = load_data()
            if df.empty:
                print("No data found.")
            else:
                df['date'] = pd.to_datetime(df['date'])
                summary = df.groupby(['date', 'category'])['amount'].sum().unstack().fillna(0)
                summary.plot(kind='bar', stacked=True, figsize=(10,6))

                plt.title('Expenses by Date and Category')
                plt.xlabel('Date')
                plt.ylabel('Amount (₹)')
                plt.legend(title='Category')
                plt.xticks(rotation=45)
                plt.tight_layout()

                # Adding value labels on bars
                ax = plt.gca()
                for container in ax.containers:
                    ax.bar_label(container, label_type='edge')

                plt.show()

        elif choice == "4":
            df = load_data()
            if df.empty:
                print("No data found.")
            else:
                category_summary = df.groupby('category')['amount'].sum()
                plt.figure(figsize=(8,8))
                plt.pie(category_summary, labels=category_summary.index, autopct='%1.1f%%', startangle=140, shadow=True)
                plt.title('Expense Distribution by Category')
                plt.axis('equal')
                plt.show()

        elif choice == "5":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
