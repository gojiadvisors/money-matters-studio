import streamlit as st
from navigation import studio_nav
if "show_summary" not in st.session_state:
    st.session_state["show_summary"] = False
from style_utils import inject_tab_style, inject_button_style

inject_tab_style()
inject_button_style()

from budget_summary_analysis import render_budget_analysis
from session_defaults import init_session_state
from lifestyle_profiles import (
    BASE_EXPENSES_BY_HOUSEHOLD,
    LOCATION_MULTIPLIERS,
    EXPENSE_CATEGORIES,
    HOUSEHOLD_TYPES,
    LOCATION_TIERS
)

# --- Initialize Session State ---
init_session_state()

# --- Expense Grouping ---
EXPENSE_GROUPS = {
    "Essentials": ["Housing", "Utilities", "Food", "Transportation", "Insurance", "Phone/Internet"],
    "Family & Health": ["Childcare", "Health & Wellness", "Education"],
    "Lifestyle": ["Subscriptions", "Discretionary", "Shopping", "Personal Care", "Travel"],
    "Financial Goals": ["Investments", "Giving"],
    "Other": ["Other"]
}

# --- Emoji Labels ---
CATEGORY_LABELS = {
    "Housing": "🏠 Housing", "Utilities": "💡 Utilities", "Food": "🍽️ Food",
    "Transportation": "🚗 Transportation", "Insurance": "🛡️ Insurance", "Phone/Internet": "📱 Phone/Internet",
    "Childcare": "🧸 Childcare", "Health & Wellness": "🩺 Health & Wellness", "Education": "🎓 Education",
    "Subscriptions": "📺 Subscriptions", "Discretionary": "🛍️ Discretionary", "Shopping": "🛒 Shopping",
    "Personal Care": "💅 Personal Care", "Travel": "✈️ Travel", "Investments": "📈 Investments",
    "Giving": "🎁 Giving", "Other": "❓ Other"
}

# --- Apply Lifestyle Template ---
def apply_expense_template():
    if st.session_state.get("expenses_customized", False):
        return  # Skip template application if user has customized expenses

    household_type = st.session_state.get("household_type")
    budget_template = st.session_state.get("budget_template")
    location_tier = st.session_state.get("location_tier")

    base_profiles = BASE_EXPENSES_BY_HOUSEHOLD.get(household_type, {})
    base_template = base_profiles.get(budget_template, {})

    multiplier = LOCATION_MULTIPLIERS.get(location_tier, 1.0)
    adjusted_template = {
        category: int(round(base_template.get(category, 0) * multiplier))
        for category in EXPENSE_CATEGORIES
    }

    st.session_state["expense_template"] = adjusted_template
    st.session_state["expense_categories"] = EXPENSE_CATEGORIES

    for category, value in adjusted_template.items():
        st.session_state[f"{category}_expense"] = value

# --- Expense Input UI ---
def render_expense_inputs():
    st.subheader("🧾 Monthly Expenses")
    st.markdown(
        f"**Lifestyle Selected:** {st.session_state.get('budget_template', 'N/A')}, "
        f"{st.session_state.get('location_tier', 'N/A')}, "
        f"{st.session_state.get('household_type', 'N/A')}"
    )

    with st.expander("Personalize your budget: enter actual expenses to override defaults.", expanded=True):
        expense_template = st.session_state.get("expense_template", {})
        expense_categories = st.session_state.get("expense_categories", [])

        for group_name, categories in EXPENSE_GROUPS.items():
            st.markdown(f"### {group_name}")
            cols = st.columns(3)

            for i, category in enumerate(categories):
                label = CATEGORY_LABELS.get(category, category)
                default_value = expense_template.get(category, 0)
                current_value = st.session_state.get(f"{category}_expense", default_value)

                with cols[i % 3]:
                    value = st.number_input(
                        label,
                        min_value=-1,
                        value=current_value,
                        step=50
                    )
                    st.session_state[f"{category}_expense"] = value

        updated_template = {
            category: st.session_state.get(f"{category}_expense", 0)
            for category in expense_categories
        }

        # Detect if user has customized any values
        if updated_template != st.session_state.get("expense_template", {}):
            st.session_state["expenses_customized"] = True

        st.session_state["expense_template"] = updated_template
        if st.button("👉 >> 📄 Generate Budget Report >>"):
            st.session_state["show_summary"] = True


# --- FIRE Input UI ---
def render_fire_inputs():
    st.subheader("🔥 FIRE Inputs")

    annual_income = st.number_input(
        "Annual After-Tax Income ($)",
        value=st.session_state.get("annual_income", 80000),
        step=1000,
        help="Your total household income after taxes. Used to assess lifestyle affordability."
    )
    st.session_state["annual_income"] = annual_income

    annual_savings = st.number_input(
        "Annual Savings ($)",
        value=st.session_state.get("annual_savings", 30000),
        step=100,
        help="How much you aim to save each year toward FIRE."
    )
    st.session_state["annual_savings"] = annual_savings

