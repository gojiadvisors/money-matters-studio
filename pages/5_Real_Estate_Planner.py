import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import numpy_financial as npf
import datetime
this_year = datetime.datetime.now().year


if "run_model" not in st.session_state:
    st.session_state["run_model"] = False

from utils_session import initialize_state

initialize_state({
    "purchase_year": this_year,
    "purchase_price": 400000,
    "down_payment_pct": 25.0,
    "loan_term": 30,
    "interest_rate": 3.0,
    "rental_growth_rate": 1.5,
    "appreciation_rate": 3.0,
    "mortgage_years": 30,
    "annual_rent": 24000,
    "annual_expenses": 5000,
    "years_held": 15
    # Add other synced fields here
})


# --- Page Setup ---
st.set_page_config(page_title="Real Estate Planner", page_icon="🏡")

# --- Initialize session keys if missing ---
st.session_state.setdefault("fire_expenses", 80000)
st.session_state.setdefault("inflation_rate", 2.5)
st.session_state.setdefault("withdrawal_rate", 3.5)


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

# 📈 Rental Growth Scenario Picker
rental_growth_option = st.selectbox(
    "📈 Rental Income Growth Scenario",
    options=[
        "Custom",
        "Low (1.0%)",
        "Market Average (1.5%)",
        "Aggressive (3.0%)"
    ],
    index=1,
    help=(
        "Pick a preset or choose 'Custom' to set your own annual rental growth rate. "
        "This reflects how much you expect rents to increase year over year."
    )
)

if rental_growth_option == "Custom":
    rental_growth_rate = st.slider(
        "Custom Rental Income Growth Rate (%)",
        min_value=0.0,
        max_value=10.0,
        value=st.session_state.get("rental_growth_rate", 1.5),
        step=0.1,
        help=(
            "Estimate how much your rental income will grow annually. "
            "Even modest growth (1–2%) can significantly impact long-term FIRE contribution."
        )
    )
else:
    rental_growth_rate = float(rental_growth_option.split("(")[-1].replace("%)", ""))

st.session_state["rental_growth_rate"] = rental_growth_rate

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
    max_value=50,
    value=15
)
model_years = [purchase_year + i for i in range(years_held)]

with st.expander("🔧 Customize Your Assumptions", expanded=True):

    # FIRE Spending Target
    fire_expenses = st.number_input(
        "🔥 Annual FIRE Spending Target ($)",
        min_value=0,
        value=st.session_state.get("fire_expenses", 80000),
        step=1000,
        help="How much you expect to spend annually once financially independent."
    )
    st.session_state["fire_expenses"] = fire_expenses

    # Inflation Presets
    inflation_option = st.selectbox(
        "📉 Inflation Scenario",
        options=["Custom", "Low (1.5%)", "Average (2.5%)", "High (4.0%)"],
        index=2,
        help=(
            "Your expected long-term average increase in prices. "
            "This affects future expenses and the purchasing power of your portfolio."
        )
    )

    if inflation_option == "Custom":
        inflation_rate = st.slider(
            "Custom Inflation Rate (%)",
            min_value=0.0,
            max_value=10.0,
            value=st.session_state.get("inflation_rate", 2.5),
            step=0.1,
            help=(
                "Set your own inflation estimate. Higher values reduce your future purchasing power and raise your FIRE target."
            )
        )
    else:
        inflation_rate = float(inflation_option.split("(")[-1].replace("%)", ""))
    st.session_state["inflation_rate"] = inflation_rate

    # Withdrawal Presets
    withdrawal_option = st.selectbox(
        "📤 Withdrawal Scenario",
        options=["Custom", "Conservative (3.0%)", "Moderate (3.5%)", "Aggressive (4.0%)"],
        index=1,
        help=(
            "The percentage of your FIRE portfolio you plan to withdraw annually. "
            "Lower values offer more safety; higher ones assume shorter time horizons or aggressive planning."
        )
    )

    if withdrawal_option == "Custom":
        withdrawal_rate = st.slider(
            "Custom Withdrawal Rate (%)",
            min_value=0.0,
            max_value=10.0,
            value=st.session_state.get("withdrawal_rate", 3.5),
            step=0.1,
            help=(
                "Set your own expected withdrawal rate, used to calculate the size of your required portfolio."
            )
        )
    else:
        withdrawal_rate = float(withdrawal_option.split("(")[-1].replace("%)", ""))
    st.session_state["withdrawal_rate"] = withdrawal_rate

adjust_for_inflation = st.checkbox("🪄 View All Outputs in Today's Dollars", value=True)

with st.expander("❓ What's the difference between nominal and inflation-adjusted values?"):
    st.markdown("""
    <ul>
        <li><strong>Nominal values:</strong> show raw dollars at each point in time—no adjustment for inflation</li>
        <li><strong>Inflation-adjusted values:</strong> show today's equivalent dollars, revealing the <em>real</em> purchasing power over time</li>
        <li><strong>Example:</strong> A property worth $500,000 in 20 years might only feel like $300,000 today if inflation averages 2.5% annually.</li>
    </ul>
    """, unsafe_allow_html=True)

