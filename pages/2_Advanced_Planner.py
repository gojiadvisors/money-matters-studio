import streamlit as st
from navigation import studio_nav
from sidebar import render_global_assumptions
render_global_assumptions()
from ui_helpers import show_sidebar_hint

# Init sidebar hint
if "show_sidebar_hint" not in st.session_state:
    st.session_state["show_sidebar_hint"] = True

show_sidebar_hint()

st.set_page_config(page_title="Advanced Planner", page_icon="🧠")

studio_nav()

st.markdown("## 🛠️ Coming Soon to Money Matters Studio")
st.success(
    "This page is part of an upcoming feature designed to help you plan with even more clarity and confidence. Stay tuned!",
    icon="📈"
)
