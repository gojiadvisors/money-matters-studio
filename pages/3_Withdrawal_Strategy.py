import streamlit as st
from navigation import studio_nav
from sidebar import render_global_assumptions
render_global_assumptions()


st.set_page_config(page_title="Withdrawal Designer", page_icon="📤")
studio_nav()