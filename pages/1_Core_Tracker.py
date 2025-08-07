import plotly.graph_objects as go
import streamlit as st
from calculate_fi_progress import calculate_fire_number, estimate_years_to_fi
import pandas as pd
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

st.set_page_config(page_title="FIRE Tracker", page_icon="🔥")
st.title("🔥 FIRE Tracker")
st.caption("Find out how close you are to financial independence.")

with st.expander("💡 What Is FIRE and How Does This Tool Help?", expanded=False):
    st.markdown("""
    **FIRE** stands for **Financial Independence - Retire Early**,  a movement built around achieving freedom and flexibility by covering your lifestyle without relying on active income.

    This tool helps you quickly answer:
    """)
    st.markdown(
        "<blockquote style='color: #B00020; font-style: italic; font-size: 16px;'>“How far am I from financial independence, and what will get me there faster?”</blockquote>",
        unsafe_allow_html=True
    )
    st.markdown("""

Adjust your assumptions below and track your journey toward financial independence.
    """)

# ### What You’ll See:
# - **Your FIRE Goal Number**: How much you need to achieve freedom
# - **Time to FIRE**: Estimated years until you reach your goal
# - **Growth Path**: Year-by-year net worth projections
# - **Personalized Feedback**: Actionable insights based on your inputs

st.header("📥 Input Your Info")

# Age input
user_age = st.number_input(
    "🎂 Your Age",
    min_value=18,
    max_value=100,
    value=st.session_state.get("user_age", 35),
    help="Your age helps calculate when you can access retirement accounts like 401(k) and IRA penalty-free."
)
st.session_state["user_age"] = user_age

# Input fields
liquid_assets = st.number_input(
    "💰 Liquid or Investable Assets ($)",
    value=st.session_state.get("liquid_assets", 100000),
    step=1000,
    help="Include cash, brokerage accounts, HSA, and any other liquid assets. Exclude retirement accounts like 401(k) and IRA."
)
st.session_state["liquid_assets"] = liquid_assets

retirement_assets = st.number_input(
    "💵 Retirement-Constrained Assets (401k, IRA, etc.) ($)",
    value=st.session_state.get("retirement_assets", 400000),
    step=1000,
    help="Assets in accounts with age restrictions, like 401(k) and traditional IRAs."
)
st.session_state["retirement_assets"] = retirement_assets

illiquid_assets = st.number_input(
    "🏠 Illiquid Assets (e.g. primary home equity) ($)",
    value=st.session_state.get("illiquid_assets", 0),
    step=1000,
    help="Include equity in your primary home, private businesses, or non-liquid holdings."
)
st.session_state["illiquid_assets"] = illiquid_assets

include_illiquid = st.checkbox("Include illiquid assets (e.g. home equity) in FIRE calculation?",
    value=st.session_state.get("include_illiquid", False))
st.session_state["include_illiquid"] = include_illiquid

if include_illiquid:
    st.info("🏠 *You're including illiquid assets like real estate or collectibles in your FIRE estimate.*")
else:
    st.info("💰 *You're excluding illiquid assets for a conservative FIRE estimate based on accessible funds.*")

# Net worth assignment
# Total accessible funds for early retirement
early_access_assets = liquid_assets
# Full net worth (includes restricted retirement accounts)
current_net_worth = liquid_assets + illiquid_assets if include_illiquid else liquid_assets
total_net_worth = early_access_assets + retirement_assets + illiquid_assets

# Annual Savings
annual_savings = st.number_input(
    "Annual Savings ($)",
    value=st.session_state.get("annual_savings", 30000),
    step=100,
    help="Total annual contributions to your FIRE portfolio."
)
st.session_state["annual_savings"] = annual_savings

# Savings Growth Scenario
from shared_components import growth_picker
savings_growth, return_label= growth_picker()

# Annual Return of investments

from shared_components import return_picker
annual_return, return_label = return_picker()
#st.caption(f"📘 Using **{return_label}** scenario → {annual_return * 100:.1f}% expected annual return.")

# --- ASSUMPTIONS BLOCK ---
fire_expenses = st.number_input(
    "🔥 Annual FIRE Spending Target ($)",
    value=st.session_state.get("fire_expenses", 80000),
    step=1000,
    help="Expected yearly spending after achieving FIRE."
)
st.session_state["fire_expenses"] = fire_expenses

# Inflation Input from Shared Component
from shared_components import inflation_picker
inflation_rate = inflation_picker()

# Withdrawl Scenario
from shared_components import withdrawal_picker

withdrawal_rate, withdrawal_scenario = withdrawal_picker()
#st.caption(f"📘 Using **{withdrawal_scenario}** scenario → {withdrawal_rate * 100:.2f}% withdrawal rate.")

adjust_fire_expenses_for_inflation = st.checkbox(
    "📈 Adjust FIRE Spending for Inflation",
    value=st.session_state.get("adjust_fire_expenses_for_inflation", True)
)
st.session_state["adjust_fire_expenses_for_inflation"] = adjust_fire_expenses_for_inflation