# --- Core Calculators ---
def amortization_schedule(loan_amount, annual_interest_rate, loan_term_years, years_held, start_year):
    monthly_rate = annual_interest_rate / 12 / 100
    num_payments = loan_term_years * 12
    monthly_payment = npf.pmt(monthly_rate, num_payments, -loan_amount)  # ✅ this is missing

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

def project_property_equity(purchase_price, appreciation_rate, loan_amount, annual_interest_rate, loan_term, years_held, start_year, inflation_rate=0.0, adjust_for_inflation=False):
    amort_df = amortization_schedule(loan_amount, annual_interest_rate, loan_term, years_held, start_year)
    equity_records = []

    for i, row in amort_df.iterrows():
        year = row["Year"]
        value = purchase_price * ((1 + appreciation_rate / 100) ** i)
        equity = value - row["Ending Balance"]

        if adjust_for_inflation:
            inflation_factor = (1 + inflation_rate / 100) ** i
            value /= inflation_factor
            equity /= inflation_factor

        equity_records.append({
            "Year": year,
            "Estimated Property Value": value,
            "Loan Balance": row["Ending Balance"],
            "Equity": equity
        })
    return pd.DataFrame(equity_records)


fire_expenses = st.session_state["fire_expenses"]

def project_cashflow(annual_rent, annual_expenses, rental_growth_rate, annual_debt_service, years_out, inflation_rate, adjust_for_inflation):
    cashflow_records = []
    for i in range(years_out):
        rent = annual_rent * ((1 + rental_growth_rate / 100) ** i)
        expenses = annual_expenses * ((1 + inflation_rate / 100) ** i)
        net_income = rent - expenses
        cashflow = net_income - annual_debt_service

        if adjust_for_inflation:
            inflation_factor = (1 + inflation_rate / 100) ** i
            cashflow /= inflation_factor

        cashflow_records.append(cashflow)

    return cashflow_records

# --- Results Section ---

if st.button("Run Property Model"):
    st.session_state["run_model"] = True

