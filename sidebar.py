# sidebar.py

import streamlit as st

def render_global_assumptions():
    with st.sidebar:
        st.markdown("## 💼 Global Assumptions")
        st.caption("These inputs apply to all FIRE tools.")

        fire_expenses = st.number_input(
            "🔥 Annual FIRE Spending Target ($)",
            min_value=0,
            value=st.session_state.get("fire_expenses", 40000),
            step=1000,
            help="How much you expect to spend each year once you’ve reached financial independence. Think: housing, food, travel, healthcare... your lifestyle costs when you’re no longer working for income."
        )
        st.session_state["fire_expenses"] = fire_expenses

        # Inflation presets
        inflation_option = st.selectbox(
            "📉 Inflation Scenario",
            options=["Custom", "Low (1.5%)", "Average (2.5%)", "High (4.0%)"],
            index=1,
            help="Choose a preset or select 'Custom' to enter your own annual inflation rate"
        )

        # Determine inflation rate based on selection
        if inflation_option == "Low (1.5%)":
            inflation_rate = 1.5
        elif inflation_option == "Average (2.5%)":
            inflation_rate = 2.5
        elif inflation_option == "High (4.0%)":
            inflation_rate = 4.0
        else:
            inflation_rate = st.number_input(
                "Custom Inflation Rate (%)",
                min_value=0.0,
                max_value=10.0,
                value=st.session_state.get("inflation_rate", 2.5),
                step=0.1,
                help="Enter your expected average annual increase in prices. Inflation reduces the value of future dollars—2.5% is historically average."
            )

        st.session_state["inflation_rate"] = inflation_rate

        # --- Withdrawal Rate Presets ---
        withdrawal_option = st.selectbox(
            "📤 Withdrawal Scenario",
            options=["Custom", "Conservative (3.0%)", "Moderate (3.5%)", "Aggressive (4.0%)"],
            index=1,
            help="Choose a preset or select 'Custom' to enter your own safe withdrawal rate"
        )

        if withdrawal_option == "Conservative (3.0%)":
            withdrawal_rate = 3.0
        elif withdrawal_option == "Moderate (3.5%)":
            withdrawal_rate = 3.5
        elif withdrawal_option == "Aggressive (4.0%)":
            withdrawal_rate = 4.0
        else:
            withdrawal_rate = st.number_input(
                "Custom Withdrawal Rate (%)",
                min_value=0.0,
                max_value=10.0,
                value=st.session_state.get("withdrawal_rate", 3.5),
                step=0.1,
                help=(
                    "The percentage of your portfolio you can safely withdraw annually in retirement "
                    "without running out of money. Common guidance ranges from 3.0% (conservative) to 4.0% (aggressive)."
                )
            )

        st.session_state["withdrawal_rate"] = withdrawal_rate
