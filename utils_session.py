import streamlit as st
from session_defaults import DEFAULTS

def initialize_state_once(defaults: dict):
    if "state_initialized" not in st.session_state:
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
        st.session_state["state_initialized"] = True

def clear_session_state():
    for key in DEFAULTS:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state["state_initialized"] = False
