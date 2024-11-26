import pandas as pd
import numpy as np
import os

data_file = "family_financial_score.xlsx"

# Define weights
weights = {
    'Savings_to_Income': 0.30,
    'Expenses_to_Income': 0.25,
    'Loan_to_Income': 0.20,
    'Credit_Card_Spending': 0.15,
    'Spending_Category_Balance': 0.10
}

def calculate_savings_to_income(savings, income):
    return min(savings / income, 1) * 100

def calculate_expenses_to_income(expenses, income):
    return min(expenses / income, 1) * 100

def calculate_loan_to_income(loans, income):
    return min(loans / income, 1) * 100

def spending_category_penalty(category_spending):
    discretionary_categories = ['Entertainment', 'Travel', 'Food']
    discretionary_spending = category_spending.loc[category_spending.index.isin(discretionary_categories)].sum()
    total_spending = category_spending.sum()
    penalty_ratio = discretionary_spending / total_spending if total_spending > 0 else 0
    return max(0, (1 - penalty_ratio) * 100)

def generate_recommendation(metrics):
    financial_score = metrics['Financial_Score']
    recommendations = []
    
    if financial_score >= 70:
        category = 'Excellent'
    elif financial_score >= 50:
        category = 'Good'
    elif financial_score >= 30:
        category = 'Average'
    else:
        category = 'Poor'

    # Generate specific recommendations based on intermediate metrics
    if metrics['Savings_to_Income'] < 40:
        recommendations.append("Increase savings to at least 30% of income.")
    if metrics['Expenses_to_Income'] > 40:
        recommendations.append("Reduce expenses to below 40% of income.")
    if metrics['Loan_to_Income'] > 20:
        recommendations.append("Lower loan payments to less than 20% of income.")
    if metrics['Credit_Card_Spending_Score'] > 25:
        recommendations.append("Cut down on credit card spending.")
    if metrics['Spending_Category_Balance'] < 70:
        recommendations.append("Balance discretionary spending better.")

    return category + ": " + " ".join(recommendations)

def calculate_financial_scores(new_data):
    scores = []
    
    for family_id, group in new_data.groupby('Family_ID'):
        # Extract relevant details
        income = group['Income'].iloc[0]
        savings = group['Savings'].iloc[0]
        expenses = group['Monthly_Expenses'].iloc[0]
        loans = group['Loan_Payments'].iloc[0]
        credit_card = group['Credit_Card_Spending'].iloc[0]

        # Spending by category for penalty
        category_spending = group.groupby('Category')['Amount'].sum()
        category_penalty = spending_category_penalty(category_spending)

        # Calculate individual scores
        savings_to_income_score = calculate_savings_to_income(savings, income)
        expenses_to_income_score = 100 - calculate_expenses_to_income(expenses, income)
        loan_to_income_score = 100 - calculate_loan_to_income(loans, income)
        credit_card_score = max(0, (1 - (credit_card / income)) * 100)

        # Final weighted score
        final_score = (
            savings_to_income_score * weights['Savings_to_Income'] +
            expenses_to_income_score * weights['Expenses_to_Income'] +
            loan_to_income_score * weights['Loan_to_Income'] +
            credit_card_score * weights['Credit_Card_Spending'] +
            category_penalty * weights['Spending_Category_Balance']
        )

        # Generate recommendations
        recommendation = generate_recommendation({
            'Savings_to_Income': savings_to_income_score,
            'Expenses_to_Income': calculate_expenses_to_income(expenses, income),
            'Loan_to_Income': calculate_loan_to_income(loans, income),
            'Credit_Card_Spending_Score': max(0, (credit_card / income) * 100),
            'Spending_Category_Balance': category_penalty,
            'Financial_Score': final_score,
            'Income': income,
            'Monthly_Expenses': expenses,
            'Loan_Payments': loans
        })

        # Append only necessary details to the final output
        for _, row in group.iterrows():
            scores.append({
                'Family_ID': family_id,
                'Member_ID': row['Member_ID'],
                'Category': row['Category'],
                'Amount': row['Amount'],
                'Income': income,
                'Monthly_Expenses': expenses,
                'Loan_Payments': loans,
                'Credit_Card_Spending': credit_card,
                'Savings': savings,
                'Financial_Score': final_score,
                'Recommendation': recommendation
            })
    
    # Create DataFrame
    return pd.DataFrame(scores)


def save_scores_to_excel(data):
    # Columns to save
    required_columns = [
        'Family_ID', 'Member_ID', 'Amount', 'Income', 'Monthly_Expenses',
        'Loan_Payments', 'Credit_Card_Spending', 'Savings', 'Category',
        'Financial_Score', 'Recommendation'
    ]

    # Keep only these columns
    data = data[required_columns]

    # Save to Excel
    if os.path.exists(data_file):
        existing_data = pd.read_excel(data_file)
        updated_data = pd.concat([existing_data, data], ignore_index=True)
    else:
        updated_data = data

    updated_data.to_excel(data_file, index=False)
