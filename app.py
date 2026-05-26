import streamlit as st
import random

st.set_page_config(page_title="العبقري 2 - حل العرض", layout="wide")

st.title("العبقري 2: الدقة المطلقة")

if 'sel' not in st.session_state: st.session_state.sel = []
if 'draws' not in st.session_state: st.session_state.draws = []

def toggle(n):
    if n in st.session_state.sel: st.session_state.sel.remove(n)
    elif len(st.session_state.sel) < 50: st.session_state.sel.append(n)

# إجبار الأزرار على البقاء في صفوف
cols_per_row = 10
for i in range(0, 90, cols_per_row):
    row_cols = st.columns(cols_per_row)
    for j in range(cols_per_row):
        num = i + j + 1
        with row_cols[j]:
            if st.button(str(num), key=f"b{num}", type="primary" if num in st.session_state.sel else "secondary"):
                toggle(num)