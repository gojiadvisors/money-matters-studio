import streamlit as st

def inject_tab_style():
    st.markdown("""
        <style>
        button[aria-selected="true"] {
            background-color: #ffe082 !important;
            color: #333 !important;
            border-bottom: 3px solid #ffb300 !important;
            border-radius: 6px 6px 0 0 !important;
            font-weight: 600 !important;
            padding: 12px 20px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        button[aria-selected="false"] {
            background-color: #fff8e1 !important;
            color: #333 !important;
            border-radius: 6px 6px 0 0 !important;
            font-weight: 500 !important;
            padding: 12px 20px !important;
        }

        button[aria-selected]:hover {
            background-color: #ffecb3 !important;
        }
        </style>
    """, unsafe_allow_html=True)

def inject_button_style():
    st.markdown("""
        <style>
        div[data-testid="stButton"] button {
            padding: 2px 6px;
            font-size: 0.75rem;
            background-color: #f9f9f9;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-shadow: none;
        }
        div[data-testid="stButton"] button:hover {
            background-color: #e0e0e0;
        }
        </style>
    """, unsafe_allow_html=True)
