import streamlit as st
import numpy_financial as npf
import pandas as pd
import datetime
this_year = datetime.datetime.now().year

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
    "years_held": 15,
    "closing_costs": 10000.0,
    "renovation_costs": 15000.0,
    # Add other synced fields here
})

# --- Page Setup ---
st.set_page_config(page_title="Investment Analyzer", page_icon="📊")

st.title("📊 Investment Analyzer")
st.caption("Compare investment strategies (🏘️ real estate vs. 📈 stock market) to see which accelerates your FIRE timeline more efficiently.")

with st.expander("💡 Which Investment Leads to FIRE Faster?", expanded=False):
    st.markdown("""
Choosing between **real estate** and **stock market** can shape the pace and flexibility of your path to financial independence.

This module helps you answer the essential FIRE question:

<blockquote style='color: #B00020; font-style: italic; font-size: 16px;'>“Should I invest in property or the stock market? Which one gets me to FIRE faster?”</blockquote>

### What It Compares:
- 🏘️ **Real Estate**: Net cash flow, equity buildup, and appreciation over time  
- 📈 **Equity Markets**: Portfolio growth through compounding, dividend reinvestment, and consistent contributions
- 🧮 **Total FIRE Contribution**: Real estate vs stock market outcomes, adjusted for net investment impact
- 🔁 **Break-Even Analysis**: Year-by-year comparison to spotlight when one strategy pulls ahead

This tool lets you simulate assumptions, explore trade-offs, and uncover the most effective wealth-building route based on your timeline and risk comfort.
""", unsafe_allow_html=True)

# --- Shared Inputs (Planner-style) ---

this_year = datetime.datetime.now().year

st.subheader("🔧 Customize Your Investment Timeline")

purchase_year = st.number_input(
    "🗓️ Year Investment Was (or Will Be) Made",
    min_value=this_year - 50,
    max_value=this_year + 50,
    value=st.session_state.get("purchase_year", this_year),
    step=1,
    help="The year you bought or expect to buy this property or make the fund investment."
)

investment_years = st.slider(
    "📅 Investment Duration (Years)",
    min_value=1,
    max_value=50,
    value=st.session_state.get("years_held", 15),
    help="How long you plan to hold this investment before selling or retiring."
)

st.markdown("### 📂 Input Assumptions for Both Investment Paths")
st.warning(
    "⚠️ To compare real estate and stock market, be sure to enter your assumptions for **BOTH** tabs.\n\n"
    # "🔹 Start with your property details in **Real Estate**\n\n"
    # "🔹 Then switch to **Equity Market** to configure stock-based growth assumptions"
)

#use_synced_investment = True  # You can later make this a checkbox toggle if desired
use_synced_investment = st.checkbox("🔗 Use same investment amount for both strategies", value=True)

# Tabs for scenario input
tab1, tab2 = st.tabs(["🏘️ Real Estate", "📈 Equity Market"])