# --- CONVERSION ---
inflation_rate /= 100

def get_effective_assets(user_age, liquid_assets, retirement_assets, fire_year, include_illiquid=False, illiquid_assets=0, access_age=59.5):
    import datetime

    current_year = datetime.datetime.now().year
    access_year = current_year + int(access_age - user_age)

    base_assets = liquid_assets + (illiquid_assets if include_illiquid else 0)

    if fire_year >= access_year:
        return (
            base_assets + retirement_assets,
            "✅ Retirement assets will be fully accessible at FIRE year.",
            {
                "bridge_years": 0,
                "reduction_factor": 1.0,
                "needs_bridge_strategy": False
            }
        )
    else:
        years_to_access = access_year - fire_year
        reduction_factor = max(0, 1 - (years_to_access / 10))
        partial_access = retirement_assets * reduction_factor
        total_assets = base_assets + partial_access

        if retirement_assets > 0:
            message = (
                f"🚧 You will reach FIRE {years_to_access} years before you can fully access retirement accounts. "
                f"We estimate you'll be able to tap into about {reduction_factor:.0%} of those assets during this early phase."
            )
        else:
            message = (
                f"🚧 You will reach FIRE {years_to_access} years before traditional retirement age, but since you've allocated $0 to retirement-restricted accounts, there's no early access needed."
            )

        bridge_info = {
            "bridge_years": years_to_access,
            "reduction_factor": reduction_factor,
            "needs_bridge_strategy": True
        }

        return total_assets, message, bridge_info



# --- CALCULATION BLOCK ---
if st.button("▶️ Calculate Years to FIRE"):

    # Step 1: FIRE Goal (Base)
    fire_goal_base = calculate_fire_number(fire_expenses, withdrawal_rate)
    this_year = datetime.datetime.now().year
    retirement_accessible = float(user_age) >= 59.5

    # Step 1.5: Get effective assets before estimation
    adjusted_expenses = fire_expenses * ((1 + inflation_rate) ** 1) if adjust_fire_expenses_for_inflation else fire_expenses  # Temporary 1-year inflation buffer for first pass
    fire_goal_base = calculate_fire_number(adjusted_expenses, withdrawal_rate)
    fire_year_guess = this_year + 1  # Temporary guess for bridge years

    effective_fire_assets, _, _ = get_effective_assets(
        user_age, liquid_assets, retirement_assets, fire_year_guess,
        include_illiquid=include_illiquid, illiquid_assets=illiquid_assets
    )

    # Step 2: First Estimation — FIRE Year
    temp_years_to_fi, _, _ = estimate_years_to_fi(effective_fire_assets, annual_savings, annual_return, fire_goal_base)
    fire_year = this_year + temp_years_to_fi

    # Step 3: Inflation Adjustment
    adjusted_expenses = fire_expenses * ((1 + inflation_rate) ** temp_years_to_fi) if adjust_fire_expenses_for_inflation else fire_expenses
    fire_goal = calculate_fire_number(adjusted_expenses, withdrawal_rate)

    # Step 4: Get Effective FIRE Assets & Bridge Message
    effective_fire_assets, bridge_message, bridge_info = get_effective_assets(
        user_age, liquid_assets, retirement_assets, fire_year,
        include_illiquid=include_illiquid, illiquid_assets=illiquid_assets
    )

    # Step 5: Final Estimation
    years_to_fi, final_net_worth, net_worth_history = estimate_years_to_fi(
    effective_fire_assets, annual_savings, annual_return, fire_goal
    )
    fire_year = this_year + years_to_fi
    fire_age = user_age + years_to_fi
    progress_pct = min(effective_fire_assets / fire_goal, 1.0)

    # Step 6: Sync Outputs
    st.session_state["fire_goal"] = fire_goal
    st.session_state["adjusted_expenses"] = adjusted_expenses
    st.session_state["years_to_fi"] = years_to_fi
    st.session_state["final_net_worth"] = final_net_worth
    st.session_state["fire_year"] = fire_year
    st.session_state["fire_age"] = fire_age
    st.session_state["progress_pct"] = progress_pct
    st.session_state["progress_basis"] = "Liquid" if not include_illiquid else "Total"
    st.session_state["calculation_run"] = True

    st.markdown("---")

    # Step 7: Headline
    if progress_pct >= 1.0:
        headline = "🎉 FIRE Achieved · You’re Financially Independent!"
    elif progress_pct >= 0.75:
        headline = f"🔥 Nearly There · Freedom Awaits in {years_to_fi} Years"
    elif progress_pct >= 0.5:
        headline = f"⛽ Halfway to FIRE · {years_to_fi} Years to Go"
    elif progress_pct >= 0.25:
        headline = f"🚀 Early Progress · {years_to_fi} Years from Freedom"
    else:
        headline = f"✨ Just Getting Started · {years_to_fi} Years to FIRE"

    st.markdown(f"""
    <h3 style='margin-top:0; color:#4a6572; font-weight:600;'>
    {headline}
    </h3>
    """, unsafe_allow_html=True)

    # Step 8: Progress Bar
    st.markdown(f"""
    <style>
    .bar-container {{
    position: relative;
    background-color: #e0e0e0;
    border-radius: 8px;
    height: 24px;
    width: 100%;
    margin-top: 10px;
    }}

    .bar-fill {{
    background-color: #4CAF50;
    width: {progress_pct * 100}%;
    height: 100%;
    border-radius: 8px;
    }}

    .current-marker {{
    position: absolute;
    top: -6px;
    left: calc({progress_pct * 100}% - 10px);
    font-size: 1.2em;
    }}

    .goal-marker {{
    position: absolute;
    top: -6px;
    right: -4px;
    font-size: 1.2em;
    opacity: 0.7;
    }}
    </style>

    <div class="bar-container">
    <div class="bar-fill"></div>
    <div class="current-marker">🏃‍♂️‍➡️</div>
    <div class="goal-marker">🎯</div>
    </div>

    <p style='margin-top:8px'><b>{progress_pct * 100:.1f}% of your FIRE journey completed (measured by assets accumulated toward your goal)</b></p>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    ### 🎯 Your FIRE Summary

    | 🎯 Milestone | 💰 Result | 🧭 What It Means for You |
    |----------------|-------------------|------------------|
    | **FIRE Goal ($)** | ${fire_goal:,.0f} | Total amount you need to retire comfortably |
    | **FIRE Year** | In {years_to_fi} years | Time until you reach financial independence |
    | **FIRE Age** | At Age {fire_age} ({fire_year})| When you expect to reach financial independence |
    | **Target FIRE Spending** | ${adjusted_expenses:,.0f} | Annual expenses starting in {fire_year} |
    | **Net Worth at FIRE** | ${final_net_worth:,.0f} | Projected total assets by the time you reach financial independence |
    | **Net Worth Today** | ${total_net_worth:,.0f} | Combined value of all assets today |
    """)
    
    st.success(bridge_message)
    if "🚧" in bridge_message and retirement_assets > 0 and progress_pct < 1.0:
        st.info("💡 To retire earlier, consider increasing liquid savings or exploring Roth IRA conversion ladders, SEPP withdrawals, or taxable asset growth. Find out more in the Advanced Planner (coming soon).")

    st.markdown("---")

