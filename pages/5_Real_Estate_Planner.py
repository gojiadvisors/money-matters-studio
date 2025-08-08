import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import numpy_financial as npf
import datetime
this_year = datetime.datetime.now().year
from session_defaults import DEFAULTS
from utils_session import initialize_state_once
initialize_state_once(DEFAULTS)  # ✅ now has the required argument
def clear_session_state():
    for key in st.session_state.keys():
        del st.session_state[key]

col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    if st.button("🔄 Reset", help="Reset Session Inputs"):
        clear_session_state()
        st.rerun()


# --- Page Setup ---
st.set_page_config(page_title="Real Estate Planner", page_icon="🏡")
st.title("🏘️ Real Estate Planner")
st.caption("Model rental income, equity growth, and appreciation strategies to support your FIRE plan.")

# --- Intro ---
with st.expander("💡 What Role Does Real Estate Play in FIRE?", expanded=False):
    st.markdown("""
**Real estate** can be a powerful lever in your FIRE strategy—offering both steady cash flow and long-term equity growth.

This planner helps you answer a pivotal question:  
<blockquote style='color: #B00020; font-style: italic; font-size: 16px;'>“How much does this property contribute toward my financial independence?”</blockquote>

Adjust inputs like purchase year, appreciation rate, or expenses—and discover how your property helps you swap rent checks for freedom.
""", unsafe_allow_html=True)

# ### What It Calculates:
# - **Net Cash Flow**: Rental income minus operating costs and loan payments  
# - **Equity Growth**: Year-by-year breakdown of appreciation and mortgage payoff  
# - **Wealth Timeline**: Property value vs loan balance over time  
# - **FIRE Summary**: Total projected cash flow + equity minus upfront costs, to reveal the property’s true FIRE contribution

# --- Inputs ---
st.subheader("📋 Property Info")

purchase_year = st.number_input(
    "🗓️ Year Property Was (or Will Be) Purchased",
    min_value=this_year - 50,
    max_value=this_year + 50,
    value=st.session_state.get("purchase_year", this_year),
    step=1,
    help="Enter the year you bought or expect to buy this property."
)
st.session_state["purchase_year"] = purchase_year

purchase_price = st.number_input(
    "🏠 Purchase Price ($)",
    min_value=0,
    value=st.session_state.get("purchase_price", 400000),
    step=10000,
    help="Total property cost before fees or closing costs"
)
st.session_state["purchase_price"] = purchase_price

down_payment_pct = st.number_input(
    "💵 Down Payment (% of purchase price)",
    min_value=0.0,
    value=st.session_state.get("down_payment_pct", 25.0),
    step=1.0,
    help="Portion paid upfront; the rest is financed through a loan"
)
st.session_state["down_payment_pct"] = down_payment_pct

with st.expander("🧰 Additional Property Expenses", expanded=True):

    closing_costs = st.number_input(
        "🧾 Closing Costs ($)",
        value=st.session_state.get("closing_costs", 10000.0),
        step=500.0,
        help="Fees and charges incurred at purchase (e.g., title, escrow, loan origination)."
    )
    st.session_state["closing_costs"] = closing_costs

    renovation_costs = st.number_input(
        "🛠️ Renovation Costs ($)",
        value=st.session_state.get("renovation_costs", 15000.0),
        step=1000.0,
        help="Estimated post-purchase upgrade or repair expenses to improve livability or value."
    )
    st.session_state["renovation_costs"] = renovation_costs

# 👉 Insert this block BELOW the inputs
down_payment = purchase_price * (down_payment_pct / 100)

# 🧮 New addition!
property_initial_investment = down_payment + closing_costs + renovation_costs

st.markdown(f"💵 **Total Initial Investment:** ${property_initial_investment:,.0f}")

loan_term = st.number_input(
    "📅 Loan Term (years)",
    min_value=0,
    value=st.session_state.get("mortgage_years", 30),
    step=5,
    help="Length of your mortgage, usually 15–30 years"
)
st.session_state["mortgage_years"] = loan_term

