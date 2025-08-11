import streamlit as st
import numpy_financial as npf
import pandas as pd
import plotly.graph_objects as go
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

st.markdown("""
    <style>
    div[data-testid="stButton"] button {
        padding: 2px 6px;
        font-size: 0.75rem;
        background-color: #f9f9f9;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-shadow: none;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Page Setup ---
st.set_page_config(page_title="Investment Analyzer", page_icon="📊")

st.title("📊 Investment Analyzer")
st.caption("Compare investment strategies (🏘️ real estate vs. 📈 stock market) to see which accelerates your FIRE timeline more efficiently.")

with st.expander("💡 Which Investment Leads to FIRE Faster?", expanded=False):
    st.markdown("""
Choosing between **real estate** and **stock market** can shape the pace and flexibility of your path to financial independence.

This module helps you answer the essential FIRE question:

<blockquote style='color: #B00020; font-style: italic; font-size: 16px;'>“Should I invest in property or the stock market? Which one gets me to FIRE faster?”</blockquote>

This tool lets you simulate assumptions, explore trade-offs, and uncover the most effective wealth-building route based on your timeline and risk comfort.
""", unsafe_allow_html=True)

# ### What It Compares:
# - 🏘️ **Real Estate**: Net cash flow, equity buildup, and appreciation over time  
# - 📈 **Equity Markets**: Portfolio growth through compounding, dividend reinvestment, and consistent contributions
# - 🧮 **Total FIRE Contribution**: Real estate vs stock market outcomes, adjusted for net investment impact
# - 🔁 **Break-Even Analysis**: Year-by-year comparison to spotlight when one strategy pulls ahead


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
st.session_state["purchase_year"] = purchase_year

investment_years = st.slider(
    "📅 Investment Duration (Years)",
    min_value=1,
    max_value=50,
    value=st.session_state.get("years_held", 15),
    help="How long you plan to hold this investment before selling or retiring."
)
st.session_state["years_held"] = investment_years

st.markdown("### 📂 Input Assumptions for Both Investment Paths")
st.warning(
    "⚠️ To compare real estate and stock market, be sure to enter your assumptions for **BOTH** tabs.\n\n"
    # "🔹 Start with your property details in **Real Estate**\n\n"
    # "🔹 Then switch to **Equity Market** to configure stock-based growth assumptions"
)

#use_synced_investment = True  # You can later make this a checkbox toggle if desired
use_synced_investment = st.checkbox("🔗 Use same investment amount for both strategies", value=True)

# Inject tab styling
st.markdown("""
    <style>
    button[aria-selected="true"] {
        background-color: #ffe082 !important;
        color: #333 !important;
        border-bottom: 3px solid #ffb300 !important;
        border-radius: 6px 6px 0 0 !important;
        font-weight: 600 !important;
        padding: 12px 20px !important;  /* Wider padding */
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);  /* Optional depth */
    }

    button[aria-selected="false"] {
        background-color: #fff8e1 !important;
        color: #333 !important;
        border-radius: 6px 6px 0 0 !important;
        font-weight: 500 !important;
        padding: 12px 20px !important;
    }

    button[aria-selected]:hover {
        background-color: #ffecb3 !important;
    }
    </style>