# --- Lifestyle Selector UI ---
def render_lifestyle_selector():
    st.subheader("🎯 Lifestyle Selector")

    disabled = st.session_state.get("expenses_customized", False)

    household_type = st.selectbox(
        "👥 Household Type",
        options=HOUSEHOLD_TYPES,
        index=HOUSEHOLD_TYPES.index(
            st.session_state.get("household_type", "Married with Kids")
        ),
        help="Used to scale default expenses based on household size, life stage, and financial priorities.",
        disabled=disabled
    )
    st.session_state["household_type"] = household_type

    location_tier = st.selectbox(
        "📍 Location Tier",
        options=LOCATION_TIERS,
        index=LOCATION_TIERS.index(
            st.session_state.get("location_tier", "Major Metro Area")
        ),
        help="Adjusts cost-of-living multiplier based on your geographic region.",
        disabled=disabled
    )
    st.session_state["location_tier"] = location_tier

    lifestyle_options = [
        "🧘‍♀️ Lean & Serene ($)",
        "🏡 Suburban Comfort ($$)",
        "🏙️ Urban Explorer ($$$)",
        "🎨 Creative Nomad ($$$)",
        "✈️ Jetsetter ($$$$)"
    ]

    budget_template = st.selectbox(
        "🧬 Lifestyle Template",
        options=lifestyle_options,
        index=lifestyle_options.index(
            st.session_state.get("budget_template", "🏡 Suburban Comfort ($$)")
        ),
        help="Choose a lifestyle profile to pre-fill your expense categories. You can customize them in the next tab.",
        disabled=disabled
    )
    st.session_state["budget_template"] = budget_template

    if disabled:
        st.info("You've customized your expenses. To change lifestyle presets, reset your session below.")

    if st.button("🔄 Reset Budget Session"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- Main App ---
def run_lifestyle_budgeter():
    st.title("🎒 Lifestyle Budgeter")

    with st.expander("💡 What Role Does Lifestyle Play in FIRE?", expanded=False):
        st.markdown("""
        **Lifestyle choices** shape both your day-to-day joy and your long-term financial trajectory.  
        Whether you're dreaming of Lean FIRE simplicity or Fat FIRE abundance, your spending habits define your path.

        This planner helps you answer a pivotal question:  
        <blockquote style='color: #B00020; font-style: italic; font-size: 16px;'>“Can I afford the lifestyle I want while staying on track for FIRE?”</blockquote>

        Explore templates, adjust spending tiers, and see how your lifestyle stacks up against your income and savings goals.
        """, unsafe_allow_html=True)

    st.warning("⚠️ Be sure to fill out the **FIRE Inputs**, **Lifestyle Selector**, and **Monthly Expenses** tabs below.\n\n")

    tabs = st.tabs(["🔥 FIRE Inputs", "🎯 Lifestyle Selector", "🧾 Monthly Expenses"])
    with tabs[0]:
        render_fire_inputs()
    with tabs[1]:
        render_lifestyle_selector()
        apply_expense_template()
    with tabs[2]:
        render_expense_inputs()
    
    if st.session_state.get("show_summary", False):
        st.markdown("---")
        render_budget_analysis()

        user_notes = st.text_area("📝 Add notes about this budget session (optional)", placeholder="Reflections, goals, or context...")
        st.session_state["user_notes"] = user_notes

        from utils_export import get_budget_snapshot, render_export_buttons
        snapshot = get_budget_snapshot(st.session_state)
        render_export_buttons(snapshot)

        # --- Reference Notes ---
        # with st.expander("📎 Budget Template Reference Notes", expanded=False):
        #     st.markdown("""
        #     These default values are illustrative estimates based on:
        #     - **Consumer Expenditure Survey (CES)** data from the U.S. Bureau of Labor Statistics  
        #     - **FIRE community benchmarks** from Reddit, Facebook groups, and blogs (e.g. Mr. Money Mustache, Millennial Revolution)  
        #     - **Cost-of-living calculators** from Numbeo, SmartAsset, and NerdWallet  
        #     - **Money Matters Studio’s own synthesis** of real-world FIRE scenarios and user interviews  

        #     Values are scaled by household type, lifestyle intensity, and location tier.  
        #     Users are encouraged to adjust inputs to reflect their actual spending.
        #     """)
        st.markdown("""
        <div style='font-size: 0.85em; color: #6c757d; font-style: italic; line-height: 1.4; margin-top: 2em;'>
        <b>Note:</b> These default values are illustrative estimates based on:<br><br>
        <ul style='margin-left: 1.5em;'>
        <li>Consumer Expenditure Survey (CES) data from the U.S. Bureau of Labor Statistics</li>
        <li>FIRE community benchmarks from Reddit, Facebook groups, and blogs (e.g. Mr. Money Mustache, Millennial Revolution)</li>
        <li>Cost-of-living calculators from Numbeo, SmartAsset, and NerdWallet</li>
        <li>Money Matters Studio’s own synthesis of real-world FIRE scenarios and user interviews</li>
        </ul>
        Values are scaled by household type, lifestyle intensity, and location tier.  
        Users are encouraged to adjust inputs to reflect their actual spending.
        </div>
        """, unsafe_allow_html=True)



# --- Run App ---
if __name__ == "__main__":
    studio_nav()
    run_lifestyle_budgeter()