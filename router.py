import streamlit as st
from navigation import studio_nav
from session_defaults import DEFAULTS
from utils_session import initialize_state_once

initialize_state_once(DEFAULTS)


st.set_page_config(page_title="Money Matters Studio", page_icon="💰")

selected_page = studio_nav()
selected_page.run()
