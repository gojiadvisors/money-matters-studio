# session_defaults.py

import streamlit as st
import datetime

this_year = datetime.datetime.now().year

DEFAULTS = {
    # --- Shared FIRE / Real Estate / Investment Defaults ---
    "user_age": 35,
    "liquid_assets": 300000,
    "retirement_assets": 400000,
    "illiquid_assets": 0,
    "include_illiquid": False,
    "annual_savings": 30000,
    "savings_growth_scenario": "Flat (0.0%)",
    "return_option": "Moderate Growth (7.0%)",
    "fire_expenses": 80000,
    "withdrawal_option": "Moderate (3.5%)",
    "inflation_option": "Average (2.5%)",
    "adjust_fire_expenses_for_inflation": True,

    # --- Real Estate Planner Defaults ---
    "purchase_year": this_year,
    "purchase_price": 400000,
    "down_payment_pct": 25.0,
    "loan_term": 30,
    "interest_rate": 3.0,
    "rental_growth_rate": 1.5,
    "run_model": False,
    "appreciation_rate": 3.0,
    "mortgage_years": 30,
    "annual_rent": 24000,
    "annual_expenses": 5000,
    "years_held": 15,
    "closing_costs": 10000.0,
    "renovation_costs": 15000.0,

    # --- Lifestyle Budgeter Defaults ---
    "annual_income": 80000,
    "household_type": "Married with Kids",
    "location_tier": "Major Metro Area",
    "budget_template": "🏡 Suburban Comfort ($$)",
    "col_multiplier": 1.35,
    "use_budget_template_for_fire": True,

    # --- Expense Template ---
    "expense_template": {
        "Housing": 2200, "Utilities": 300, "Food": 800, "Transportation": 500,
        "Insurance": 400, "Phone/Internet": 150, "Childcare": 600, "Health & Wellness": 250,
        "Subscriptions": 100, "Discretionary": 300, "Shopping": 250, "Personal Care": 150,
        "Travel": 300, "Other": 200, "Investments": 600,
        "Education": 300, "Giving": 100
    },

    "expense_categories": [
        "Housing", "Utilities", "Food", "Transportation", "Insurance",
        "Phone/Internet", "Childcare", "Health & Wellness", "Subscriptions",
        "Discretionary", "Travel", "Shopping", "Personal Care", "Giving",
        "Investments", "Education", "Other"
    ]
}

def init_session_state():
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value