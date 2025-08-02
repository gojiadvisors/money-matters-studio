import plotly.graph_objects as go
import streamlit as st
from calculate_fi_progress import calculate_fire_number, estimate_years_to_fi
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
### What You’ll See:
- **Your FIRE Goal Number**: How much you need to achieve freedom
- **Time to FIRE**: Estimated years until you reach your goal
- **Growth Path**: Year-by-year net worth projections
- **Personalized Feedback**: Actionable insights based on your inputs

Adjust your assumptions below and track your journey toward financial independence.
    """)

st.header("📥 Input Your Info")

# Input fields
liquid_assets = st.number_input(
    "💰 Liquid or Investable Assets ($)",
    value=st.session_state.get("liquid_assets", 100000),
    step=1000,
    help="Include brokerage accounts, retirement accounts (401k, IRA), HSA, and cash savings."
)
st.session_state["liquid_assets"] = liquid_assets

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

# Net worth assignment (already handled)
current_net_worth = liquid_assets + illiquid_assets if include_illiquid else liquid_assets
total_net_worth = liquid_assets + illiquid_assets

# Add optional caption below inputs
#st.caption("🔍 Not sure whether to include home equity in your FIRE calculation? Try toggling it on and off to see how it affects your timeline and progress. But note: real estate cash flow and appreciation are handled in a separate module.")

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

# --- CALCULATION BLOCK ---
if st.button("🔥 Calculate Years to FIRE"):

    # Initial approximation (without inflation)
    fire_goal_base = calculate_fire_number(fire_expenses, withdrawal_rate)
    years_to_fi, _, _ = estimate_years_to_fi(current_net_worth, annual_savings, annual_return, fire_goal_base)

    # Now adjust for inflation if enabled
    adjusted_expenses = fire_expenses * ((1 + inflation_rate) ** years_to_fi) if adjust_fire_expenses_for_inflation else fire_expenses
    fire_goal = calculate_fire_number(adjusted_expenses, withdrawal_rate)
    years_to_fi, final_net_worth, net_worth_history = estimate_years_to_fi(current_net_worth, annual_savings, annual_return, fire_goal)

    this_year = datetime.datetime.now().year
    fire_year = this_year + years_to_fi

    progress_pct = min(current_net_worth / fire_goal, 1.0)

    # ✅ Sync Outputs
    st.session_state["fire_goal"] = fire_goal
    st.session_state["adjusted_expenses"] = adjusted_expenses
    st.session_state["years_to_fi"] = years_to_fi
    st.session_state["final_net_worth"] = final_net_worth
    st.session_state["fire_year"] = fire_year
    st.session_state["progress_pct"] = progress_pct
    st.session_state["progress_basis"] = "Liquid" if not include_illiquid else "Total"
    st.session_state["calculation_run"] = True

    # Divider
    st.markdown("<hr style='margin-top:20px; margin-bottom:20px;'>", unsafe_allow_html=True)
    
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

    st.subheader("🎯 FIRE Results Summary")

    st.markdown(f"""
    - **FIRE Goal:** ${fire_goal:,.0f}  
    - **Target FIRE Spending in Year {fire_year}:** ${adjusted_expenses:,.0f} {"(inflation-adjusted)" if adjust_fire_expenses_for_inflation else "(flat spending)"}  
    - **Liquid Investable Assets Today:** ${liquid_assets:,.0f}  
    - **Illiquid Assets Today (e.g. home equity):** ${illiquid_assets:,.0f}  
    - **Total Net Worth Today:** ${total_net_worth:,.0f}  
    - **Estimated Years to FIRE (based on liquid assets):** {years_to_fi}  
    - **Projected Net Worth at FIRE:** ${final_net_worth:,.0f}
    """)

    st.subheader("🧭 How close are you to FIRE?")
    
    #st.progress(progress_pct, text=f"{progress_pct * 100:.1f}% of FIRE goal reached")

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

    <p style='margin-top:8px'><b>{progress_pct * 100:.1f}% of FIRE goal reached</b></p>
    """, unsafe_allow_html=True)

    # st.subheader("📣 A Message for you")

    # if progress_pct >= 1.0:
    #     st.success("🎉 Based on your liquid assets alone, you’ve reached your FIRE number! You’re financially independent—and your net worth is even higher when counting other assets.")
    # elif progress_pct >= 0.75:
    #     st.info(f"You're {progress_pct * 100:.1f}% of the way to FIRE. So close you can smell the campfire on your freedom hikes. At this pace, you’ll get there in {years_to_fi} years.")
    # elif progress_pct >= 0.5:
    #     st.info(f"Halfway there! You’ve built up {progress_pct * 100:.1f}% of your FIRE goal. Keep stacking—it’s all compounding from here. FIRE is {years_to_fi} years away.")
    # elif progress_pct >= 0.25:
    #     st.info(f"You’re {progress_pct * 100:.1f}% of the way in. You’ve started something powerful—stay the course and your {years_to_fi}-year plan will pay off.")
    # else:
    #     st.info(f"Every FIRE journey starts with that first spark. You’re {progress_pct * 100:.1f}% there. With your current pace, independence is on the horizon in about {years_to_fi} years.")


    st.subheader("📈 Net Worth Projection")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
    x=list(range(len(net_worth_history))),
    y=net_worth_history,
    mode='lines+markers',
    fill='tozeroy',
    name='Net Worth'
))

    import datetime
    this_year = datetime.datetime.now().year
    fire_year = this_year + years_to_fi

    # 📍 Add marker for Year 0 ("Today")
    fig.add_vline(
    x=0,
    line_dash="dot",
    line_color="#999999",
    line_width=2,
    annotation_text=f"📍 You are here ({this_year})",
    annotation_position="top left",
    annotation_font_size=12,
    annotation_font_color="#555",
    annotation_bgcolor="#f2f2f2"
)

    # Add FIRE goal line
    fig.add_shape(
    type="line",
    x0=0,
    x1=len(net_worth_history),
    y0=fire_goal,
    y1=fire_goal,
    line=dict(color="green", width=2, dash="dash"),
)

    # Add annotation
    fig.add_annotation(
    x=years_to_fi,
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

    # Pre-FIRE zone
    fig.add_vrect(
    x0=0,
    x1=years_to_fi,
    fillcolor="rgba(255,165,0,0.05)",  # faint orange
    layer="below",
    line_width=0
)

# Optional: Add annotation
    fig.add_annotation(
    x=years_to_fi / 2,
    y=max(net_worth_history)*0.95,
    text="Pre-FIRE accumulation phase",
    showarrow=False,
    font=dict(size=11, color="#555"),
    bgcolor="#fff8e5",
    bordercolor="#ffcc66",
    borderwidth=1
)


    fig.update_layout(
    title="Net Worth Projection Over Time",
    xaxis_title="Years from Today",
    yaxis_title="Projected Net Worth",
    template="plotly_white",
    showlegend=False
)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ⚠️ **Important note:**  
    This tool assumes your retirement will span about 30 years, following standard safe withdrawal guidelines. 
    If you expect a longer retirement (such as retiring in your 30s or 40s), you may need a higher FIRE Goal number. 
    For deeper analysis, check out the Advanced Planner (coming soon).
    """)

    # Optional prompt to explore more tools
    #st.markdown("🏡 Want to model rental income or property appreciation? Try the **Real Estate Planner** in the sidebar.")