""", unsafe_allow_html=True)




# Tabs for scenario input
tab1, tab2 = st.tabs(["🏘️ Real Estate", "📈 Stock Market"])

with tab1:
    st.subheader("🏘️ Real Estate Scenario")

    all_cash_purchase = st.checkbox("🪙 Buy with All Cash (No Mortgage)", value=False)

    property_value = st.number_input(
        "🏠 Property Purchase Price ($)",
        min_value=50000,
        step=10000,
        value=st.session_state.get("purchase_price", 400000),
        help="Full market price of the property you'd like to invest in."
    )
    st.session_state["purchase_price"] = property_value

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
        st.session_state["down_payment_pct"] = down_payment_pct
        initial_investment = property_value * (down_payment_pct / 100) + closing_costs + renovation_costs

        mortgage_years = st.number_input(
            "📅 Loan Term (years)",
            min_value=1,
            max_value=40,
            value=st.session_state.get("mortgage_years", 30),
            step=1,
            help="Length of your mortgage, typically 15–30 years."
        )
        st.session_state["mortgage_years"] = mortgage_years

        mortgage_rate = st.number_input(
            "📈 Mortgage Interest Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state.get("mortgage_rate", 6.0),
            step=0.1,
            help="Annual interest rate charged on the loan."
        )
        st.session_state["interest_rate"] = mortgage_rate

    
    # -- Performance Assumptions --
    appreciation_rate = st.number_input(
        "📈 Property Appreciation Rate (%)",
        min_value=0.0,
        value=st.session_state.get("appreciation_rate", 3.0),
        step=0.1,
        help="Expected annual increase in property value, compounded yearly (e.g. 3 means ~3% growth per year)."
    )
    st.session_state["appreciation_rate"] = appreciation_rate

    annual_rent = st.number_input(
        "🏡 Annual Rental Income ($)",
        min_value=0,
        value=st.session_state.get("annual_rent", 24000),
        step=1000,
        help="Gross rent expected from tenants in one year — before expenses or vacancy adjustments."
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
    help="Total costs per year including tax, maintenance, insurance, and management."
)
    st.session_state["annual_expenses"] = annual_expenses

    
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
#with st.expander("📉 Inflation Scenario", expanded=True):
    # Inflation Input from Shared Component
    from shared_components import inflation_picker
    inflation_rate = inflation_picker()
    #st.caption(f"📘 We'll adjust values for inflation using an estimated {inflation_rate:.1f}% annually.")

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
    from shared_components import equity_return_picker
    equity_return, equity_label = equity_return_picker()

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
    initial_investment, years, equity_return, dividend_yield, reinvest_dividends, inflation_rate=0.0, adjust_for_inflation=False
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

        portfolio_value *= (1 + equity_return / 100)

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
    
    st.markdown("---")

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
        equity_return,
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

    # # Display Results side by side

    # st.subheader("📊 Investment Comparison Summary")

    # col1, col2 = st.columns(2)

    # with col1:
    #     st.metric("🏘️ Real Estate FIRE Contribution", f"${re_contribution:,.0f}", help="Equity + rental cash flow minus closing and renovation costs.")
    # with col2:
    #     st.metric("📈 Index Fund FIRE Contribution", f"${eq_contribution:,.0f}")

    # # --- ROI Comparison (based on initial investment) ---

    # col1, col2 = st.columns(2)

    # with col1:
    #     st.metric(
    #         "🏘️ Real Estate ROI",
    #         f"{real_estate_roi:.2f}x",
    #         help="Net FIRE contribution divided by total upfront investment (including closing + renovation)."
    #     )
    # with col2:
    #     st.metric(
    #         "📈 Index Fund ROI",
    #         f"{index_fund_roi:.2f}x",
    #         help="Growth of your index portfolio compared to initial investment over the same time horizon."
    #     )
    
    real_estate_roi = re_contribution / initial_investment if initial_investment else 0
    index_fund_roi = eq_contribution / index_investment if index_investment else 0

    st.markdown(f"""
    ### 📊 Investment Comparison Summary

    <table style="width:100%; border-collapse: collapse;">
        <thead>
            <tr style="background-color:#f2f2f2;">
                <th style="text-align: left; padding: 8px;">📁 Metric</th>
                <th style="text-align: left; padding: 8px;">🏘️ Real Estate</th>
                <th style="text-align: left; padding: 8px;">📈 Stock Index Fund</th>
                <th style="text-align: left; padding: 8px;">💡 What It Means</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="padding: 8px;">🔥 FIRE Contribution</td>
                <td style="padding: 8px;">${re_contribution:,.0f}</td>
                <td style="padding: 8px;">${eq_contribution:,.0f}</td>
                <td style="padding: 8px;">How much each strategy contributes toward financial independence and early retirement.</td>
            </tr>
            <tr>
                <td style="padding: 8px;">📈 ROI Multiple</td>
                <td style="padding: 8px;">{real_estate_roi:.2f}x</td>
                <td style="padding: 8px;">{index_fund_roi:.2f}x</td>
                <td style="padding: 8px;">The total return on investment relative to the initial capital (higher means more growth).</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # Strategy Comparison Chart
    #
    #st.markdown("### 🔍 Visual Comparison of Cumulative FIRE Contributions")
    #st.subheader("📊 Year-by-Year FIRE Contributions")

    comparison_fig = go.Figure()

    comparison_fig.add_trace(go.Scatter(
        x=fire_df["Year"],
        y=fire_df["Real Estate (Cumulative)"],
        mode="lines+markers",
        name="Real Estate",
        line=dict(color="goldenrod"),
        hovertemplate="Real Estate: $%{y:,.0f}<br>Year %{x}"
    ))

    comparison_fig.add_trace(go.Scatter(
        x=fire_df["Year"],
        y=fire_df["Index Fund (Cumulative)"],
        mode="lines+markers",
        name="Index Fund",
        line=dict(color="green", dash="dot"),
        hovertemplate="Index Fund: $%{y:,.0f}<br>Year %{x}"
    ))

    comparison_fig.update_layout(
        template="plotly_white",
        xaxis_title="Year",
        yaxis_title="Cumulative Value ($)",
        title="📈 FIRE Path Comparison Over Time",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        margin=dict(t=60, b=100)
    )

    # Initialize breakeven year
    breakeven_year = None

    for i in range(len(fire_df)):
        re_value = fire_df["Real Estate (Cumulative)"].iloc[i]
        eq_value = fire_df["Index Fund (Cumulative)"].iloc[i]
        if re_value > eq_value:
            breakeven_year = fire_df["Year"].iloc[i]
            break

    if breakeven_year:
        comparison_fig.add_annotation(
            x=breakeven_year,
            y=fire_df.loc[fire_df["Year"] == breakeven_year, "Real Estate (Cumulative)"].values[0],
            text=f"🏁 Breakeven in {breakeven_year}",
            showarrow=True,
            arrowhead=2,
            ax=30,
            ay=30,  # Pulls annotation toward lower-right
            textangle=0,
            bgcolor="lightyellow",
            bordercolor="darkgoldenrod",
            font=dict(size=12),
            xref="x",
            yref="y"
        )
    else:
        comparison_fig.add_annotation(
            xref="paper", yref="paper",
            x=0.99, y=0.15,
            showarrow=False,
            text="⚠️ No breakeven: Index Fund leads throughout",
            font=dict(size=13),
            bgcolor="lightgreen",
            bordercolor="darkgreen"
        )

    final_year = fire_df["Year"].iloc[-1]
    final_re = fire_df["Real Estate (Cumulative)"].iloc[-1]
    final_eq = fire_df["Index Fund (Cumulative)"].iloc[-1]

    winner_text = (
        "🏆 Real Estate wins long-term" if final_re > final_eq
        else "🏆 Index Fund wins long-term" if final_eq > final_re
        else "⚖️ Both strategies finish evenly"
    )

    comparison_fig.add_annotation(
        x=final_year,
        y=max(final_re, final_eq),
        text=winner_text,
        showarrow=False,
        font=dict(size=14, color="black"),
        bgcolor="lightgray",
        bordercolor="gray"
    )

    st.plotly_chart(comparison_fig, use_container_width=True)
    #st.caption("🏁 Track how each strategy contributes to your financial independence year by year — with upfront investments reflected in Year 0.")

    # Pre-format values
    re_total = f"${final_re:,.0f}"
    eq_total = f"${final_eq:,.0f}"
    breakeven = str(breakeven_year)

    # Generate summary paragraph with HTML tags
    if breakeven_year:
        summary = (
            f"<p>Over the modeled period, the real estate strategy begins to outperform index investing starting in <strong>{breakeven}</strong>, "
            f"ultimately contributing <strong>{re_total}</strong> toward your financial independence journey. "
            f"This includes both rental income and equity growth, net of upfront costs. "
            f"The index fund strategy, while steadier, finishes with a total contribution of <strong>{eq_total}</strong>, "
            f"making real estate the stronger performer in this scenario.</p>"
        )
    else:
        summary = (
            f"<p>Throughout the modeled period, the index fund strategy consistently contributes more toward your financial independence goal, "
            f"ending with a total of <strong>{eq_total}</strong>. The real estate strategy, while valuable, finishes with <strong>{re_total}</strong>, "
            f"reflecting the impact of upfront costs and slower early growth. "
            f"In this scenario, index investing offers a more reliable path to FIRE.</p>"
        )

    # Display in Streamlit
    st.markdown(summary, unsafe_allow_html=True)

    st.markdown("---")

    with st.expander("📊 Year-by-Year FIRE Contribution Comparison", expanded=False):

        # YoY Table

        # Reset index and drop the "Year" column (assuming it's the index)
        fire_df_display = fire_df.reset_index(drop=True)

        # Or if "Year" becomes a column after reset and you want to drop it:
        # fire_df_display = fire_df.reset_index().drop(columns=["Year"])

        # Highlight function stays the same
        def highlight_winner(row):
            re_value = row["Real Estate (Cumulative)"]
            eq_value = row["Index Fund (Cumulative)"]
            styles = [""] * len(row)
            if eq_value > re_value:
                styles[row.index.get_loc("Index Fund (Cumulative)")] = "background-color: lightgreen"
            elif re_value > eq_value:
                styles[row.index.get_loc("Real Estate (Cumulative)")] = "background-color: lightyellow"
            return styles

        # Apply formatting and highlighting to modified DataFrame
        styled_df = fire_df_display.style \
            .format({
                "Real Estate (Annual)": "${:,.0f}",
                "Real Estate (Cumulative)": "${:,.0f}",
                "Index Fund (Annual)": "${:,.0f}",
                "Index Fund (Cumulative)": "${:,.0f}"
            }) \
            .apply(highlight_winner, axis=1)

        # Display without the index column
        st.subheader("📊 Year-by-Year FIRE Contributions")
        st.caption("💡 Year 0 reflects the upfront investment costs for the real estate strategy, resulting in a lower starting point.")
        st.dataframe(styled_df, hide_index=True)


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