# pages/0_Home.py
import streamlit as st

st.set_page_config(page_title="🏠 Studio Home", page_icon="💰")

# Logo and Hero Section
st.image("logo.png", width=120)
st.title("Money Matters Studio")
st.caption("Tools to master money now, so it doesn’t have to matter later.")

st.markdown("---")

# Welcome Message
st.markdown("## 🎯 Your Personal Finance Toolkit")
st.markdown(
    "Explore interactive tools to help you gain insight, plan intentionally, and reach financial independence on your terms."
)

# App Tiles
st.markdown("## 🧭 Tools")

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_Core_Tracker.py", label="🔥 **FIRE Progress Tracker**")
    st.markdown("Estimate how close you are to FIRE and how long it might take, based on your current savings, expenses, and returns.")

with col2:
    st.page_link("pages/2_Advanced_Planner.py", label="🧠 **Advanced FIRE Planner** *(Coming Soon)*")
    st.markdown("Layer in real estate, variable income, and equity unlock strategies to build a personalized FIRE plan.")

col3, col4 = st.columns(2)

with col3:
    st.page_link("pages/3_Withdrawal_Strategy.py", label="📤 **Withdrawal Strategy Designer** *(Coming Soon)*")
    st.markdown("Design a tax-aware, sustainable drawdown strategy for post-FIRE living.")

with col4:
    st.page_link("pages/4_Lifestyle_Budgeter.py", label="🎒 **Lifestyle Budgeter** *(Planned)*")
    st.markdown("Model your FI lifestyle budget and optimize spending around your values.")

st.markdown("---")

# Optional: What's New or Feedback
st.markdown("📌 **Coming Soon:** Real estate appreciation modeling, equity unlock tools, and scenario comparisons.")
st.markdown("Have feedback or feature requests? [Click here to share your thoughts](https://forms.gle/your-form-link).")