# Net worth chart

    import datetime
    this_year = datetime.datetime.now().year
    year_list = [this_year + i for i in range(len(net_worth_history))]
    fire_year = this_year + years_to_fi

    fig = go.Figure()

    # Main Net Worth Line
    fig.add_trace(go.Scatter(
        x=year_list,
        y=net_worth_history,
        mode='lines+markers',
        fill='tozeroy',
        name='Net Worth'
    ))

    # 📍 "Today" marker
    fig.add_vline(
        x=this_year,
        line_dash="dot",
        line_color="#999999",
        line_width=2,
        annotation_text=f"📍 You are here ({this_year})",
        annotation_position="top left",
        annotation_font_size=12,
        annotation_font_color="#555",
        annotation_bgcolor="#f2f2f2"
    )

    # 🎯 FIRE goal line
    fig.add_shape(
        type="line",
        x0=year_list[0],
        x1=year_list[-1],
        y0=fire_goal,
        y1=fire_goal,
        line=dict(color="green", width=2, dash="dash"),
    )

    fig.add_annotation(
        x=fire_year,
        y=fire_goal,
        text=f"🎯 FIRE Target ({fire_year})",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40,
        font=dict(size=12),
        bgcolor="#e6ffe6",
        bordercolor="green",
        borderwidth=1
    )

    # 🟠 Pre-FIRE zone shading
    fig.add_vrect(
        x0=this_year,
        x1=fire_year,
        fillcolor="rgba(255,165,0,0.05)",  # faint orange
        layer="below",
        line_width=0
    )

    fig.add_annotation(
        x=this_year + (fire_year - this_year) / 2,
        y=max(net_worth_history)*0.95,
        text="Pre-FIRE accumulation phase",
        showarrow=False,
        font=dict(size=11, color="#555"),
        bgcolor="#fff8e5",
        bordercolor="#ffcc66",
        borderwidth=1
    )

    # Final layout
    fig.update_layout(
        title="📈 Net Worth Projection Over Time",
        xaxis_title="Calendar Year",
        yaxis_title="Projected Net Worth",
        template="plotly_white",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


    st.markdown("""
    ⚠️ **Note:** This tool uses a phased drawdown strategy to reflect how asset accessibility changes across retirement stages, assuming ~30 years of withdrawals.

    - Retiring in your 30s or 40s? You may need a higher FIRE number to support a longer lifespan.
    - Limited access to pre-tax accounts (401(k), IRA) before age ~59 can shift your timeline.
    - Strong savings and growth can produce similar timelines across different life stages.

    Want to go deeper into withdrawal strategies and tax planning? The **Advanced Planner** is on the way.
    """)


    # Optional prompt to explore more tools
    #st.markdown("🏡 Want to model rental income or property appreciation? Try the **Real Estate Planner** in the sidebar.")