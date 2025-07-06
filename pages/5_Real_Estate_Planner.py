# pages/5_Real_Estate_Planner.py

import streamlit as st

st.set_page_config(page_title="🏘️ Real Estate Planner", page_icon="🏡")
st.title("🏘️ Real Estate Planner")
st.caption("Model rental income, equity, and appreciation to accelerate your FIRE plan.")

st.markdown("## 🧾 Property Profile")

col1, col2 = st.columns(2)

with col1:
    address = st.text_input("Property name or address", "Duplex on 5th Ave")
    purchase_price = st.number_input("Purchase price ($)", min_value=0, step=1000)
    down_payment_pct = st.slider("Down payment (%)", 0, 100, 20)

with col2:
    annual_rent = st.number_input("Annual rental income ($)", min_value=0, step=1000)
    annual_expenses = st.number_input("Annual operating expenses ($)", min_value=0, step=100)
    appreciation_rate = st.slider("Annual appreciation (%)", 0.0, 10.0, 3.0)

st.markdown("## 🧮 Financing and Horizon")

col3, col4 = st.columns(2)

with col3:
    interest_rate = st.slider("Loan interest rate (%)", 0.0, 10.0, 4.0)
    loan_term = st.slider("Loan term (years)", 1, 40, 30)

with col4:
    years_held = st.slider("Years to hold property", 1, 40, 15)
    sell_price_override = st.number_input("Optional resale price override ($)", value=0)

# 🚧 Placeholder until calculations added
if st.button("Run Property Model"):
    st.info("📊 Calculation module coming next: cash flow, equity growth, and appreciation over time.")
