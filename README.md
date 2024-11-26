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
## Explanation of Model Logic

### Overview
This Python script calculates **financial scores** for families and provides recommendations to improve their financial health. It evaluates savings, expenses, loans, credit card spending, and spending habits across discretionary categories.

---

### Key Metrics
The model calculates five primary metrics:

1. **Savings-to-Income**:
   - Measures the percentage of income saved.
   - Formula: `min(savings / income, 1) * 100`.

2. **Expenses-to-Income**:
   - Evaluates the proportion of income spent on monthly expenses.
   - Formula: `100 - min(expenses / income, 1) * 100`.

3. **Loan-to-Income**:
   - Assesses loan repayment burden relative to income.
   - Formula: `100 - min(loans / income, 1) * 100`.

4. **Credit Card Spending**:
   - Scores credit card spending efficiency.
   - Formula: `max(0, (1 - (credit_card / income)) * 100)`.

5. **Spending Category Balance**:
   - Penalizes excessive discretionary spending (e.g., on entertainment, travel, food) relative to total spending.
   - **Formula**:
     
     $$ \text{Penalty} = \max \left( 0, \left( 1 - \frac{\text{Discretionary Spending}}{\text{Total Spending}} \right) \times 100 \right) $$


---

### Final Financial Score
The **financial score** is a weighted combination of the above metrics. Each metric is weighted based on its importance:

| Metric                    | Weight |
|---------------------------|--------|
| Savings-to-Income         | 0.30   |
| Expenses-to-Income        | 0.25   |
| Loan-to-Income            | 0.20   |
| Credit Card Spending      | 0.15   |
| Spending Category Balance | 0.10   |

**Formula:**

$$ \text{Final Score} = (\text{Savings-to-Income Score} \times 0.30) + (\text{Expenses-to-Income Score} \times 0.25) + (\text{Loan-to-Income Score} \times 0.20) + (\text{Credit Card Score} \times 0.15) + (\text{Category Penalty} \times 0.10) $$


---

### Recommendations
Based on the **financial score** and metric thresholds, the model categorizes financial health and generates recommendations:

#### Score Categories
| Financial Score Range | Category   |
|-----------------------|------------|
| ≥ 70                 | Excellent  |
| 50–69                | Good       |
| 30–49                | Average    |
| < 30                 | Poor       |

#### Specific Recommendations
- **Savings-to-Income**: Suggests increasing savings if less than 40% of income.
- **Expenses-to-Income**: Advises reducing expenses to below 40% of income.
- **Loan-to-Income**: Recommends lowering loans to below 20% of income.
- **Credit Card Spending**: Suggests minimizing credit card usage if excessive.
- **Spending Category Balance**: Encourages balancing discretionary and essential spending.

---

### Data Processing
1. **Input Data**:
   - Family financial data grouped by `Family_ID` and `Member_ID`.
   - Includes `Income`, `Savings`, `Monthly_Expenses`, `Loan_Payments`, `Credit_Card_Spending`, and spending by `Category`.

2. **Metrics Calculation**:
   - Metrics are calculated for each family based on aggregated values.

3. **Data Aggregation**:
   - Outputs include:
     - Family and member IDs
     - Income, expenses, loans, and savings details
     - Financial score
     - Recommendations

4. **Excel Output**:
   - Saves results to `family_financial_score.xlsx`.
   - Appends data if the file exists; creates a new file otherwise.

---

### Benefits
1. **Comprehensive Analysis**: Evaluates financial health across multiple aspects.
2. **Custom Recommendations**: Provides actionable suggestions for improvement.
3. **Automated Reporting**: Supports ongoing financial tracking and reporting.

---


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Utkarsh-152/Family-Finance-Score-Measure.git
   cd Family-Finance-Score-Measure

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

---

## Streamlit Financial Score Dashboard

This is a simple Streamlit app that allows you to interact with the financial scoring model, simulate changes in financial data, and view personalized recommendations for improving your financial score. The app provides a visual interface where you can:

- View stored financial data and scores.
- Simulate changes such as increasing savings or reducing expenses.
- View recommendations on how to improve your financial score.

### Features

1. **View Data**:
    - Displays the stored financial data in a tabular format.
    - Shows a bar chart visualizing the financial scores of each family.

2. **Simulate Changes**:
    - Lets users simulate changes in their financial data (e.g., increase savings, reduce expenses, etc.).
    - Recalculates and displays the new financial score after the simulated changes.
    - Shows the improvement in the financial score based on the applied changes.

3. **Personalized Recommendations**:
    - Provides tailored recommendations for improving the financial score, such as reducing discretionary spending or increasing savings.

### Prerequisites

Before using this app, ensure that you have the following:

- **Streamlit** for the web interface.
- **Plotly** for data visualization.
- An existing Excel file (`family_financial_score.xlsx`) with the stored financial data. If no data is available, you can add data via the Flask app first.

### Requirements

You need to install the required dependencies for Streamlit and Plotly.

#### Install Dependencies 
      ```bash
      pip install streamlit plotly pandas openpyxl

### Running the App

#### Start the Streamlit App
      ```bash
      streamlit run streamlit_app.py

#### Open the App
- After running the command, you will see a URL in the terminal, typically http://localhost:8501.
- Open your web browser and navigate to this URL to access the app.

### App Layout
#### Sidebar
The app has a sidebar with two main options:
- **View Data**: Displays the stored financial data and a bar chart of financial scores.
- **Simulate Changes**: Allows users to simulate changes like increasing savings or reducing expenses and see how these changes impact the financial score.
#### Main Area
- **View Data**: Displays a table with the stored financial data and a bar chart visualizing the financial scores of families.
- **Simulate Changes**: Allows users to input percentages for increasing savings, reducing expenses, and reducing credit card spending. After applying these changes, it will calculate and display the new financial score and provide recommendations on how to improve financial health.

---

### How It Works

#### Data Viewing
1. When you select the View Data option, the app loads and displays the financial data stored in the family_financial_score.xlsx file.
2. It also generates a bar chart that visualizes the financial scores of different families.
#### Simulating Financial Changes
1. The Simulate Changes option lets you adjust various financial metrics (e.g., increase savings, reduce monthly expenses).
2. The app will recalculate the financial score based on these changes and show how the score improves.
#### Recommendations
1. Based on the new financial score, the app will generate and display recommendations to help improve the score further. For example:
   - "Reduce discretionary spending by 10% to improve your score by X points."
