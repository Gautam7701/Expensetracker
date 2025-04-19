import os
from datetime import datetime
import csv

EXPENSE_FILE = "expenses.txt"

def load_expenses():
    expenses = []
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "r") as file:
            for line in file:
                try:
                    amount, category, date = line.strip().split("|")
                    expenses.append({
                        "amount": float(amount),
                        "category": category,
                        "date": date
                    })
                except ValueError:
                    continue
    return expenses

def save_expenses(expenses):
    with open(EXPENSE_FILE, "w") as file:
        for expense in expenses:
            file.write(f"{expense['amount']}|{expense['category']}|{expense['date']}\n")

def add_expense(expenses, amount, category):
    date = datetime.now().strftime("%Y-%m-%d")
    expenses.append({"amount": amount, "category": category, "date": date})
    save_expenses(expenses)
    print(f"Added: ${amount:.2f} | {category} | {date}")

def view_expenses(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    print("\n--- All Expenses ---")
    for i, e in enumerate(expenses, 1):
        print(f"{i}. ${e['amount']:.2f} - {e['category']} ({e['date']})")

def show_summary(expenses):
    if not expenses:
        print("No expenses to summarize.")
        return
    total = sum(e["amount"] for e in expenses)
    print(f"\nTotal Spent: ${total:.2f}")
    category_summary = {}
    for e in expenses:
        category_summary[e["category"]] = category_summary.get(e["category"], 0) + e["amount"]
    print("By Category:")
    for cat, amt in category_summary.items():
        print(f"  {cat}: ${amt:.2f}")

def search_expenses(expenses, keyword):
    found = [e for e in expenses if keyword.lower() in e["category"].lower() or keyword in e["date"]]
    if not found:
        print("No matches.")
        return
    for i, e in enumerate(found, 1):
        print(f"{i}. ${e['amount']} - {e['category']} ({e['date']})")

def export_to_csv(expenses, filename="expenses.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["amount", "category", "date"])
        writer.writeheader()
        writer.writerows(expenses)
    print(f"Exported to {filename}")

def delete_expense(expenses, index):
    if 1 <= index <= len(expenses):
        removed = expenses.pop(index - 1)
        save_expenses(expenses)
        print(f"Deleted: ${removed['amount']} | {removed['category']}")
    else:
        print("Invalid index.")

def main():
    expenses = load_expenses()
    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add Expense\n2. View Expenses\n3. Summary\n4. Search\n5. Export CSV\n6. Delete\n7. Exit")
        choice = input("Choose: ")
        if choice == "1":
            try:
                amt = float(input("Amount: "))
                cat = input("Category: ")
                add_expense(expenses, amt, cat)
            except:
                print("Invalid amount.")
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            show_summary(expenses)
        elif choice == "4":
            keyword = input("Search by category or date (YYYY-MM-DD): ")
            search_expenses(expenses, keyword)
        elif choice == "5":
            export_to_csv(expenses)
        elif choice == "6":
            view_expenses(expenses)
            try:
                idx = int(input("Delete which number? "))
                delete_expense(expenses, idx)
            except:
                print("Invalid number.")
        elif choice == "7":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
