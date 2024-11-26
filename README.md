# Family Financial Score Web Application

## Overview

The **Family Financial Score Web Application** is a Flask-based tool designed to help families manage their finances effectively. By entering financial data such as income, savings, expenses, loan payments, and credit card spending, users can calculate a **financial score** and receive recommendations on improving their financial stability.

The application also provides an interface to view saved data and financial scores.

---

## Features

1. **Financial Data Input**:
   - Input categories include income, savings, monthly expenses, loan payments, and credit card spending.
   - Users can specify spending categories (e.g., Entertainment, Travel, Food, Education).

2. **Score Calculation**:
   - The financial score is calculated using weighted metrics such as:
     - Savings-to-Income ratio
     - Expenses-to-Income ratio
     - Loan-to-Income ratio
     - Credit Card Spending
     - Spending Category Balance
   - Personalized recommendations are provided based on the calculated score.

3. **Data Persistence**:
   - User input is stored in an Excel file (`family_financial_score.xlsx`) for future reference.

4. **User-Friendly Interface**:
   - Simple web interface to input and view data.
   - Bootstrap for responsive design.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/family-financial-score.git
   cd family-financial-score
