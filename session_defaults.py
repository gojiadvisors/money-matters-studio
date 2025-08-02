# session_defaults.py

import datetime
this_year = datetime.datetime.now().year

DEFAULTS = {
    # FIRE Tracker
    "liquid_assets": 100000,
    "illiquid_assets": 0,
    "include_illiquid": False,
    "annual_savings": 30000,
    "savings_growth_scenario": "Flat (0.0%)",
    "return_option": "Moderate Growth (7.0%)",
    "fire_expenses": 80000,
    "withdrawal_option": "Moderate (3.5%)",
    "inflation_option": "Average (2.5%)",
    "adjust_fire_expenses_for_inflation": True,

    # Real Estate Planner
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
}
