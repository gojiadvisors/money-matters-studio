# pages/0_Home.py
import streamlit as st

st.set_page_config(page_title="Studio Home", page_icon="💰")

# Logo and Hero Section
col1, col2 = st.columns([5, 1])
with col1:
    st.title("💰 Money Matters Studio")
    st.caption("Tools to master money now, so money doesn’t have to matter later.")
with col2:
    st.image("logo.png", width=100)

st.markdown("---")

# Welcome Message
st.markdown("### 🧰 Your Financial Toolkit")

st.markdown("""
| Tool | What Is It? | Real Estate? | Integrated? |
|------|---------------|---------------------|--------------------------|
| [🔥 **FIRE Progress Tracker**](https://money-matters-studio.streamlit.app/Core_Tracker) | Estimate your time to FIRE based on savings, expenses, and returns | ❌ | 🔜 Will integrate with Advanced Planner |
| [🏘️ **Real Estate Planner**](phttps://money-matters-studio.streamlit.app/Real_Estate_Planner) | Model rental income, appreciation, and mortgage payoff over time | ✅ | ✅ Feeds into Advanced Planner |
| 🧠 **Advanced FIRE Planner** | Combine real estate, side income, and equity events to customize your path | ✅ | ✅ Synthesizes all tools |
| 📤 **Withdrawal Strategy Designer** | Design a tax-aware, sustainable withdrawal strategy post-FIRE | ❌ | 🔄 Uses FIRE Tracker results |
| 🎒 **Lifestyle Budgeter** | Build your ideal FIRE lifestyle and optimize your spending | ❌ | 🔄 Helps define FIRE goal |
""")


st.caption("📎 This table will grow as your toolkit evolves. Real estate support is modular by design - use only what fits your FIRE journey.")
st.markdown("---")
st.markdown("### 🚀 Not Sure Where to Start?")
st.markdown("Start here:")

st.page_link("pages/1_Core_Tracker.py", label="🔥 FIRE Progress Tracker")
st.caption("Your baseline projection tool. Estimate how long it’ll take to reach FIRE based on liquid savings, income, and expenses.")

st.page_link("pages/5_Real_Estate_Planner.py", label="🏘️ Real Estate Planner")
st.caption("See how a rental property could boost your wealth and speed up your timeline.")

st.page_link("pages/2_Advanced_Planner.py", label="🧠 Advanced Planner (Coming Soon)")
st.caption("Eventually, use all your data sources to create a master forecast.")

st.markdown("---")
st.markdown(
    "<div style='text-align: left; font-size: 15px;'>"
    "🔗 Visit the full studio site at "
    "<a href='https://money-matters-studio.super.site/' target='_blank' style='text-decoration: none; color: #4B8BBE;'>Money Matters Studio</a> "
    "for more tools, updates, resources, or contact us to give us suggestions and feedback."
    "</div>",
    unsafe_allow_html=True
)