with tab1:
    st.subheader("🏘️ Real Estate Scenario")

    all_cash_purchase = st.checkbox("🪙 Buy with All Cash (No Mortgage)", value=False)

    property_value = st.number_input(
        "🏠 Property Purchase Price ($)",
        min_value=50000,
        step=10000,
        value=st.session_state.get("property_value", 400000),
        help="Full market price of the property you'd like to invest in."
    )

    with st.expander("🧰 Additional Property Expenses", expanded=True):

        closing_costs = st.number_input(
            "🧾 Closing Costs ($)",
            value=st.session_state.get("closing_costs", 10000.0),
            step=500.0,
            help="Fees and charges incurred at purchase (e.g., title, escrow, loan origination)."
        )

        renovation_costs = st.number_input(
            "🛠️ Renovation Costs ($)",
            value=st.session_state.get("renovation_costs", 15000.0),
            step=1000.0,
            help="Estimated post-purchase upgrade or repair expenses to improve livability or value."
        )

    if all_cash_purchase:
        initial_investment = property_value + closing_costs + renovation_costs
        down_payment_pct = 100
        st.info("You're purchasing the property outright. No mortgage terms needed.")
    else:
        down_payment_pct = st.number_input(
            "💵 Down Payment (% of purchase price)",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state.get("down_payment_pct", 25.0),
            step=1.0,
            help="Portion paid upfront; the rest is financed through a loan."
        )
        initial_investment = property_value * (down_payment_pct / 100) + closing_costs + renovation_costs

        mortgage_years = st.number_input(
            "📅 Loan Term (years)",
            min_value=1,
            max_value=40,
            value=st.session_state.get("mortgage_years", 30),
            step=1,
            help="Length of your mortgage, typically 15–30 years."
        )

        mortgage_rate = st.number_input(
            "📈 Mortgage Interest Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state.get("mortgage_rate", 6.0),
            step=0.1,
            help="Annual interest rate charged on the loan."
        )
    
    # -- Performance Assumptions --
    appreciation_rate = st.number_input(
        "📈 Property Appreciation Rate (%)",
        min_value=0.0,
        value=st.session_state.get("appreciation_rate", 3.0),
        step=0.1,
        help="Expected annual increase in property value, compounded yearly (e.g. 3 means ~3% growth per year)."
    )

    annual_rent = st.number_input(
        "🏡 Annual Rental Income ($)",
        min_value=0,
        value=st.session_state.get("annual_rent", 24000),
        step=1000,
        help="Gross rent expected from tenants in one year — before expenses or vacancy adjustments."
    )

    # 📈 Rental Income Growth Scenario Picker
    growth_rate_from_session = st.session_state.get("rental_growth_rate", 1.5)

    # Dynamically determine default index based on session value
    if growth_rate_from_session == 1.0:
        default_index = 1
    elif growth_rate_from_session == 1.5:
        default_index = 2
    elif growth_rate_from_session == 3.0:
        default_index = 3
    else:
        default_index = 0  # Custom

    rental_growth_option = st.selectbox(
        "📈 Rental Income Growth Scenario",
        options=[
            "Custom",
            "Low (1.0%)",
            "Market Average (1.5%)",
            "Aggressive (3.0%)"
        ],
        index=default_index,
        help=(
            "Pick a preset or choose 'Custom' to set your own annual rental growth rate. "
            "This reflects how much you expect rents to increase year over year."
        )
    )

    # Capture input based on selected option
    if rental_growth_option == "Custom":
        rental_growth_rate = st.slider(
            "Custom Rental Income Growth Rate (%)",
            min_value=0.0,
            max_value=10.0,
            value=growth_rate_from_session,
            step=0.1,
            help=(
                "Estimate how much your rental income will grow annually. "
                "Even modest growth (1–2%) can significantly impact long-term FIRE contribution."
            )
        )
    else:
        rental_growth_rate = float(rental_growth_option.split("(")[-1].replace("%)", ""))

    # Sync back to session
    st.session_state["rental_growth_rate"] = rental_growth_rate

    annual_expenses = st.number_input(
    "🧾 Annual Operating Expenses ($)",
    min_value=0,
    value=st.session_state.get("annual_expenses", 5000),
    step=500,
    help="Total costs per year including tax, maintenance, insurance, and management."
)
    
    st.markdown(
    f"""
    <span style='font-size: 0.85rem; color: gray;'>
    📘 This simulation assumes a property worth ${property_value:,.0f} with an initial investment of ${initial_investment:,.0f}, reflecting your upfront capital and purchase assumptions.
    </span>
    <br><br>
    """,
    unsafe_allow_html=True
)

    # with st.expander("📋 What's included in Operating Expenses?"):
    #     st.markdown("""
    #     This field typically includes:
    #     - 🏛️ **Property Taxes** (e.g. 1–2% of purchase price)
    #     - 🛠️ **Maintenance and Repairs**
    #     - 🏡 **Insurance** and HOA dues
    #     - 📉 **Vacancy/Turnover buffer**

    #     You can refine this breakdown in advanced modules.
    #     """)


# -- Inflation Assumption --
with st.expander("📉 Inflation Scenario", expanded=True):
    preset = st.selectbox(
        "Choose Your Inflation Estimate",
        options=["Use global default", "Low (1.5%)", "Average (2.5%)", "High (4.0%)", "Custom"],
        index=2,
        help="Used to adjust future cash flows and equity for purchasing power."
    )

    if preset == "Use global default":
        inflation_rate = st.session_state.get("inflation_rate", 2.5)  # fallback if not preset
    elif preset == "Custom":
        inflation_rate = st.slider(
            "Custom Inflation Rate (%)",
            min_value=0.0,
            max_value=10.0,
            value=2.5,
            step=0.1,
            help="Set your own expected inflation rate."
        )
    else:
        try:
            inflation_rate = float(preset.split("(")[-1].replace("%)", ""))
        except ValueError:
            inflation_rate = 2.5  # safety fallback

    st.caption(f"📘 We'll adjust values for inflation using an estimated {inflation_rate:.1f}% annually.")


