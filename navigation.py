import streamlit as st


def studio_nav():
    return st.navigation([
        st.Page("pages/0_Home.py", title="🏠 Money Matters Studio Home"),
        st.Page("pages/1_Core_Tracker.py", title="🔥 FIRE Tracker"),
        st.Page("pages/5_Real_Estate_Planner.py", title="🏘️ Real Estate Planner"),
        st.Page("pages/6_Investment_Comparison_Tool.py", title="📊 Investment Comparison Tool"),
        st.Page("pages/2_Advanced_Planner.py", title="🧠 Advanced Planner"),
        st.Page("pages/3_Withdrawal_Strategy.py", title="📤 Withdrawal Designer"),
        st.Page("pages/4_Lifestyle_Budgeter.py", title="🎒 Lifestyle Budgeter")
        
    ])
