import streamlit as st
import pandas as pd
import plotly.express as px

def render_budget_analysis():
    # --- Retrieve Session Data ---
    monthly_expenses = st.session_state.get("expense_template", {})
    annual_income = st.session_state.get("annual_income", 0)
    annual_savings = st.session_state.get("annual_savings", 0)

    # --- Define Category Groups ---
    ESSENTIALS = ["Housing", "Utilities", "Food", "Transportation", "Insurance", "Phone/Internet", "Childcare", "Health & Wellness"]
    LIFE_SERVICES = ["Subscriptions", "Discretionary", "Shopping", "Personal Care"]
    LIFESTYLE = ["Travel", "Other"]
    GOALS_GIVING = ["Investments", "Giving", "Education"]

    def sum_group(group):
        return sum(monthly_expenses.get(cat, 0) for cat in group)

    # --- Calculate Totals ---
    monthly_essentials = sum_group(ESSENTIALS)
    monthly_services = sum_group(LIFE_SERVICES)
    monthly_lifestyle = sum_group(LIFESTYLE)
    monthly_goals = sum_group(GOALS_GIVING)
    monthly_total = sum(monthly_expenses.values())
    annual_total = monthly_total * 12
    delta = annual_income - annual_total
    savings_rate = round((annual_savings / annual_income) * 100, 1) if annual_income else 0
    buffer = delta - annual_savings

    # --- FIRE Impact First ---
    st.markdown("### 🔥 FIRE Impact Summary")

    if delta >= annual_savings:
        st.success("✅ Your lifestyle supports your FIRE plan.")
    else:
        st.error("⚠️ Your lifestyle may be outpacing your FIRE savings target.")

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Income", f"${annual_income:,.0f}")
    col2.metric("🧾 Spending", f"${annual_total:,.0f}")
    col3.metric("📈 Target Savings", f"${annual_savings:,.0f}")

    if delta >= annual_savings:
        st.markdown(f"""
        **📝 Summary:** You're saving \\${annual_savings:,.0f} annually ({savings_rate}%),  
        with a buffer of \\${buffer:,.0f} beyond your FIRE target.  
        Your current spending leaves room for flexibility and continued progress.
        """)
    else:
        shortfall = annual_savings - delta
        st.markdown(f"""
        **📝 Summary:** Your current spending of \\${annual_total:,.0f} exceeds your income by \\${-delta:,.0f},  
        leaving a shortfall of \\${shortfall:,.0f} below your FIRE savings target.  
        Consider adjusting high-impact categories or revisiting your savings goals.
        """)

    st.markdown("---")

    # --- Budget Breakdown ---
    st.markdown("### 🧾 Your Budget Overview")

    st.markdown(f"""
    | 🏷️ Category Group | 💸 Monthly Amount | 📅 Annual Amount |
    |-------------------|-------------------|------------------|
    | **🏠 Essentials** | ${monthly_essentials:,.0f} | ${monthly_essentials * 12:,.0f} |
    | **💬 Life & Services** | ${monthly_services:,.0f} | ${monthly_services * 12:,.0f} |
    | **🎉 Lifestyle** | ${monthly_lifestyle:,.0f} | ${monthly_lifestyle * 12:,.0f} |
    | **🎯 Goals & Giving** | ${monthly_goals:,.0f} | ${monthly_goals * 12:,.0f} |
    | <strong>📊 Total Expense</strong> | <strong>${monthly_total:,.0f}</strong> | <strong>${annual_total:,.0f}</strong> |
    """, unsafe_allow_html=True)

    # --- Bar Chart ---
    data = pd.DataFrame({
        "Category": ["🏠 Essentials", "💬 Life & Services", "🎉 Lifestyle", "🎯 Goals & Giving"],
        "Monthly Expense": [monthly_essentials, monthly_services, monthly_lifestyle, monthly_goals]
    })

    fig = px.bar(
        data,
        x="Monthly Expense",
        y="Category",
        orientation="h",
        text="Monthly Expense",
        color="Category",
        color_discrete_sequence=["#FF6B6B", "#4ECDC4", "#FFD93D", "#6A4C93"]
    )

    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="auto", insidetextanchor="start")
    fig.update_layout(
        title={"text": "Monthly Expense Breakdown", "x": 0.0, "xanchor": "left", "font": dict(size=20)},
        xaxis=dict(title="Amount ($)", showgrid=True, gridcolor="lightgrey", zeroline=False),
        yaxis=dict(title="", tickfont=dict(weight="bold"), showgrid=False),
        showlegend=False,
        height=420,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- Optional Sync ---
    if st.button("👉 >> 🔄 Sync Spending ($) >>"):
        st.session_state["fire_expenses"] = annual_total
        st.success(f"✅ Synced! ${annual_total:,.0f} now powers your FIRE Tracker and other planning tools.")

