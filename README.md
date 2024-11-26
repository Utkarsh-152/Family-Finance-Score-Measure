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

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the Flask application:
   ```bash
   python app.py

4. Open your browser and navigate to http://127.0.0.1:5000/.

## Usage
**Home Page**
   - Welcome Screen: Provides an overview of the application.
   - Navigate to:
      - Add Data: Input financial details.
      - View Data: View stored financial scores and recommendations.
**Add Data**
   - Enter the required fields:
      - Family ID
      - Member ID
      - Spending Category
      - Amount
      - Income
      - Monthly Expenses
      - Loan Payments
      - Credit Card Spending
      - Savings
   - Submit to calculate scores and save data.
**View Data**
   - Displays stored financial data in a tabular format with calculated scores and recommendations.

## How It Works

1. Data Input:
   - Users enter financial data through the form on the "Add Data" page.
2. Score Calculation:
   - Metrics like Savings-to-Income and Expenses-to-Income are calculated.
   - A weighted financial score is derived.
   - Recommendations are generated based on the score.
3. Data Storage:
   - The input data, along with scores and recommendations, are saved to an Excel file.
4. Data Viewing:
   - Saved data is displayed in a table format on the "View Data" page.

   
## Dependencies
   - Python 3.7+
   - Flask
   - Pandas
   - OpenPyXL (for Excel file handling)
   - Bootstrap (for frontend styling)

