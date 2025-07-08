import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import numpy_financial as npf
from sidebar import render_global_assumptions
render_global_assumptions()


if "run_model" not in st.session_state:
    st.session_state["run_model"] = False


# --- Page Setup ---
st.set_page_config(page_title="Real Estate Planner", page_icon="🏡")

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

fire_expenses = st.session_state["fire_expenses"]
inflation_rate = st.session_state["inflation_rate"]
withdrawal_rate = st.session_state["withdrawal_rate"]

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

purchase_price = st.number_input(
    "🏠 Purchase Price ($)",
    min_value=0,
    value=400000,
    step=10000,
    help="Total property cost before fees or closing costs"
)
down_payment_pct = st.number_input(
    "💵 Down Payment (% of purchase price)",
    min_value=0.0,
    value=20.0,
    step=1.0,
    help="Portion paid upfront; the rest is financed through a loan"
)
loan_term = st.number_input(
    "📅 Loan Term (years)",
    min_value=0,
    value=30,
    step=5,
    help="Length of your mortgage, usually 15–30 years"
)
interest_rate = st.number_input(
    "📈 Interest Rate (%)",
    min_value=0.0,
    value=6.0,
    step=0.1,
    help="Annual loan interest applied to the outstanding balance"
)

annual_rent = st.number_input(
    "🏡 Annual Rental Income ($)",
    min_value=0,
    value=24000,
    step=1000,
    help="Gross rent expected from tenants in one year"
)
annual_expenses = st.number_input(
    "🧾 Annual Operating Expenses ($)",
    min_value=0,
    value=5000,
    step=500,
    help="Includes property tax, maintenance, insurance, vacancy buffer, etc."
)
with st.expander("📋 What's included in Operating Expenses?"):
    st.markdown("""
    This field typically includes:
    - 🏛️ **Property Taxes** (e.g. 1–2% of purchase price)
    - 🛠️ **Maintenance and Repairs**
    - 🏡 **Insurance** and HOA dues
    - 📉 **Vacancy/Turnover buffer**
    
    If you want to model these separately, stay tuned for our Advanced Real Estate Planner 👷‍♀️
    """)
appreciation_rate = st.number_input(
    "📈 Property Appreciation Rate (%)",
    min_value=0.0,
    value=3.0,
    step=0.1,
    help="Expected annual increase in property value, compounded yearly (e.g. 3 means ~3% growth per year)"
)
years_held = st.slider(
    "How Many Years Will You Hold / Have You Held the Property?",
    min_value=1,
    max_value=40,
    value=15
)
model_years = [purchase_year + i for i in range(years_held)]

with st.expander("📋 View Global Assumptions (You can adjust these on the sidebar)", expanded=False):
    st.markdown(f"""
    - **🔥 FIRE Annual Spending:** `${fire_expenses:,.0f}`
    - **📉 Inflation Rate:** `{inflation_rate:.1f}%`
    - **📤 Withdrawal Rate:** `{withdrawal_rate:.1f}%`
    """)


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

fire_expenses = st.session_state["fire_expenses"]



# --- Results Section ---
if st.button("Run Property Model"):
    st.session_state["run_model"] = True

