# pages/0_Home.py
import streamlit as st

st.set_page_config(page_title="Studio Home", page_icon="💰")

# Logo and Hero Section
col1, col2 = st.columns([5, 1])
with col1:
    st.title("💰 Money Matters Studio")
    st.caption("Your one-stop shop for tools to master money now, so money doesn’t have to matter later.")
with col2:
    st.image("logo.png", width=100)

st.markdown("""
---
### 🔍 FIRE Essential Tools""")
st.caption("*FIRE = Financial Independence - Retire Early")

st.markdown("""

| 🔧 Tool | 💡 What It Does | 🚦 Status |
|--------|------------------|------------|
| [🔥 **FIRE Tracker**](https://money-matters-studio.streamlit.app/Core_Tracker) | Estimate time to FIRE from savings, expenses, and returns | ✅ Live |
| 🎒 **Lifestyle Budgeter** (https://money-matters-studio.streamlit.app/Lifestyle_Budgeter)  | Build your ideal FIRE lifestyle and optimize spending | 🧪 Beta |
| 📤 **Withdrawal Designer** | Design a tax-aware, sustainable withdrawal strategy post-FIRE | 🛠️ Coming Soon |

---

### 🏗️ Advanced Planning Tools

| 🛠️ Tool | 📈 What It Models | 🚦 Status |
|--------|-------------------|------------|
| [🏘️ **Real Estate Planner**](https://money-matters-studio.streamlit.app/Real_Estate_Planner) | Rental income, appreciation, and mortgage payoff over time | ✅ Live |
| [📊 **Investment Analyzer**](https://money-matters-studio.streamlit.app/Investment_Analyzer) | Compare real estate and stock market strategies using synced assumptions | ✅ Live |
| 🧠 **Advanced FIRE Planner** | Combine real estate, side income, and equity events for a tailored path | 🛠️ Coming Soon |

""")


st.caption("✨ More modules coming soon!")
#st.caption("📎 This table will grow as your toolkit evolves. Real estate support is modular by design - use only what fits your FIRE journey.")
st.markdown("---")
st.markdown("### 🚀 Not Sure Where to Start?")
st.markdown("Try following this path:")

st.page_link("pages/1_Core_Tracker.py", label="🔥 FIRE Tracker")
st.caption("Your baseline projection tool. Estimate time to FIRE based on income, savings, and expenses.")

st.page_link("pages/5_Real_Estate_Planner.py", label="🏘️ Real Estate Planner")
st.caption("Model rental income, property appreciation, and mortgage payoff over time.")

st.page_link("pages/6_Investment_Analyzer.py", label="📊 Investment Analyzer")
st.caption("Compare real estate vs. index fund strategies using synced assumptions from other tools.")

st.page_link("pages/2_Advanced_Planner.py", label="🧠 Advanced Planner (Coming Soon)")
st.caption("Eventually, combine all tools to build a master forecast that reflects your full FIRE strategy.")

st.markdown("---")
st.markdown(
    "<div style='text-align: left; font-size: 15px;'>"
    "🔗 Visit the full studio site at "
    "<a href='https://money-matters-studio.super.site/' target='_blank' style='text-decoration: none; color: #4B8BBE;'>Money Matters Studio</a> "
    "for updates, resources, or feature requests."
    "</div>",
    unsafe_allow_html=True
)