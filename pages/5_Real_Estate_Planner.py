import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import numpy_financial as npf


# --- Page Setup ---
st.set_page_config(page_title="🏘️ Real Estate Planner", page_icon="🏡")
st.title("🏘️ Real Estate Planner")
st.caption("Model rental income, equity growth, and appreciation strategies to support your FIRE plan.")

# --- Intro ---
with st.expander("💡 What Role Does Real Estate Play in FIRE?", expanded=False):
    st.markdown("""
**Real estate** can be a powerful engine in your FIRE journey—offering both steady cash flow and long-term wealth through equity growth.

This planner helps you answer a focused question:

<blockquote style='color: #B00020; font-style: italic; font-size: 16px;'>“How much does this property contribute toward my financial independence?”</blockquote>

### What It Calculates:
- **Annual Net Cash Flow**: Rental income minus operating costs and debt service  
- **Equity Growth**: A year-by-year breakdown of mortgage payoff and appreciation  
- **Property Value vs Loan Balance**: Track how your investment builds wealth over time  
- **FIRE Summary**: Total projected cash flow and equity aligned to your FIRE timeline

Experiment with inputs (purchase year, appreciation, expenses) and explore how your property helps you trade rent checks for freedom.
""", unsafe_allow_html=True)


# --- Inputs ---
st.subheader("📋 Property Info")

import datetime
this_year = datetime.datetime.now().year

purchase_year = st.number_input(
    "🗓️ Year Property Was (or Will Be) Purchased",
    min_value=this_year - 50,
    max_value=this_year + 50,
    value=this_year,
    step=1,
    help="Enter the year you bought or expect to buy this property."
)

purchase_price = st.number_input("Purchase Price ($)", value=400000, step=5000)
down_payment_pct = st.slider("Down Payment (%)", 0, 100, 20)
loan_term = st.slider("Loan Term (Years)", 5, 40, 30)
interest_rate = st.slider("Interest Rate (%)", 1.0, 10.0, 4.0)

annual_rent = st.number_input("Annual Rental Income ($)", value=24000, step=1000)
annual_expenses = st.number_input("Annual Operating Expenses ($)", value=8000, step=500)

appreciation_rate = st.slider("Appreciation Rate (%)", 0.0, 10.0, 3.0)

years_held = st.slider(
    "How Many Years Will You Hold the Property?",
    min_value=1,
    max_value=40,
    value=15
)
model_years = [purchase_year + i for i in range(years_held)]

# --- Core Calculators ---
def amortization_schedule(loan_amount, annual_interest_rate, loan_term_years, years_held, start_year):
    monthly_rate = annual_interest_rate / 12 / 100
    num_payments = loan_term_years * 12
    monthly_payment = npf.pmt(monthly_rate, num_payments, -loan_amount)

    schedule = []
    balance = loan_amount

    for i in range(years_held):
        year = start_year + i
        interest_paid = 0
        principal_paid = 0
        for _ in range(12):
            interest = balance * monthly_rate
            principal = monthly_payment - interest
            balance -= principal
            interest_paid += interest
            principal_paid += principal
        schedule.append({
            "Year": year,
            "Beginning Balance": schedule[-1]["Ending Balance"] if schedule else loan_amount,
            "Principal Paid": principal_paid,
            "Interest Paid": interest_paid,
            "Ending Balance": balance
        })

    return pd.DataFrame(schedule)


def project_property_equity(purchase_price, appreciation_rate, loan_amount, annual_interest_rate, loan_term, years_held, start_year):
    amort_df = amortization_schedule(loan_amount, annual_interest_rate, loan_term, years_held, start_year)
    equity_records = []

    for i, row in amort_df.iterrows():
        year = row["Year"]
        value = purchase_price * ((1 + appreciation_rate / 100) ** (i+1))
        equity = value - row["Ending Balance"]
        equity_records.append({
            "Year": year,
            "Estimated Property Value": value,
            "Loan Balance": row["Ending Balance"],
            "Equity": equity
        })
    return pd.DataFrame(equity_records)

# --- Results Section ---
if st.button("Run Property Model"):
    st.markdown("## 📊 Property Analysis")

    loan_amount = purchase_price * (1 - down_payment_pct / 100)
    down_payment = purchase_price - loan_amount
    annual_debt_service = loan_amount * (interest_rate / 100)  # Simple interest-only approx

    gross_yield = (annual_rent / purchase_price) * 100
    net_operating_income = annual_rent - annual_expenses
    annual_cash_flow = net_operating_income - annual_debt_service
    cash_on_cash = (annual_cash_flow / down_payment) * 100 if down_payment else 0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("💵 Annual Net Cash Flow", f"${annual_cash_flow:,.0f}")
        st.metric("🏷️ Gross Yield", f"{gross_yield:.2f}%")
    with col2:
        st.metric("📊 Cash-on-Cash Return", f"{cash_on_cash:.2f}%")
        st.metric("💸 Est. Debt Service", f"${annual_debt_service:,.0f}")

    # --- Equity Visualization ---
    equity_df = project_property_equity(
        purchase_price, appreciation_rate,
        loan_amount, interest_rate,
        loan_term, years_held, purchase_year
    )
    
    # 🔥 FIRE-Oriented Summary Insight
    years_out = years_held
    projected_equity = equity_df["Equity"].iloc[-1]
    cashflow_total = annual_cash_flow * years_out

    st.markdown("### 🔥 FIRE Alignment Summary")
    st.success(f"""
    If you hold this property for **{years_out} years**:
    - You'll build **${projected_equity:,.0f}** in equity
    - You'll receive **${cashflow_total:,.0f}** in rental income
    - That's approximately **${projected_equity + cashflow_total:,.0f}** in FIRE-aligned wealth creation
    """)
    


    if annual_cash_flow > 0:
        st.success(f"🎉 Positive cash flow! This property is contributing **${annual_cash_flow:,.0f}**/year toward your expenses.")
    elif annual_cash_flow < 0:
        st.warning(f"⚠️ Negative cash flow of **${abs(annual_cash_flow):,.0f}**/year. Consider optimizing rent or reducing costs.")
    else:
        st.info("🧾 This property breaks even on operating costs and loan service.")

    if st.button("📤 Send These Results to FIRE Planner (Coming Soon)"):
        st.info("We'll soon let you use this property's annual cash flow or net equity in your FIRE timeline. Stay tuned!")

    st.markdown("### 📈 Equity Growth Over Time")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=equity_df["Year"], y=equity_df["Estimated Property Value"], name="Property Value", line=dict(color="green")))
    fig.add_trace(go.Scatter(x=equity_df["Year"], y=equity_df["Loan Balance"], name="Loan Balance", line=dict(color="red", dash="dot")))
    fig.add_trace(go.Scatter(x=equity_df["Year"], y=equity_df["Equity"], name="Net Equity", line=dict(color="blue")))
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Year",
        yaxis_title="Dollar Value ($)",
        title="Appreciation & Equity Projection"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("📈 Property value builds slowly but steadily — this is your hidden wealth engine powering your FIRE path.")