if st.session_state["run_model"]:
    # Your existing calculations and display code here

    loan_amount = purchase_price * (1 - down_payment_pct / 100)
    down_payment = purchase_price - loan_amount
    annual_debt_service = loan_amount * (interest_rate / 100)  # Simple interest-only approx

    gross_yield = (annual_rent / purchase_price) * 100
    net_operating_income = annual_rent - annual_expenses
    annual_cash_flow = net_operating_income - annual_debt_service
    cash_on_cash = (annual_cash_flow / down_payment) * 100 if down_payment else 0
    
    # --- Generate equity_df first ---
    equity_df = project_property_equity(
        purchase_price, appreciation_rate,
        loan_amount, interest_rate,
        loan_term, years_held, purchase_year
    )
    
    st.markdown("### 📊 Property Analysis")
    col1, col2 = st.columns(2)
    with col1:
            st.metric(
                "💵 Annual Net Cash Flow",
                f"${annual_cash_flow:,.0f}",
                help="Net income after operating expenses and loan payments"
            )
    with col1:
            st.metric(
                "🏷️ Gross Yield",
                f"{gross_yield:.2f}%",
                help="Annual rent divided by purchase price (before expenses)"
            )
    with col2:
            st.metric(
                "📊 Cash-on-Cash Return",
                f"{cash_on_cash:.2f}%",
                help="Cash flow divided by down payment—measures return on invested cash"
            )
    with col2:
            st.metric(
                "💸 Est. Debt Service",
                f"${annual_debt_service:,.0f}",
                help="Approximate annual mortgage payment (interest-only estimate)"
            )

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

    total_property_value = projected_equity + cashflow_total
    fire_years_covered = total_property_value / fire_expenses if fire_expenses else 0

    st.markdown("### 🔥 FIRE Impact Summary")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🏠 Equity Built", f"${projected_equity:,.0f}", help="Total equity from appreciation and loan paydown")
    with col2:
        st.metric("💵 Rental Income", f"${cashflow_total:,.0f}", help="Cumulative cash flow over the hold period")
    with col1:
        st.metric("🔥 Total FIRE Contribution", f"${projected_equity + cashflow_total:,.0f}", help="CCombined projected equity and cash flow from this property over the hold period")
    with col2:
        st.metric("📆 FIRE Years Covered", f"{fire_years_covered:.1f} yrs", help="Years this property could cover based on your FI lifestyle cost")


    st.markdown(f"""
    Over **{years_out} years**, this property could contribute **${projected_equity + cashflow_total:,.0f}** toward your path to financial independence.  
    That's real estate pulling serious FIRE weight 💪🏽🏘️
    """)

    if annual_cash_flow > 0:
        st.success(f"🎉 Positive cash flow means this property adds ${annual_cash_flow:,.0f}/year to your FIRE runway.")
    elif annual_cash_flow < 0:
        st.warning(f"⚠️ Negative cash flow of ${abs(annual_cash_flow):,.0f}/year could drag on your FIRE progress.")
    else:
        st.info("🧾 This property breaks even on income vs costs—not hurting, not helping FIRE cash flow.")


    if st.button("📤 Send These Results to Advanced Planner (Coming Soon)"):
        st.info("We'll soon let you use this property's annual cash flow or net equity in your FIRE timeline. Stay tuned!")

    st.markdown("### 📈 Equity Growth Over Time")

    with st.expander("❓ What's the difference between nominal and inflation-adjusted values?"):
        st.markdown("""
        <ul>
            <li><strong>Nominal values:</strong> show raw dollars at each point in time—no adjustment for inflation</li>
            <li><strong>Inflation-adjusted values:</strong> show today's equivalent dollars, revealing the <em>real</em> purchasing power over time</li>
            <li><strong>Example:</strong> A property worth $500,000 in 20 years might only feel like $300,000 today if inflation averages 2.5% annually.</li>
        </ul>
        """, unsafe_allow_html=True)


    # Update the global session value if changed
    st.session_state["inflation_rate"] = inflation_rate

    adjust_for_inflation = st.checkbox("🪄 Adjust for Inflation", value=True)   

    # --- Adjust data if needed ---
    equity_df = equity_df.copy()

    if adjust_for_inflation:
        equity_df["Inflation Factor"] = [
            (1 + inflation_rate / 100) ** (year - equity_df["Year"].iloc[0]) for year in equity_df["Year"]
        ]
        equity_df["Plot Property Value"] = equity_df["Estimated Property Value"] / equity_df["Inflation Factor"]
        equity_df["Plot Loan Balance"] = equity_df["Loan Balance"] / equity_df["Inflation Factor"]
        equity_df["Plot Equity"] = equity_df["Equity"] / equity_df["Inflation Factor"]
    else:
        equity_df["Plot Property Value"] = equity_df["Estimated Property Value"]
        equity_df["Plot Loan Balance"] = equity_df["Loan Balance"]
        equity_df["Plot Equity"] = equity_df["Equity"]

    # --- Plot ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=equity_df["Year"], y=equity_df["Plot Property Value"], name="Property Value", line=dict(color="green"), hovertemplate="$%{y:,.0f} market value<br>in %{x}"))
    fig.add_trace(go.Scatter(x=equity_df["Year"], y=equity_df["Plot Loan Balance"], name="Loan Balance", line=dict(color="red", dash="dot"), hovertemplate="$%{y:,.0f} loan balance<br>in %{x}"))
    fig.add_trace(go.Scatter(x=equity_df["Year"], y=equity_df["Plot Equity"], name="Net Equity", line=dict(color="blue"), hovertemplate="$%{y:,.0f} equity<br>in %{x}"))
    fig.update_layout(template="plotly_white", xaxis_title="Year", yaxis_title="Dollar Value ($)", title="Appreciation & Equity Projection" + (" (Real Dollars)" if adjust_for_inflation else " (Nominal Dollars)"))

    st.plotly_chart(fig, use_container_width=True)
    st.caption("📈 Property value builds slowly but steadily — this is your hidden wealth engine powering your FIRE path.")