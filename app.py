from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
from model import calculate_financial_scores, save_scores_to_excel, calculate_expenses_to_income,calculate_loan_to_income,calculate_savings_to_income,spending_category_penalty

app = Flask(__name__)

# File to save data
data_file = "family_financial_score.xlsx"

# CustomData class to structure the form data
class CustomData:
    def __init__(self, Amount, Income, Monthly_Expenses, Loan_Payments, Credit_Card_Spending, Family_ID, Member_ID, Savings, Category='Other'):
        self.Amount = Amount
        self.Income = Income
        self.Monthly_Expenses = Monthly_Expenses
        self.Loan_Payments = Loan_Payments
        self.Credit_Card_Spending = Credit_Card_Spending
        self.Family_ID = Family_ID
        self.Member_ID = Member_ID
        self.Savings = Savings
        self.Category = Category  # Category defaults to 'Other'

    def get_data_as_data_frame(self):
        custom_data_input_dict = {
            "Amount": [self.Amount],
            "Income": [self.Income],
            "Monthly_Expenses": [self.Monthly_Expenses],
            "Loan_Payments": [self.Loan_Payments],
            "Credit_Card_Spending": [self.Credit_Card_Spending],
            "Family_ID": [self.Family_ID],
            "Member_ID": [self.Member_ID],
            "Savings": [self.Savings],
            "Category": [self.Category]
        }
        return pd.DataFrame(custom_data_input_dict)

# Route to display home page
@app.route('/')
def home():
    return render_template('home.html')

# Route to add data via form
@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        # Collect data from form
        Amount = int(request.form['Amount'])
        Income = int(request.form['Income'])
        Monthly_Expenses = int(request.form['Monthly_Expenses'])
        Loan_Payments = int(request.form['Loan_Payments'])
        Credit_Card_Spending = int(request.form['Credit_Card_Spending'])
        Family_ID = request.form['Family_ID']
        Member_ID = request.form['Member_ID']
        Savings = int(request.form['Savings'])
        Category = request.form['Category']  # Collect the Category

        # Convert to DataFrame
        data = CustomData(Amount, Income, Monthly_Expenses, Loan_Payments, Credit_Card_Spending, Family_ID, Member_ID, Savings, Category)
        df = data.get_data_as_data_frame()

        # Calculate financial scores
        scores_df = calculate_financial_scores(df)

        # Save to Excel
        save_scores_to_excel(scores_df)

        return render_template('home.html', message="Data added successfully!")

    return render_template('index.html')

# Route to view data stored in the file
@app.route('/view_data')
def view_data():
    if os.path.exists(data_file):
        data = pd.read_excel(data_file)

        # Columns to display
        columns_to_display = [
            'Family_ID', 'Member_ID', 'Amount', 'Income', 'Monthly_Expenses',
            'Loan_Payments', 'Credit_Card_Spending', 'Savings', 'Category',
            'Financial_Score', 'Recommendation'
        ]

        # Filter columns
        data = data[columns_to_display]

        # Display in table format
        return render_template('view_data.html', data=data.to_html(classes='table table-striped'))

    return render_template('home.html', message="No data available.")


if __name__ == '__main__':
    app.run(debug=True)