with tab2:
    st.subheader("📈 Stock Market Scenario")

    if use_synced_investment:
        index_investment = initial_investment  # synced from real estate tab
        st.text(f"💵 Stock Index Fund Investment: ${index_investment:,.0f} (synced from real estate scenario)")
    else:
        index_investment = st.number_input(
            "💵 Initial Amount Invested in Index Fund ($)",
            min_value=1000.0,
            value=float(initial_investment),  # prefill for continuity
            step=1000.0,
            help="Starting capital allocated to the equity market strategy."
        )

    # 📈 Market Return Scenario Picker
    market_return_option = st.selectbox(
        "📈 Annual Market Return Scenario",
        options=[
            "Custom",
            "Negative (-10.0%)",
            "Flat (0%)",
            "Conservative (5.0%)",
            "Balanced (7.0%)",
            "Aggressive (10.0%)",
            "Super Growth (15.0%)"
        ],
        index=4,
        help=(
            "Pick a preset or choose 'Custom' to set your own expected annual market return. "
            "This reflects portfolio growth from appreciation and compounding."
        )
    )

    if market_return_option == "Custom":
        annual_return = st.slider(
            "Custom Annual Return (%)",
            min_value=-50.0,
            max_value=50.0,
            value=st.session_state.get("annual_return", 7.0),
            step=0.1,
            help="Estimate how much your portfolio will grow annually, on average."
        )
    else:
        annual_return = float(market_return_option.split("(")[-1].replace("%)", ""))
    st.session_state["annual_return"] = annual_return

    # 💸 Dividend Scenario Picker
    dividend_option = st.selectbox(
        "💸 Dividend Yield Scenario",
        options=[
            "Custom",
            "None (0.0%)",
            "Moderate (1.5%)",
            "High (3.0%)"
        ],
        index=2,
        help="Choose a preset or set your own expected annual dividend yield."
    )

    if dividend_option == "Custom":
        dividend_yield = st.slider(
            "Custom Dividend Yield (%)",
            min_value=0.0,
            max_value=5.0,
            value=st.session_state.get("dividend_yield", 1.5),
            step=0.1,
            help="Annual dividends earned as a percentage of portfolio value."
        )
    else:
        dividend_yield = float(dividend_option.split("(")[-1].replace("%)", ""))
    st.session_state["dividend_yield"] = dividend_yield

    reinvest_dividends = st.checkbox(
        "📥 Reinvest Dividends Automatically",
        value=True,
        help="If checked, dividends are reinvested into the portfolio each year."
    )

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

# --- 🚀 Simulation Logic Functions ---

def simulate_real_estate_fire_contribution(
    property_value, down_payment_pct, mortgage_rate, mortgage_years,
    annual_rent, annual_expenses, rental_growth_rate,
    appreciation_rate, investment_years, inflation_rate, adjust_for_inflation, 
    closing_costs=0.0, renovation_costs=0.0, start_year=purchase_year
):
    loan_amount = property_value * (1 - down_payment_pct / 100)
    annual_debt_service = 0 if down_payment_pct == 100 else npf.pmt(
        mortgage_rate / 100 / 12, mortgage_years * 12, -loan_amount
    ) * 12

    amort_schedule = amortization_schedule(
        loan_amount, mortgage_rate, mortgage_years, investment_years, start_year
    )

    equity_records = project_property_equity(
        property_value, appreciation_rate,
        amort_schedule, inflation_rate,
        adjust_for_inflation, start_year
    )

    cashflow_records = project_cashflow(
        annual_rent, annual_expenses,
        rental_growth_rate, annual_debt_service,
        investment_years, inflation_rate, adjust_for_inflation
    )

    fire_contribution = equity_records[-1]["equity"] + sum(cashflow_records) - (closing_costs + renovation_costs)
    return fire_contribution, equity_records, cashflow_records

