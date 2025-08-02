import streamlit as st

# Inflation Rate

def inflation_picker(label="📈 Inflation Scenario"):
    preset_map = {
        "Low (1.5%)": 1.5,
        "Average (2.5%)": 2.5,
        "High (4.0%)": 4.0
    }

    options = ["Custom"] + list(preset_map.keys())

    # Get current session values
    current_rate = st.session_state.get("inflation_rate", 2.5)
    current_option = st.session_state.get("inflation_option", "Average (2.5%)")

    # Match dropdown label to the current rate if needed
    matched_label = next((label for label, rate in preset_map.items() if abs(rate - current_rate) < 1e-6), "Custom")
    if current_option != "Custom" and current_option != matched_label:
        current_option = matched_label
        st.session_state["inflation_option"] = current_option

    # Dropdown for preset/custom options
    selected_option = st.selectbox(
        label,
        options=options,
        index=options.index(current_option),
        key=f"{label}_dropdown",
        help="Expected long-term inflation rate. This impacts future expenses, lifestyle costs, and purchasing power across all modules."
    )

    # Input box when "Custom" is chosen
    if selected_option == "Custom":
        _, input_col = st.columns([0.05, 0.85])
        with input_col:
            inflation_rate = st.number_input(
                "↳ Custom Inflation Rate (%)",
                min_value=0.0,
                max_value=10.0,
                value=current_rate,
                step=0.1,
                key=f"{label}_custom_input",
                help="Set a custom inflation estimate. This will apply to forecasts for expenses and purchasing power."
            )
    else:
        inflation_rate = preset_map[selected_option]

    # Sync values back to session
    st.session_state["inflation_rate"] = inflation_rate
    st.session_state["inflation_option"] = selected_option

    return inflation_rate

# Portfolio Return Rate

def return_picker(default="Moderate Growth (7.0%)", allow_custom=True):
    preset_map = {
        "Income-Focused (5.0%)": 5.0,
        "Moderate Growth (7.0%)": 7.0,
        "Growth-Oriented (10.0%)": 10.0
    }

    options = ["Custom"] + list(preset_map.keys()) if allow_custom else list(preset_map.keys())

    # Load session state safely
    current_option = st.session_state.get("return_option", default)
    current_value = st.session_state.get("expected_return_percent", preset_map.get(current_option, 7.0))

    # Selectbox for scenario
    return_option = st.selectbox(
        "📊 Annual Return on Investment Scenario",
        options=options,
        index=options.index(current_option),
        help="Expected average annual growth rate across your entire portfolio."
    )
    st.session_state["return_option"] = return_option

    # Determine percent before widget renders
    if return_option == "Custom":
        _, input_col = st.columns([0.05, 0.5])
        with input_col:
            expected_return_percent = st.number_input(
                "↳ Custom Expected Annual Return (%)",
                min_value=3.0,
                max_value=12.0,
                value=current_value,
                step=0.1,
                key="return_custom_input",  # unique widget key avoids session conflicts
                help="Set your own expected return rate. This value is shared across all modules."
            )
        st.session_state["expected_return_percent"] = expected_return_percent
    else:
        expected_return_percent = preset_map[return_option]
        st.session_state["expected_return_percent"] = expected_return_percent

    return expected_return_percent / 100, return_option

# Savings Growth Scenario

def growth_picker(
    label="Annual Savings Growth Scenario",
    custom_label="↳ Custom Annual Growth (%)",
    key_prefix="growth",
    default="Flat (0.0%)",
    allow_custom=True
):
    growth_map = {
        "Flat (0.0%)": 0.0,
        "Conservative (1.0%)": 1.0,
        "Typical Merit Increase (2.0%)": 2.0,
        "Strong Career Growth (3.5%)": 3.5,
        "Temporary Setback (-1.0%)": -1.0
    }

    options = ["Custom"] + list(growth_map.keys()) if allow_custom else list(growth_map.keys())

    scenario_key = f"{key_prefix}_growth_scenario"
    value_key = f"{key_prefix}_growth_rate"
    input_key = f"{key_prefix}_custom_input"

    current_option = st.session_state.get(scenario_key, default)
    current_value = st.session_state.get(value_key, growth_map.get(current_option, 0.0))

    selected_option = st.selectbox(
        label,
        options=options,
        index=options.index(current_option),
        help="Assumes how your annual value (savings, salary, etc.) will change year over year."
    )
    st.session_state[scenario_key] = selected_option

    if selected_option == "Custom":
        # Indented input using columns
        _, input_col = st.columns([0.05, 0.5])
        with input_col:
            growth_rate = st.number_input(
                custom_label,
                min_value=-5.0,
                max_value=10.0,
                value=current_value,
                step=0.05,
                key=input_key,
                help="Define your custom annual growth rate. This value will apply across all modules."
            )
        st.session_state[value_key] = growth_rate
    else:
        growth_rate = growth_map[selected_option]
        st.session_state[value_key] = growth_rate

    return growth_rate / 100, selected_option

# Withdrawal Picker

