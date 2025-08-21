import streamlit as st
from navigation import studio_nav
from session_defaults import init_session_state  # ✅ Use centralized initializer

# --- Initialize Session State Once ---
init_session_state()

# --- Inject Custom CSS ---
def inject_custom_css():
    st.markdown("""
        <style>
        * {
            border-radius: 0 !important;
        }
        
        div.block-container {
            padding-top: 3rem !important;
            padding-bottom: 6rem !important;
        }

        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# --- Page Config ---
st.set_page_config(page_title="Money Matters Studio", page_icon="💰")

# --- Navigation ---
selected_page = studio_nav()
selected_page.run()