def simulate_equity(
    initial_investment, years, annual_return, dividend_yield, reinvest_dividends, inflation_rate=0.0, adjust_for_inflation=False
):
    portfolio_value = initial_investment
    dividends_total = 0
    growth_history = []

    for year in range(1, years + 1):
        dividends = portfolio_value * (dividend_yield / 100)
        if reinvest_dividends:
            portfolio_value += dividends
        else:
            dividends_total += dividends

        portfolio_value *= (1 + annual_return / 100)

        # Adjust this year’s values if inflation toggle is on
        if adjust_for_inflation:
            inflation_factor = (1 + inflation_rate / 100) ** year
            adjusted_value = portfolio_value / inflation_factor
            adjusted_dividends = dividends / inflation_factor
        else:
            adjusted_value = portfolio_value
            adjusted_dividends = dividends

        growth_history.append({
            "year": year,
            "portfolio_value": adjusted_value,
            "dividends": adjusted_dividends
        })

    # FIRE contribution (still based on adjusted final year value)
    fire_contribution = portfolio_value / ((1 + inflation_rate / 100) ** years) if adjust_for_inflation else portfolio_value
    fire_contribution += 0 if reinvest_dividends else dividends_total / ((1 + inflation_rate / 100) ** years)

    return fire_contribution, growth_history


# --- Real Estate Planner functions ---

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

    return schedule

def project_property_equity(purchase_price, appreciation_rate, amort_schedule, inflation_rate, adjust_for_inflation, start_year):
    equity_records = []
    for i, row in enumerate(amort_schedule):
        year = start_year + i  # 🔄 Use explicit year tracking
        value = purchase_price * ((1 + appreciation_rate / 100) ** i)
        equity = value - row["Ending Balance"]

        if adjust_for_inflation:
            inflation_factor = (1 + inflation_rate / 100) ** i
            value /= inflation_factor
            equity /= inflation_factor

        equity_records.append({
            "year": year,
            "property_value": value,
            "loan_balance": row["Ending Balance"],
            "equity": equity
        })
    return equity_records

def project_cashflow(annual_rent, annual_expenses, rental_growth_rate, annual_debt_service, years_held, inflation_rate, adjust_for_inflation):
    cashflow_records = []
    for i in range(years_held):
        rent = annual_rent * ((1 + rental_growth_rate / 100) ** i)
        expenses = annual_expenses * ((1 + inflation_rate / 100) ** i)
        net_income = rent - expenses
        cashflow = net_income - annual_debt_service
        if adjust_for_inflation:
            inflation_factor = (1 + inflation_rate / 100) ** i
            cashflow /= inflation_factor
        cashflow_records.append(cashflow)
    return cashflow_records

