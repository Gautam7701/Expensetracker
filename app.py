from flask import Flask, render_template, request, redirect
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')
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

@app.route('/')
def index():
    expenses = load_expenses()
    total = sum(e["amount"] for e in expenses)
    return render_template("index.html", expenses=expenses, total=total)

@app.route('/add', methods=['POST'])
def add():
    amount = request.form.get("amount")
    category = request.form.get("category")
    if amount and category:
        try:
            amount = float(amount)
            date = datetime.now().strftime("%Y-%m-%d")
            expenses = load_expenses()
            expenses.append({"amount": amount, "category": category, "date": date})
            save_expenses(expenses)
        except ValueError:
            pass
    return redirect('/')

@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    expenses = load_expenses()
    if 0 <= index < len(expenses):
        del expenses[index]  # Delete the expense at the given index
        save_expenses(expenses)  # Save the updated list of expenses
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