if st.session_state["run_model"]:
    
    # Your existing calculations and display code here
    inflation_factor = (1 + inflation_rate / 100) ** years_held
    loan_amount = purchase_price * (1 - down_payment_pct / 100)
    down_payment = purchase_price - loan_amount

    # 🔢 Compute amortized annual mortgage payment
    monthly_rate = interest_rate / 12 / 100
    num_payments = loan_term * 12
    monthly_payment = npf.pmt(monthly_rate, num_payments, -loan_amount)
    annual_debt_service = monthly_payment * 12

    gross_yield = (annual_rent / purchase_price) * 100
    cashflow_list = project_cashflow(
        annual_rent, annual_expenses, rental_growth_rate,
        annual_debt_service, years_held,
        inflation_rate, adjust_for_inflation
    )

    cashflow_total = sum(cashflow_list)
    #annual_cash_flow_avg = sum(cashflow_list) / years_held
    annual_cash_flow_year_1 = cashflow_list[0]  # First year of projected cash flow
    cash_on_cash = (annual_cash_flow_year_1 / down_payment) * 100 if down_payment else 0
    
    # --- Generate equity_df first ---
    amort_schedule = amortization_schedule(
        loan_amount, interest_rate, loan_term, years_held, purchase_year
    )

    equity_records = project_property_equity(
        purchase_price,
        appreciation_rate,
        amort_schedule,
        inflation_rate,
        adjust_for_inflation,
        years_held,
        start_year=purchase_year
    )

    equity_df = pd.DataFrame(equity_records)
    
    st.markdown("### 📊 Property Analysis")
    col1, col2 = st.columns(2)
    with col1:
            st.metric(
                "💵 Year 1 Net Cash Flow",
                f"${annual_cash_flow_year_1:,.0f}",
                help="Net income in the first year after operating expenses and mortgage payments"
            )
    with col1:
            st.metric(
                "🏷️ Gross Yield",
                f"{gross_yield:.2f}%",
                help="Annual rent divided by purchase price (before expenses)"
            )
    with col2:
            st.metric(
                "📊 Cash-on-Cash Return (Year 1)",
                f"{cash_on_cash:.2f}%",
                help="Year 1 cash flow divided by down payment—standard metric used in real estate analysis"
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
        loan_term, years_held, purchase_year,
        inflation_rate, adjust_for_inflation  # ✅ Add these two
    )

    # 🔥 FIRE-Oriented Summary Insight
    years_out = years_held
    projected_equity = equity_df["Equity"].iloc[-1]
    cashflow_total = sum(cashflow_list)

    if adjust_for_inflation:
        projected_equity = equity_df["Equity"].iloc[-1]  # ✅ Already inflation-adjusted
        #projected_equity /= inflation_factor  # ✅ Adjust equity at summary level
        # cashflow_total was already discounted year-by-year
    
    total_property_value = projected_equity + cashflow_total
    fire_years_covered = total_property_value / fire_expenses if fire_expenses else 0

    st.markdown("### 🔥 FIRE Impact Summary")

    equity_label = "🏠 Real Equity Built" if adjust_for_inflation else "🏠 Equity Built"
    cashflow_label = "💵 Inflation-Adjusted Rental Income" if adjust_for_inflation else "💵 Rental Income"

    col1, col2 = st.columns(2)
    with col1:
        st.metric(equity_label, f"${projected_equity:,.0f}", help="Total equity from appreciation and loan paydown")
    with col2:
        st.metric(cashflow_label, f"${cashflow_total:,.0f}", help="Cumulative cash flow over the hold period")
    with col1:
        st.metric("🔥 Total FIRE Contribution", f"${projected_equity + cashflow_total:,.0f}", help="Combined projected equity and cash flow from this property over the hold period")
    with col2:
        st.metric("📆 FIRE Years Covered", f"{fire_years_covered:.1f} yrs", help="Years this property could cover based on your FI lifestyle cost")


    st.markdown(f"""
    Over **{years_out} years**, this property could contribute **${projected_equity + cashflow_total:,.0f}** toward your path to financial independence.  
    This includes both net rental income you receive along the way and equity built over time, which becomes available when you sell. 
    """)
    #That's real estate pulling serious FIRE weight 💪🏽🏘️


    if annual_cash_flow_year_1 > 0:
        st.success(f"🎉 In Year 1, this property adds ${annual_cash_flow_year_1:,.0f}/year to your FIRE runway.")
    elif annual_cash_flow_year_1 < 0:
        st.warning(f"⚠️ In Year 1, negative cash flow of ${abs(annual_cash_flow_year_1):,.0f}/year could drag on your FIRE progress.")
    else:
        st.info("🧾 This property breaks even in Year 1—neutral impact on your FIRE runway.")

    if st.button("📤 Send These Results to Investment Comparison Tool"):
        st.session_state["re_sync"] = True
        st.session_state["purchase_year"] = purchase_year
        st.session_state["property_value"] = purchase_price
        st.session_state["down_payment_pct"] = down_payment_pct
        st.session_state["mortgage_years"] = loan_term
        st.session_state["mortgage_rate"] = interest_rate
        st.session_state["appreciation_rate"] = appreciation_rate
        st.session_state["annual_rent"] = annual_rent
        st.session_state["rental_growth_rate"] = rental_growth_rate
        st.session_state["annual_expenses"] = annual_expenses
        st.session_state["years_held"] = years_held
        st.success("✅ Inputs synced to Investment Comparison Tool.")

    st.markdown("### 📈 Equity Growth Over Time")

    # Update the global session value if changed
    st.session_state["inflation_rate"] = inflation_rate

    # --- Adjust data if needed ---
    equity_df = equity_df.copy()

    if adjust_for_inflation:
        equity_df["Inflation Factor"] = [
            (1 + inflation_rate / 100) ** (year - equity_df["Year"].iloc[0]) for year in equity_df["Year"]
        ]
        equity_df["Plot Property Value"] = equity_df["Estimated Property Value"] / equity_df["Inflation Factor"]
        equity_df["Plot Loan Balance"] = equity_df["Loan Balance"] / equity_df["Inflation Factor"]
        equity_df["Plot Equity"] = equity_df["Equity"]
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

    cf_df = pd.DataFrame({
        "Year": [purchase_year + i for i in range(years_held)],
        "Net Cash Flow": cashflow_list
    })

    year_1_cashflow = cashflow_list[0]
    year_final_cashflow = cashflow_list[-1]
    year_final_label = cf_df["Year"].iloc[-1]

    import plotly.graph_objects as go

    cf_df = pd.DataFrame({
        "Year": [purchase_year + i for i in range(years_held)],
        "Net Cash Flow": cashflow_list
    })

    st.markdown("### 💵 Cash Flow Trend Over Time")

    cf_fig = go.Figure()

    cf_fig.add_trace(go.Scatter(
        x=cf_df["Year"],
        y=cf_df["Net Cash Flow"],
        name="Net Cash Flow",
        line=dict(color="blue"),
        hovertemplate="$%{y:,.0f} net cash flow<br>in %{x}"
    ))

    cf_fig.update_layout(
        template="plotly_white",
        xaxis_title="Year",
        yaxis_title="Net Cash Flow ($)",
        xaxis=dict(tickmode="linear", tickformat=".0f"),
        title="Year-by-Year Cash Flow Projection" + (" (Purchasing Power in Today's Dollars)" if adjust_for_inflation else " (Nominal Future Dollars)")
    )

    cf_fig.add_annotation(
    xref="paper", yref="paper",
    x=0, y=1.12,  # position above top-left corner
    showarrow=False,
    text=(
        f"Year 1 Cash Flow: ${year_1_cashflow:,.0f} → "
        f"Year {year_final_label}: ${year_final_cashflow:,.0f} "
        f"({ 'inflation-adjusted' if adjust_for_inflation else 'nominal' })"
    ),
    font=dict(size=14),
    align="left",
    bgcolor="rgba(255,255,255,0.8)",
    bordercolor="lightgray",
    borderwidth=1,
)
    st.plotly_chart(cf_fig, use_container_width=True)
    st.caption("📊 This chart shows how rental income, inflation, and fixed mortgage payments interact over time.")

