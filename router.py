import streamlit as st
from navigation import studio_nav
from session_defaults import DEFAULTS
from utils_session import initialize_state_once

initialize_state_once(DEFAULTS)

import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        * {
            border-radius: 0 !important;
        }
        
        div.block-container {
            padding-top: 3rem !important;
            padding-bottom: 0rem !important;
        }

        </style>
    """, unsafe_allow_html=True)

inject_custom_css()


st.set_page_config(page_title="Money Matters Studio", page_icon="💰")

selected_page = studio_nav()
selected_page.run()
