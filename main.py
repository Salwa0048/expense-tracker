import csv
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

FILENAME="expenses.csv"

if not os.path.exists(FILENAME):
    with open(FILENAME, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Category', 'Amount'])


def add_expense():
    category= input("Enter the category of the expense: ")
    amount = float(input("Enter the amount of the expense: "))
    date = input("Enter the date of the expense (YYYY-MM-DD) or leave blank for today: ")

    if date.strip() == "":
        date = datetime.now().strftime("%Y-%m-%d")

    with open(FILENAME, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount])

        print(f"Expense added: {date}, {category}, ${amount:.2f}")


def view_expenses():
    df=pd.read_csv(FILENAME)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)
    print(df) 

def reset_expenses():
    confirm = input("Are you sure you want to reset all expenses? This cannot be undone. (yes/no): ")
    if confirm.lower() == "yes":
        with open(FILENAME, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Amount'])
        print("All expenses have been reset.")
    else:
        print("Reset cancelled.")


def monthly_summary():
    df = pd.read_csv(FILENAME)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df.dropna(inplace=True)

    print("\nMONTHLY EXPENSES SUMMARY:")
    monthly = df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum()
    print(monthly)

    print("\nMonthly Breakdown by Category:")
    breakdown = df.groupby([df['Date'].dt.to_period('M'), 'Category'])['Amount'].sum()
    print(breakdown.unstack(fill_value=0))

    breakdown.unstack(fill_value=0).plot(kind='bar', stacked=True)
    plt.title('Monthly Expenses by Category')
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.tight_layout()
    plt.show()

def total_expenses():
    df = pd.read_csv(FILENAME)
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    total = df['Amount'].sum()
    print(f"\nTotal Expenses: ${total:.2f}")

def main():
    while True:
        print("Welcome to the Expense Tracker!")
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Monthly Summary")
        print("4. Total Expenses")
        print("5.Reset Expenses")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            monthly_summary()
        elif choice == '4':
            print("Calculating total expenses...")
            total_expenses()
        elif choice == '5':
            reset_expenses()
            print("resetting expenses...")
            break
        elif choice == '6':
            print("Exiting the Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
     main()
# This code is a simple expense tracker that allows users to add expenses, view them, and generate monthly summaries.




