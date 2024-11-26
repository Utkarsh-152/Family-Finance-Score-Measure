import streamlit as st
import pandas as pd
import plotly.express as px
import os
from model import calculate_financial_scores, generate_recommendation

DATA_FILE = "family_financial_score.xlsx"

def load_data():
    if not os.path.exists(DATA_FILE):
        st.warning("No data file found. Add data using the Flask app first.")
        return pd.DataFrame()
    return pd.read_excel(DATA_FILE)

# App layout
st.title("Financial Score Dashboard")
st.sidebar.header("Options")

# Options
view_data = st.sidebar.checkbox("View Data", value=True)
add_simulation = st.sidebar.checkbox("Simulate Changes", value=False)

data = load_data()

if view_data:
    st.subheader("Financial Data Overview")
    
    if data.empty:
        st.info("No data available to display.")
    else:
        st.write("Here is the stored financial data:")
        st.dataframe(data)

        # Visualization: Financial Scores per Family
        st.subheader("Financial Score Visualization")
        score_fig = px.bar(
            data,
            x="Family_ID",
            y="Financial_Score",
            color="Financial_Score",
            title="Financial Scores by Family",
            labels={"Financial_Score": "Score"},
        )
        st.plotly_chart(score_fig)

if add_simulation:
    st.subheader("Simulate Financial Changes")

    if data.empty:
        st.info("Add financial data first using the Flask app.")
    else:
        # Select a family to simulate
        selected_family = st.selectbox("Select a Family ID", data["Family_ID"].unique())
        family_data = data[data["Family_ID"] == selected_family]

        # Display family financial data
        st.write(f"Current Financial Data for Family {selected_family}:")
        st.dataframe(family_data)

        # Simulate changes
        savings = st.number_input("Increase Savings (%)", min_value=0, max_value=100, step=5)
        expenses = st.number_input("Reduce Monthly Expenses (%)", min_value=0, max_value=100, step=5)
        credit_card = st.number_input("Reduce Credit Card Spending (%)", min_value=0, max_value=100, step=5)

        # Apply changes
        if st.button("Simulate"):
            simulated_data = family_data.copy()
            simulated_data["Savings"] += simulated_data["Savings"] * (savings / 100)
            simulated_data["Monthly_Expenses"] -= simulated_data["Monthly_Expenses"] * (expenses / 100)
            simulated_data["Credit_Card_Spending"] -= simulated_data["Credit_Card_Spending"] * (credit_card / 100)

            # Calculate new scores
            scores_df = calculate_financial_scores(simulated_data)
            new_score = scores_df["Financial_Score"].iloc[0]
            current_score = family_data["Financial_Score"].iloc[0]

            # Display results
            st.write(f"**Current Score:** {current_score:.2f}")
            st.write(f"**New Score After Simulation:** {new_score:.2f}")
            improvement = new_score - current_score
            st.success(f"Score Improvement: {improvement:.2f} points")

            # Recommendations
            st.subheader("Recommendations for Improvement")
            recommendations = generate_recommendation({
                'Savings_to_Income': scores_df["Savings"].iloc[0],
                'Expenses_to_Income': scores_df["Monthly_Expenses"].iloc[0],
                'Loan_to_Income': scores_df["Loan_Payments"].iloc[0],
                'Credit_Card_Spending_Score': scores_df["Credit_Card_Spending"].iloc[0],
                'Spending_Category_Balance': 80,  
                'Financial_Score': new_score,
                'Income': family_data["Income"].iloc[0],
                'Monthly_Expenses': family_data["Monthly_Expenses"].iloc[0],
                'Loan_Payments': family_data["Loan_Payments"].iloc[0]
            })
            st.write(recommendations)