interest_rate = st.number_input(
    "📈 Mortgage Interest Rate (%)",
    min_value=0.0,
    value=st.session_state.get("interest_rate", 6.0),
    step=0.1,
    help="Annual loan interest applied to the outstanding balance"
)
st.session_state["interest_rate"] = interest_rate

annual_rent = st.number_input(
    "🏡 Annual Rental Income ($)",
    min_value=0,
    value=st.session_state.get("annual_rent", 24000),
    step=1000,
    help="Gross rent expected from tenants in one year"
)
st.session_state["annual_rent"] = annual_rent

# 📈 Rental Income Growth Scenario Picker
from shared_components import rental_growth_picker
# Set the default selection and invoke the picker
rental_growth_rate = rental_growth_picker(default="Moderate Growth (1.5%)")

annual_expenses = st.number_input(
    "🧾 Annual Operating Expenses ($)",
    min_value=0,
    value=st.session_state.get("annual_expenses", 5000),
    step=500,
    help="Includes property tax, maintenance, insurance, vacancy buffer, etc."
)
st.session_state["annual_expenses"] = annual_expenses

# with st.expander("📋 What's included in Operating Expenses?"):
#     st.markdown("""
#     This field typically includes:
#     - 🏛️ **Property Taxes** (e.g. 1–2% of purchase price)
#     - 🛠️ **Maintenance and Repairs**
#     - 🏡 **Insurance** and HOA dues
#     - 📉 **Vacancy/Turnover buffer**
    
#     If you want to model these separately, stay tuned for our Advanced Real Estate Planner 👷‍♀️
#     """)

appreciation_rate = st.number_input(
    "📈 Property Appreciation Rate (%)",
    min_value=0.0,
    value=st.session_state.get("appreciation_rate", 3.0),
    step=0.1,
    help="Expected annual increase in property value, compounded yearly (e.g. 3 means ~3% growth per year)"
)
st.session_state["appreciation_rate"] = appreciation_rate

years_held = st.slider(
    "How Many Years Will You Hold / Have You Held the Property?",
    min_value=1,
    max_value=50,
    value=st.session_state.get("years_held", 15)
)
st.session_state["years_held"] = years_held
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
    # Map preset labels to inflation rates
    preset_map = {
        "Low (1.5%)": 1.5,
        "Average (2.5%)": 2.5,
        "High (4.0%)": 4.0
    }

    # Identify preset match based on session inflation_rate
    current_rate = st.session_state.get("inflation_rate", 2.5)
    matched_label = next((label for label, rate in preset_map.items() if rate == current_rate), None)

    # Define available options
    options = ["Custom"] + list(preset_map.keys())

    # Pick dropdown index based on match or prior selection
    dropdown_index = options.index(matched_label) if matched_label else options.index(st.session_state.get("inflation_option", "Average (2.5%)"))

    # Select inflation scenario
    # Inflation Input from Shared Component
    from shared_components import inflation_picker
    inflation_rate = inflation_picker()

    # Withdrawl Scenario
    from shared_components import withdrawal_picker
    withdrawal_rate, withdrawal_scenario = withdrawal_picker()
    #st.caption(f"📘 Using **{withdrawal_scenario}** scenario → {withdrawal_rate * 100:.2f}% withdrawal rate.")

adjust_for_inflation = st.checkbox(
    "🪄 View All Outputs in Today's Dollars",
    value=True,
    help="Shows inflation-adjusted results, meaning your future values expressed in today's purchasing power. Without adjustment, values appear in raw future dollars (nominal)."
)

# with st.expander("❓ What's the difference between nominal and inflation-adjusted values?"):
#     st.markdown("""
#     <ul>
#         <li><strong>Nominal values:</strong> show raw dollars at each point in time—no adjustment for inflation</li>
#         <li><strong>Inflation-adjusted values:</strong> show today's equivalent dollars, revealing the <em>real</em> purchasing power over time</li>
#         <li><strong>Example:</strong> A property worth $500,000 in 20 years might only feel like $300,000 today if inflation averages 2.5% annually.</li>
#     </ul>
#     """, unsafe_allow_html=True)

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

if st.button("▶️ Run Property Model"):
    st.session_state["run_model"] = True

