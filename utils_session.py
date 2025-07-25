import streamlit as st

def initialize_state(defaults: dict):
    """
    Initializes Streamlit session state variables with defaults if not already set.

    Args:
        defaults (dict): A dictionary where keys are variable names and values are default values.
    """
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        for key, value in defaults.items():
            st.session_state[key] = st.session_state.get(key, value)
