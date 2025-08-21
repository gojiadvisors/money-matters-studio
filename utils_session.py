import streamlit as st
from session_defaults import DEFAULTS

def initialize_state_once(defaults: dict):
    if not st.session_state.get("initialized_once", False):
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
        st.session_state["initialized_once"] = True

def clear_session_state():
    for key in DEFAULTS:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state["initialized_once"] = False
