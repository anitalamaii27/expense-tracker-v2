from flask import Flask, render_template, request, redirect, url_for, Response
import csv
import os
from datetime import datetime

app = Flask(__name__)
CSV_FILE = 'expenses.csv'

# Read expenses from the CSV file
def read_expenses():
    expenses = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append(row)
    return expenses

# Write expenses to the CSV file
def write_expenses(expenses):
    with open(CSV_FILE, 'w', newline='') as file:
        fieldnames = ["date", "description", "amount", "category"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    amount = float(request.form['amount'])
    category = request.form['category']
    date = request.form['date']
    description = request.form['description']

    new_expense = {
        'amount': amount,
        'category': category,
        'date': date,
        'description': description
    }

    expenses = read_expenses()  # Read current expenses from CSV
    expenses.append(new_expense)  # Add new expense
    write_expenses(expenses)  # Save updated expenses to CSV

    return redirect(url_for('index'))

@app.route('/')
def index():
    expenses = read_expenses()  # Read expenses from CSV
    total = sum(float(e['amount']) for e in expenses)  # Calculate total amount
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/delete/<int:index>', methods=['GET'])
def delete_expense(index):
    expenses = read_expenses()  # Read expenses from CSV
    if 0 <= index < len(expenses):
        del expenses[index]  # Remove expense at specified index
        write_expenses(expenses)  # Save updated expenses to CSV
    return redirect(url_for('index'))

@app.route('/export')
def export_csv():
    expenses = read_expenses()  # Read expenses from CSV
    output = "date,description,amount,category\n"
    for expense in expenses:
        output += f"{expense['date']},{expense['description']},{expense['amount']},{expense['category']}\n"
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=expenses.csv"})

if __name__ == '__main__':
    app.run(debug=True, port=5050)
