import plotly.graph_objects as go

import streamlit as st
from calculate_fi_progress import calculate_fire_number, estimate_years_to_fi

st.image("logo.png", width=120)
st.title("🔥 FIRE Progress Tracker")
st.caption("Built with purpose by Goji Money Studio — tools for financial clarity and freedom.")

with st.expander("💡 What is FIRE and How Does This Tool Help?", expanded=True):
    st.markdown("""
**FIRE** stands for **Financial Independence, Retire Early**—a movement focused on reclaiming time, freedom, and choice by building a nest egg large enough to support your lifestyle without needing to work for money.

This tracker helps you answer one big question:

> _“How close am I to financial independence, and how long will it take me to get there?”_

### What It Calculates:
- **FIRE Number**: The amount you'd need saved to sustainably cover your future lifestyle
- **Years to FIRE**: How long it’ll take to reach that goal, given your current savings habits
- **Net Worth Trajectory**: A year-by-year look at your financial momentum
- **Progress Bar + Feedback**: Visual tools and insights to keep you motivated

Customize your inputs below and explore how your financial future unfolds.
    """)


st.header("📥 Input Your Info")

# Input fields
liquid_assets = st.number_input(
    "💰 Liquid or Investable Assets ($)",
    value=100000,
    step=1000,
    help="Include brokerage accounts, retirement accounts (401k, IRA), HSA, and cash savings. These are assets contributing to your FIRE path."
)
illiquid_assets = st.number_input(
    "🏠 Illiquid Assets (e.g. home equity) ($)",
    value=0,
    step=1000,
    help="Include your primary residence's equity, private businesses, real estate not producing income, collectibles, and other non-liquid holdings."
)
include_illiquid = st.checkbox("Include illiquid assets (e.g. home equity) in FIRE calculation?")
if include_illiquid:
    st.info("🏠 *You're including illiquid assets in your FIRE projection.*\n\nThis assumes you could sell or unlock equity from property or other non-liquid holdings—like real estate, private businesses, or collectibles.")
else:
    st.info("💰 *You're excluding illiquid assets from your FIRE projection.*\n\nThis gives a conservative view based only on accessible, investable funds like brokerage accounts, retirement accounts, and cash.")
if include_illiquid:
    current_net_worth = liquid_assets + illiquid_assets
else:
    current_net_worth = liquid_assets
st.caption("🔁 Not sure whether to include home equity in your FIRE calculation? Try toggling it on and off to see how it affects your timeline and progress. It’s a great way to model real-world tradeoffs.")
total_net_worth = liquid_assets + illiquid_assets
annual_savings = st.number_input("Annual Savings ($)", value=30000)
target_expenses = st.number_input("Target Annual Expenses at FI ($)", value=40000)
withdrawal_rate = st.slider("Safe Withdrawal Rate (%)", 3.0, 5.0, 4.0) / 100
annual_return = st.slider("Expected Annual Return (%)", 4.0, 10.0, 7.0) / 100

# Calculation trigger
if st.button("Calculate My FIRE Path"):
    fire_goal = calculate_fire_number(target_expenses, withdrawal_rate)
    years_to_fi, final_net_worth, net_worth_history = estimate_years_to_fi(
        current_net_worth, annual_savings, annual_return, fire_goal
        )

    st.subheader("🎯 Results Summary")

    st.markdown(f"""
    - **FIRE Goal:** ${fire_goal:,.0f}  
    - **Liquid Investable Assets:** ${liquid_assets:,.0f}  
    - **Illiquid Assets (e.g. home equity):** ${illiquid_assets:,.0f}  
    - **Total Net Worth:** ${total_net_worth:,.0f}  
    - **Estimated Years to FI (based on liquid assets):** {years_to_fi}  
    - **Projected Net Worth at FI:** ${final_net_worth:,.0f}
    """)


    st.subheader("🧭 Progress Toward FIRE")

    progress_pct = min(current_net_worth / fire_goal, 1.0)
    st.markdown(f"""
    **Liquid FIRE Progress:** {progress_pct * 100:.1f}%  
    **Total Net Worth:** ${total_net_worth:,.0f}  
    """)
    st.progress(progress_pct, text=f"{progress_pct * 100:.1f}% of FIRE goal reached")

    st.subheader("📣 Personalized Feedback (Based on Liquid Assets)")

    if progress_pct >= 1.0:
        st.success("🎉 Based on your liquid assets alone, you’ve reached your FIRE number! You’re financially independent—and your net worth is even higher when counting other assets.")
    elif progress_pct >= 0.75:
        st.info(f"You're {progress_pct * 100:.1f}% of the way to FIRE. So close you can smell the campfire on your freedom hikes. At this pace, you’ll get there in {years_to_fi} years.")
    elif progress_pct >= 0.5:
        st.info(f"Halfway there! You’ve built up {progress_pct * 100:.1f}% of your FIRE goal. Keep stacking—it’s all compounding from here. FIRE is {years_to_fi} years away.")
    elif progress_pct >= 0.25:
        st.info(f"You’re {progress_pct * 100:.1f}% of the way in. You’ve started something powerful—stay the course and your {years_to_fi}-year plan will pay off.")
    else:
        st.info(f"Every FIRE journey starts with that first spark. You’re {progress_pct * 100:.1f}% there. With your current pace, independence is on the horizon in about {years_to_fi} years.")



    st.subheader("📈 Net Worth Projection")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
    x=list(range(len(net_worth_history))),
    y=net_worth_history,
    mode='lines+markers',
    fill='tozeroy',
    name='Net Worth'
))

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
    text="🎯 FIRE Target",
    showarrow=True,
    arrowhead=1,
    ax=0,
    ay=-40
)

    fig.update_layout(
    xaxis_title="Years",
    yaxis_title="Net Worth ($)",
    template="plotly_white",
    showlegend=False
)

    st.plotly_chart(fig, use_container_width=True)
