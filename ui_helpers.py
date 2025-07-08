# ui_helpers.py

import streamlit as st
from streamlit_javascript import st_javascript

def show_sidebar_hint():
    """Show sidebar hint only on small (mobile) screen widths."""
    screen_width = st_javascript("window.innerWidth")

    if screen_width and screen_width < 700:  # Tailwind's mobile breakpoint
        if st.session_state.get("show_sidebar_hint", True):
            st.info(
                "💡 Your global planning inputs (FIRE spending, inflation, withdrawal rate) live in the sidebar. Tap the >> icon at the top-left to access them.",
                #icon="💼"
            )
            if st.button("✅ Got it"):
                st.session_state["show_sidebar_hint"] = False
