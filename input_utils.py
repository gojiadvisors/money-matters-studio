import streamlit as st

def synced_number_input(label, session_key, default, **kwargs):
    # Initialize session value if missing
    if session_key not in st.session_state:
        st.session_state[session_key] = default

    # Use a widget-specific key to avoid collisions
    widget_key = f"{session_key}_input"

    # Render input
    value = st.number_input(label, value=st.session_state[session_key], key=widget_key, **kwargs)

    # Update session state only if changed
    if value != st.session_state[session_key]:
        st.session_state[session_key] = value

    return value