# Add run trigger
if st.button("▶️ Run Investment Analyzer"):

    # --- Run Simulations ---

    re_contribution, re_history, re_cashflow = simulate_real_estate_fire_contribution(
        property_value,
        down_payment_pct,
        mortgage_rate if down_payment_pct != 100 else 0,
        mortgage_years if down_payment_pct != 100 else 1,
        annual_rent,   # ✅ new input
        annual_expenses,  # ✅ new input
        rental_growth_rate,
        appreciation_rate,
        investment_years,
        inflation_rate,
        #2.5,  # inflation_rate (you can expose this too)
        adjust_for_inflation,
        closing_costs,
        renovation_costs
    )
    equity_df = pd.DataFrame(re_history)  # re_history = equity_records


    eq_contribution, eq_history = simulate_equity(
        index_investment,
        investment_years,
        annual_return,
        dividend_yield,
        reinvest_dividends,
        inflation_rate,
        adjust_for_inflation
    )

    real_estate_upfront = closing_costs + renovation_costs
    fire_yearly = []
    re_cash_cumulative = 0

    num_years = min(investment_years, len(re_history), len(re_cashflow), len(eq_history))
    for i in range(num_years):
        year = re_history[i]["year"]

        # Real Estate
        re_equity = re_history[i]["equity"]
        re_cash = re_cashflow[i]
        re_cash_cumulative += re_cash

        if i == 0:
            re_annual = re_equity + re_cash - real_estate_upfront
        else:
            re_annual = (re_equity - re_history[i-1]["equity"]) + re_cash

        re_cumulative = re_equity + re_cash_cumulative - real_estate_upfront

        # Index Fund
        eq_current = eq_history[i]["portfolio_value"]
        eq_previous = eq_history[i-1]["portfolio_value"] if i > 0 else 0
        eq_annual = eq_current - eq_previous
        eq_cumulative = eq_current

        fire_yearly.append({
            "Year": year,
            "Real Estate (Annual)": re_annual,
            "Real Estate (Cumulative)": re_cumulative,
            "Index Fund (Annual)": eq_annual,
            "Index Fund (Cumulative)": eq_cumulative
        })


    fire_df = pd.DataFrame(fire_yearly)

    # Display Results side by side

    st.subheader("📊 Investment Comparison Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🏘️ Real Estate FIRE Contribution", f"${re_contribution:,.0f}", help="Equity + rental cash flow minus closing and renovation costs.")
    with col2:
        st.metric("📈 Index Fund FIRE Contribution", f"${eq_contribution:,.0f}")

    # --- ROI Comparison (based on initial investment) ---

    real_estate_roi = re_contribution / initial_investment if initial_investment else 0
    index_fund_roi = eq_contribution / index_investment if index_investment else 0

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🏘️ Real Estate ROI",
            f"{real_estate_roi:.2f}x",
            help="Net FIRE contribution divided by total upfront investment (including closing + renovation)."
        )
    with col2:
        st.metric(
            "📈 Index Fund ROI",
            f"{index_fund_roi:.2f}x",
            help="Growth of your index portfolio compared to initial investment over the same time horizon."
        )


    # YoY Table

    st.subheader("📊 Year-by-Year FIRE Contributions")
    st.caption("💡 Year 0 reflects the upfront investment costs for the real estate strategy, resulting in a lower starting point.")

    def highlight_winner(row):
        re_value = row["Real Estate (Cumulative)"]
        eq_value = row["Index Fund (Cumulative)"]

        styles = [""] * len(row)
        if eq_value > re_value:
            styles[row.index.get_loc("Index Fund (Cumulative)")] = "background-color: lightgreen"
        elif re_value > eq_value:
            styles[row.index.get_loc("Real Estate (Cumulative)")] = "background-color: lightyellow"
        return styles

    styled_df = fire_df.style \
        .format({
            "Real Estate (Annual)": "${:,.0f}",
            "Real Estate (Cumulative)": "${:,.0f}",
            "Index Fund (Annual)": "${:,.0f}",
            "Index Fund (Cumulative)": "${:,.0f}"
        }) \
        .apply(highlight_winner, axis=1)
        
    st.dataframe(styled_df)

    # --- 🔍 Strategic Insight Summary ---

    # Analyze which strategy leads each year
    real_estate_wins = []
    index_fund_wins = []

    for row in fire_yearly:
        year = row["Year"]
        re_cum = row["Real Estate (Cumulative)"]
        eq_cum = row["Index Fund (Cumulative)"]

        if re_cum > eq_cum:
            real_estate_wins.append(year)
        elif eq_cum > re_cum:
            index_fund_wins.append(year)

    # Final winner
    if fire_yearly[-1]["Real Estate (Cumulative)"] > fire_yearly[-1]["Index Fund (Cumulative)"]:
        final_winner = "🏘️ Real estate"
    else:
        final_winner = "📈 Index fund"

    # Summary message
    st.markdown(f"""
    ### 🔍 Strategic Insight

    Based on your inputs:

    - Your **real estate investment** could generate **${re_contribution:,.0f}** over {investment_years} years via equity and rental income.
    - Your **index fund investment** is projected to grow to **${eq_contribution:,.0f}** through compound returns and dividends.

    In the year-by-year comparison table:
    - 🟨 **Real estate outpaces index fund** in {len(real_estate_wins)} of {investment_years} years.
    - 🟩 **Index fund leads** in {len(index_fund_wins)} years.

    Final outcome: **{final_winner}** is the stronger FIRE contributor over the full investment horizon.

    The table highlights:
    - 🟨 Years where real estate is ahead
    - 🟩 Years where index fund is ahead
    """)


    # # Breakeven logic

    # break_even_year = None
    # for i in range(investment_years):
    #     re_total = re_history[i]["equity"] + re_cashflow[i]
    #     eq_total = eq_history[i]["portfolio_value"]

    #     epsilon = 100  # buffer to prevent flip due to minor fluctuations
    #     if eq_total > re_total + epsilon:
    #         break_even_year = eq_history[i]["year"]
    #         break


    # # Display breakeven results

    # if break_even_year:
    #     st.success(f"📅 Break-Even Year: Your equity market investment is projected to surpass real estate in Year {break_even_year}.")
    # else:
    #     st.info("🏠 Over this time horizon, real estate remains the stronger FIRE contributor.")

    # # Final output summary

    # st.markdown(f"""
    # ### 🔍 Strategic Insight

    # Based on your inputs:

    # - Your **real estate investment** could generate **${re_contribution:,.0f}** over {investment_years} years via equity and rental income.
    # - Your **index fund investment** is projected to grow to **${eq_contribution:,.0f}** through compound returns and dividends.

    # {"The break-even point occurs in Year " + str(break_even_year) + ", when the index fund overtakes the property in total contribution." if break_even_year else "Real estate remains dominant over the full investment horizon."}
    # """)