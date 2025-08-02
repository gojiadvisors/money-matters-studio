import streamlit as st
from navigation import studio_nav
from utils_session import initialize_state
import datetime

this_year = datetime.datetime.now().year  # Needed for some default fields



st.set_page_config(page_title="Advanced Planner", page_icon="🧠")

studio_nav()

st.markdown("## 🛠️ Coming Soon to Money Matters Studio")
st.success(
    "This page is part of an upcoming feature designed to help you plan with even more clarity and confidence. Stay tuned!",
    icon="📈"
)