if st.session_state["run_model"]:
    st.markdown("---")
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
    cash_on_cash = (annual_cash_flow_year_1 / property_initial_investment) * 100 if property_initial_investment else 0
    
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

    # --- Equity & Cash Flow Calculation ---
    equity_df = project_property_equity(
        purchase_price, appreciation_rate,
        loan_amount, interest_rate,
        loan_term, years_held, purchase_year,
        inflation_rate, adjust_for_inflation
    )

    years_out = years_held
    projected_equity = equity_df["Equity"].iloc[-1]
    cashflow_total = sum(cashflow_list)

    if adjust_for_inflation:
        projected_equity = equity_df["Equity"].iloc[-1]  # Already inflation-adjusted

    total_property_value = projected_equity + cashflow_total
    net_fire_contribution = total_property_value - (closing_costs + renovation_costs)
    fire_years_covered = total_property_value / fire_expenses if fire_expenses else 0
    net_fire_years_covered = net_fire_contribution / fire_expenses if fire_expenses else 0

    equity_label = "🏠 Real Equity Built" if adjust_for_inflation else "🏠 Equity Built"
    cashflow_label = "💵 Inflation-Adjusted Rental Income" if adjust_for_inflation else "💵 Rental Income"

    # --- Title ---
    #st.markdown("### 🔥 Real Estate FIRE Summary")
    # # --- FIRE-Focused Metrics ---
    # col1, col2 = st.columns(2)
    # with col1:
    #     st.metric(
    #         "💰 Total Initial Investment",
    #         f"${property_initial_investment:,.0f}",
    #         help="Upfront capital deployed including down payment, closing costs, and renovation expenses."
    #     )
    # with col2:
    #     st.metric(
    #         equity_label,
    #         f"${projected_equity:,.0f}",
    #         help="Equity gained from home appreciation and mortgage principal reduction."
    #     )
    # with col1:
    #     st.metric(
    #         cashflow_label,
    #         f"${cashflow_total:,.0f}",
    #         help="Cumulative rental income over the hold period."
    #     )
    # with col2:
    #     st.metric(
    #         "🔥 Net FIRE Contribution",
    #         f"${net_fire_contribution:,.0f}",
    #         help="Total rental income + equity minus closing and renovation costs."
    #     )
    # with col1:
    #     st.metric(
    #         "📆 Net FIRE Years Covered",
    #         f"{net_fire_years_covered:.1f} yrs",
    #         help="Number of years this investment could support your FIRE lifestyle, net of upfront costs."
    #     )
    # with col2:
    #     st.metric(
    #         "📈 ROI on Total Investment",
    #         f"{(net_fire_contribution / property_initial_investment):.2f}x",
    #         help="Return multiple based on initial investment including closing and renovation."
    #     )

    st.markdown(f"""
    ### 🏘️ Real Estate Investment Summary

    | 💼 Metric | 💰 Your Result | 💡 What It Means |
    |----------------------------|----------------------|------------------------------|
    | **Total Initial Investment** | ${property_initial_investment:,.0f} | The total amount of money you put in upfront, including the down payment, closing costs, and any renovations. |
    | **Projected Equity Gain** | ${projected_equity:,.0f} | How much value you build over time from your home going up in price and paying down the mortgage. |
    | **Total Cashflow Earned** | ${cashflow_total:,.0f} | The total rent money you collect after expenses during the time you own the property. |
    | **Net FIRE Contribution** | **${net_fire_contribution:,.0f}** | **The overall benefit this investment adds to your financial independence combining rent income and property value (minus costs).** |    
    | **Years of FIRE Covered** | {net_fire_years_covered:.1f} yrs | How many years this investment could help pay for your lifestyle after you retire early. |
    | **ROI on Investment** | {(net_fire_contribution / property_initial_investment):.2f}x | A simple way to see how much you got back compared to what you put in. (e.g. 2x means you doubled your money) |
    """)

    # --- FIRE Impact Narrative ---
    st.markdown(f"""
    Over **{years_out} years**, this property could contribute **${net_fire_contribution:,.0f}** toward your financial independence journey. This includes both cumulative rental income and equity growth, which become accessible when you sell.
    """)

    # # --- Traditional Metrics in Expander ---
    # with st.expander("📄 View Traditional Real Estate Metrics", expanded=False):
    #     st.metric(
    #         "💵 Year 1 Net Cash Flow",
    #         f"${annual_cash_flow_year_1:,.0f}",
    #         help="Net income after operating expenses and mortgage payments in Year 1."
    #     )
    #     st.metric(
    #         "🏷️ Gross Yield",
    #         f"{gross_yield:.2f}%",
    #         help="Annual rent divided by purchase price (before expenses)."
    #     )
    #     st.metric(
    #         "📊 Cash-on-Cash Return (Year 1)",
    #         f"{cash_on_cash:.2f}%",
    #         help="Return in Year 1 based on total upfront cash investment."
    #     )
    #     st.metric(
    #         "🏦 Annual Mortgage Payment",
    #         f"${annual_debt_service:,.0f}",
    #         help="Principal and interest paid in the first year of your loan."
    #     )
    #     # --- Optional Year 1 Impact ---
    #     if annual_cash_flow_year_1 != 0:
    #         impact_msg = (
    #             f"🎉 In Year 1, this property adds ${annual_cash_flow_year_1:,.0f}/year to your FIRE runway."
    #             if annual_cash_flow_year_1 > 0 else
    #             f"⚠️ In Year 1, negative cash flow of ${abs(annual_cash_flow_year_1):,.0f}/year could drag on your FIRE progress."
    #         )
    #         st.info(impact_msg)

    st.markdown("---")

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

    st.markdown("---")

    with st.expander("📄 View Traditional Real Estate Metrics", expanded=False):
        st.markdown(f"""
        ### 🧾 Year 1 Investment Snapshot

        | 🧮 Metric | 📊 Your Result | 💡 What It Means |
        |-----------------------------|--------------------|----------------------------|
        | **Year 1 Net Cash Flow** | ${annual_cash_flow_year_1:,.0f} | The money you make (or lose) from rent after paying for expenses and the mortgage in the first year. |
        | **Gross Yield** | {gross_yield:.2f}% | A quick way to see how much rent you earn compared to the purchase price (before subtracting expenses). |
        | **Cash-on-Cash Return** | {cash_on_cash:.2f}% | How much profit you make in the first year compared to the cash you invested upfront. |
        | **Annual Mortgage Payment** | ${annual_debt_service:,.0f} | The total amount you pay toward your loan (principal + interest) in the first year. |
        """)

        if annual_cash_flow_year_1 != 0:
            impact_msg = (
                f"🎉 In Year 1, this property adds ${annual_cash_flow_year_1:,.0f}/year to your FIRE runway."
                if annual_cash_flow_year_1 > 0 else
                f"⚠️ In Year 1, negative cash flow of ${abs(annual_cash_flow_year_1):,.0f}/year could drag on your FIRE progress."
            )
            st.info(impact_msg)

    cf_df = pd.DataFrame({
        "Year": [purchase_year - 1] + [purchase_year + i for i in range(years_held)],
        "Net Cash Flow": [-property_initial_investment] + cashflow_list
    })

    year_1_cashflow = cashflow_list[0]
    year_final_cashflow = cashflow_list[-1]
    year_final_label = cf_df["Year"].iloc[-1]

    import plotly.graph_objects as go

    cf_df = pd.DataFrame({
        "Year": [purchase_year + i for i in range(years_held)],
        "Net Cash Flow": cashflow_list
    })

    with st.expander("💵 View Cash Flow Trend Over Time", expanded=False):

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
            x=0, y=1.12,
            showarrow=False,
            text=(
                f"📉 Year 0 Investment: -${property_initial_investment:,.0f} → "
                f"📈 Year 1 Cash Flow: ${year_1_cashflow:,.0f} → "
                f"🏁 Year {year_final_label}: ${year_final_cashflow:,.0f} "
                f"({ 'inflation-adjusted' if adjust_for_inflation else 'nominal' })"
            ),
            font=dict(size=14),
            align="left",
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="lightgray",
            borderwidth=1,
        )

        st.plotly_chart(cf_fig, use_container_width=True)
        st.caption("📊 This chart shows how rental income, inflation, and fixed mortgage payments interact over time.")