def withdrawal_picker(default="Moderate (3.5%)", allow_custom=True):
    preset_map = {
        "Conservative (3.0%)": 3.0,
        "Moderate (3.5%)": 3.5,
        "Flexible FIRE (4.0%)": 4.0
    }

    options = ["Custom"] + list(preset_map.keys()) if allow_custom else list(preset_map.keys())

    # Get saved selections
    current_option = st.session_state.get("withdrawal_option", default)
    current_value = st.session_state.get("withdrawal_rate", preset_map.get(current_option, 3.5))

    # Scenario selection
    withdrawal_option = st.selectbox(
        "📤 Withdrawal Scenario",
        options=options,
        index=options.index(current_option),
        help="Expected annual withdrawal rate in retirement or financial independence. Affects portfolio sustainability."
    )
    st.session_state["withdrawal_option"] = withdrawal_option

    if withdrawal_option == "Custom":
        _, input_col = st.columns([0.05, 0.95])
        with input_col:
            withdrawal_rate = st.number_input(
                "↳ Custom Withdrawal Rate (%)",
                min_value=0.0,
                max_value=10.0,
                value=current_value,
                step=0.05,
                key="withdrawal_custom_input",
                help="Set your own withdrawal rate. Impacts how long your portfolio will last under simulated conditions."
            )
        st.session_state["withdrawal_rate"] = withdrawal_rate
    else:
        withdrawal_rate = preset_map[withdrawal_option]
        st.session_state["withdrawal_rate"] = withdrawal_rate

    return withdrawal_rate / 100, withdrawal_option

# Rental growth/decline rate

def rental_growth_picker(default="Moderate Growth (1.5%)", allow_custom=True):
    """
    Rental income growth scenario selector for FIRE planning tools.
    Includes preset growth/decline scenarios and optional custom input.
    Syncs selection and value to session state.
    """
    import streamlit as st

    preset_map = {
        "Decline (-2.0%)": -2.0,
        "Flat (0.0%)": 0.0,
        "Moderate Growth (1.5%)": 1.5,
        "Aggressive Growth (5.0%)": 5.0
    }

    options = ["Custom"] + list(preset_map.keys()) if allow_custom else list(preset_map.keys())

    # Get saved selections
    current_option = st.session_state.get("rental_growth_option", default)
    current_value = st.session_state.get("rental_growth_rate", preset_map.get(current_option, 2.0))

    # Scenario selection
    rental_growth_option = st.selectbox(
        "🏘️ Rental Income Growth Scenario",
        options=options,
        index=options.index(current_option),
        help="Expected annual change in rental income. Decline reflects shrinking rents, while growth boosts future FIRE contribution."
    )
    st.session_state["rental_growth_option"] = rental_growth_option

    if rental_growth_option == "Custom":
        _, input_col = st.columns([0.05, 0.95])
        with input_col:
            rental_growth_rate = st.number_input(
                "↳ Custom Rental Growth Rate (%)",
                min_value=-10.0,
                max_value=10.0,
                value=current_value,
                step=0.1,
                key="rental_growth_custom_input",
                help="Set expected annual change in rental income. For example, -2.0 means declining rental returns over time."
            )
        st.session_state["rental_growth_rate"] = rental_growth_rate
    else:
        rental_growth_rate = preset_map[rental_growth_option]
        st.session_state["rental_growth_rate"] = rental_growth_rate

    return rental_growth_rate

# Market Return Scenario Picker
def equity_return_picker(default="Balanced (7.0%)", allow_custom=True):
    """
    Equity market return scenario picker.
    Presets reflect asset-class-level returns.
    Avoids session state conflicts with other pickers.
    """

    import streamlit as st

    preset_map = {
        "Negative (-10.0%)": -10.0,
        "Flat (0%)": 0.0,
        "Conservative (5.0%)": 5.0,
        "Balanced (7.0%)": 7.0,
        "Aggressive (10.0%)": 10.0,
        "Super Growth (15.0%)": 15.0
    }

    options = ["Custom"] + list(preset_map.keys()) if allow_custom else list(preset_map.keys())

    # Safely load equity-specific session state
    current_option = st.session_state.get("equity_return_option", default)
    current_value = st.session_state.get("equity_annual_return", preset_map.get(current_option, 7.0))

    # Scenario selector
    return_option = st.selectbox(
        "📈 Equity Market Return Scenario",
        options=options,
        index=options.index(current_option),
        help="Annualized expected return for the equity portion of your portfolio. Choose a preset or enter a custom rate."
    )
    st.session_state["equity_return_option"] = return_option

    # Determine value from input or preset
    if return_option == "Custom":
        _, input_col = st.columns([0.05, 0.95])
        with input_col:
            annual_return = st.number_input(
                "↳ Custom Equity Return (%)",
                min_value=-50.0,
                max_value=50.0,
                value=current_value,
                step=0.1,
                key="equity_return_custom_input",
                help="Specify expected annualized return for equities, accounting for volatility or bullish outlooks."
            )
        st.session_state["equity_annual_return"] = annual_return
    else:
        annual_return = preset_map[return_option]
        st.session_state["equity_annual_return"] = annual_return

    return annual_return, return_option

