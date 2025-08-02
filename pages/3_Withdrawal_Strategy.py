import streamlit as st
from navigation import studio_nav
import datetime
this_year = datetime.datetime.now().year  # Needed for some default fields
from session_defaults import DEFAULTS
from utils_session import initialize_state_once
initialize_state_once(DEFAULTS)  # ✅ now has the required argument

def clear_session_state():
    for key in st.session_state.keys():
        del st.session_state[key]

st.set_page_config(page_title="Withdrawal Designer", page_icon="📤")

studio_nav()

st.markdown("## 🛠️ Coming Soon to Money Matters Studio")
st.success(
    "This page is part of an upcoming feature designed to help you plan with even more clarity and confidence. Stay tuned!",
    icon="📈"
)
