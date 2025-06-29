import csv
import os
from collections import defaultdict
from datetime import datetime

expenses = []
monthly_budgets = defaultdict(float)
csv_file = "expenses.csv"
CATEGORIES = ['Food', 'Travel', 'Shopping', 'Utilities', 'Miscellaneous']

# Extract YYYY-MM from a given date
def extract_month(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m")
    except ValueError:
        return None

# Load expenses from CSV
def load_expenses():
    global expenses
    if os.path.exists(csv_file):
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            expenses.clear()
            for row in reader:
                try:
                    row['amount'] = float(row['amount'])
                    expenses.append(row)
                except ValueError:
                    continue
        print("📂 Expenses loaded from file.")
    else:
        print("📁 No previous expense file found.")

# Save expenses and show monthly budget summary
def save_expenses():
    with open(csv_file, mode='w', newline='') as file:
        fieldnames = ['date', 'category', 'amount', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for exp in expenses:
            writer.writerow(exp)
    print("💾 Expenses saved successfully.")
    check_all_month_budgets()

# Add a new expense
def add_expense():
    try:
        date = input("Enter date (YYYY-MM-DD): ")
        month = extract_month(date)
        if not month:
            print("⚠️ Invalid date format. Use YYYY-MM-DD.")
            return

        print("\n📂 Available categories:", ", ".join(CATEGORIES))
        category = input("Enter category: ").title()
        if category not in CATEGORIES:
            print("⚠️ Invalid category. Choose from the list.")
            return

        amount = float(input("Enter amount: ₹"))
        description = input("Enter description: ")
        expense = {'date': date, 'category': category, 'amount': amount, 'description': description}
        expenses.append(expense)
        print(f"✅ Expense of ₹{amount:.2f} added under {category}.")
        check_budget_for_month(month)
    except ValueError:
        print("⚠️ Invalid amount. Please enter a number.")

# View all expenses (flat, ungrouped)
def view_expenses():
    if not expenses:
        print("📝 No expenses recorded yet.")
        return

    sorted_expenses = sorted(expenses, key=lambda x: x['date'])

    print("\n📋 All Expense Records:\n" + "-" * 40)
    print("{:<12} {:<15} {:<10} {}".format("Date", "Category", "Amount", "Description"))
    print("-" * 60)

    for exp in sorted_expenses:
        print("{:<12} {:<15} ₹{:<9.2f} {}".format(
            exp['date'], exp['category'], exp['amount'], exp['description']
        ))

    total_spent = sum(e['amount'] for e in expenses)
    print("\n🧾 Total Expenses Across All Months: ₹{:.2f}".format(total_spent))

# Set or update a monthly budget
def set_budget():
    try:
        month = input("Enter month for budget (YYYY-MM): ")
        datetime.strptime(month, "%Y-%m")
        if month in monthly_budgets:
            print(f"📌 Current budget for {month}: ₹{monthly_budgets[month]:.2f}")
        else:
            print(f"ℹ️ No budget set for {month} yet.")
        amount = float(input(f"Enter new budget for {month}: ₹"))
        monthly_budgets[month] = amount
        print(f"✅ Budget of ₹{amount:.2f} set for {month}.")
        check_budget_for_month(month)
    except ValueError:
        print("⚠️ Invalid input. Use YYYY-MM format and numeric value.")

# Check budget for a specific month
def check_budget_for_month(month):
    total_spent = sum(exp['amount'] for exp in expenses if extract_month(exp['date']) == month)
    budget = monthly_budgets.get(month, 0.0)
    print(f"\n📅 Month: {month}")
    print(f"🧾 Total spent: ₹{total_spent:.2f}")
    if budget == 0:
        print("⚠️ No budget set for this month.")
    elif total_spent > budget:
        print("🚨 Budget Exceeded by ₹{:.2f}!".format(total_spent - budget))
    else:
        print("✅ ₹{:.2f} remaining in budget.".format(budget - total_spent))

# Check all months
def check_all_month_budgets():
    months = set(extract_month(exp['date']) for exp in expenses)
    for month in months:
        check_budget_for_month(month)

# Interactive menu
def menu():
    load_expenses()
    while True:
        print("\n📌 Personal Expense Tracker Menu")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Set Monthly Budget")
        print("4. Save Expenses to CSV")
        print("5. Exit")
        choice = input("Select an option (1-5): ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            set_budget()
        elif choice == '4':
            save_expenses()
        elif choice == '5':
            save_expenses()
            print("👋 Exiting. Stay financially fierce!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
