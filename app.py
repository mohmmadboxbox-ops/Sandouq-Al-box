import streamlit as st

st.set_page_config(page_title="العبقري 2", layout="wide")

# CSS يمنع نزول الأرقام تحت بعضها أبداً
st.markdown("""
    <style>
    .flex-container {
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 5px !important;
    }
    .num-btn {
        width: 32px !important;
        height: 32px !important;
        font-size: 12px !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# إدارة الأرقام المختارة
if 'sel' not in st.session_state: st.session_state.sel = []

def toggle(n):
    if n in st.session_state.sel: st.session_state.sel.remove(n)
    elif len(st.session_state.sel) < 50: st.session_state.sel.append(n)

# العدّاد في الأعلى
st.subheader(f"العدد المختار: {len(st.session_state.sel)} / 50")

# عرض الأزرار كـ Flexbox
st.markdown('<div class="flex-container">', unsafe_allow_html=True)
for i in range(1, 91):
    # نستخدم زر عادي ونطبق التنسيق عليه
    if st.button(str(i), key=f"b{i}", type="primary" if i in st.session_state.sel else "secondary"):
        toggle(i)
st.markdown('</div>', unsafe_allow_html=True)