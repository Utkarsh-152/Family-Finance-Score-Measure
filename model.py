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

def generate_recommendation(row):
    # Categorize the financial score
    if row['Financial_Score'] >= 80:
        category = 'Excellent'
    elif row['Financial_Score'] >= 60:
        category = 'Good'
    elif row['Financial_Score'] >= 40:
        category = 'Average'
    else:
        category = 'Poor'
    
    # Provide recommendations based on individual components
    recommendations = []
    if row['Savings_to_Income'] < 20:  # Example threshold
        recommendations.append("Increase your savings to at least 20% of your income.")
    if row['Expenses_to_Income'] > 60:  # Example threshold
        recommendations.append("Try to reduce your monthly expenses to below 60% of your income.")
    if row['Loan_to_Income'] > 30:  # Example threshold
        recommendations.append("Aim to lower your loan payments to less than 30% of your income.")
    if row['Credit_Card_Spending_Score'] > 40:  # Example threshold
        recommendations.append("Reduce your credit card spending to improve your score.")
    if row['Spending_Category_Balance'] < 70:  # Example threshold
        recommendations.append("Balance discretionary and non-discretionary spending categories.")
    
    return category + ": " + " ".join(recommendations)

def calculate_financial_scores(new_data):
    scores = []
    
    # Iterate through each family in the grouped data
    for family_id, group in new_data.groupby('Family_ID'):
        # Extract relevant details
        income = group['Income'].iloc[0]  # Assume constant income for a family
        savings = group['Savings'].iloc[0]
        expenses = group['Monthly_Expenses'].iloc[0]
        loans = group['Loan_Payments'].iloc[0]
        credit_card = group['Credit_Card_Spending'].iloc[0]
        
        # Spending by category for penalty
        category_spending = group.groupby('Category')['Amount'].sum()
        category_penalty = spending_category_penalty(category_spending)
        
        # Calculate individual sub-scores
        savings_to_income_score = calculate_savings_to_income(savings, income)
        expenses_to_income_score = 100 - calculate_expenses_to_income(expenses, income)
        loan_to_income_score = 100 - calculate_loan_to_income(loans, income)
        credit_card_score = max(0, (1 - (credit_card / income)) * 100)
        
        # Weighted score calculation
        final_score = (
            savings_to_income_score * weights['Savings_to_Income'] +
            expenses_to_income_score * weights['Expenses_to_Income'] +
            loan_to_income_score * weights['Loan_to_Income'] +
            credit_card_score * weights['Credit_Card_Spending'] +
            category_penalty * weights['Spending_Category_Balance']
        )
        
        # Append all the details to the scores list
        for _, row in group.iterrows():
            scores.append({
                'Family_ID': family_id,
                'Member_ID': row['Member_ID'],
                'Category': row['Category'],
                'Amount': row['Amount'],
                'Income': income,  # Assumed constant income for the family
                'Monthly_Expenses': expenses,
                'Loan_Payments': loans,
                'Credit_Card_Spending': credit_card,
                'Savings': savings,
                'Savings_to_Income': savings_to_income_score,
                'Expenses_to_Income': 100 - expenses_to_income_score,  # Reverse percentage
                'Loan_to_Income': 100 - loan_to_income_score,
                'Credit_Card_Spending_Score': credit_card_score,
                'Spending_Category_Balance': category_penalty,
                'Financial_Score': final_score
            })
    
    # Create the DataFrame
    scores_df = pd.DataFrame(scores)

    # Add recommendation column
    scores_df['Recommendation'] = scores_df.apply(generate_recommendation, axis=1)

    return scores_df

def save_scores_to_excel(data):
    print("Saving the following data:")
    print(data.head())  # Debug the first few rows

    required_columns = [
        'Family_ID', 'Member_ID', 'Amount', 'Income', 'Monthly_Expenses', 
        'Loan_Payments', 'Credit_Card_Spending', 'Savings', 'Category', 
        'Financial_Score', 'Recommendation'
    ]
    
    missing_columns = [col for col in required_columns if col not in data.columns]
    
    if missing_columns:
        print(f"Error: Missing columns - {', '.join(missing_columns)}")
        return

    if os.path.exists(data_file):
        existing_data = pd.read_excel(data_file)
        updated_data = pd.concat([existing_data, data], ignore_index=True)
    else:
        updated_data = data

    updated_data.to_excel(data_file, index=False)
