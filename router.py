import streamlit as st
from navigation import studio_nav

st.set_page_config(page_title="Money Matters Studio", page_icon="💰")

selected_page = studio_nav()
selected_page.run()
