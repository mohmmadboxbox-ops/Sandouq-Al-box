import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="العبقري 2", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "templates", "index.html")

try:
    with open(file_path, "r", encoding="utf-8") as f:
        html_code = f.read()
    components.html(html_code, height=1300, scrolling=True)
except Exception as e:
    st.error(f"🚨 خطأ: لم أتمكن من العثور على الملف. المسار الذي بحثت فيه هو: {file_path}")