import streamlit as st

st.set_page_config(layout="wide")

# هذا CSS هو "قانون" التنسيق
st.markdown("""
    <style>
    .fix-grid {
        display: grid !important;
        grid-template-columns: repeat(10, 1fr) !important;
        gap: 2px !important;
        width: 100% !important;
        max-width: 400px !important; /* حجم ثابت للموبايل */
        margin: auto !important;
    }
    .num-box {
        background: #eee;
        text-align: center;
        padding: 5px 0;
        border: 1px solid #ccc;
        cursor: pointer;
        font-size: 12px;
    }
    .selected { background: #28a745 !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# إدارة الحالة
if 'sel' not in st.session_state: st.session_state.sel = []

st.subheader(f"العدد المختار: {len(st.session_state.sel)} / 50")

# إنشاء الأزرار بطريقة يدوية لضمان التنسيق
st.markdown('<div class="fix-grid">', unsafe_allow_html=True)
for i in range(1, 91):
    is_sel = i in st.session_state.sel
    # نستخدم زر لضمان التفاعل
    if st.button(str(i), key=f"n{i}", type="primary" if is_sel else "secondary"):
        if is_sel: st.session_state.sel.remove(i)
        elif len(st.session_state.sel) < 50: st.session_state.sel.append(i)
        st.rerun() # تحديث الصفحة فوراً
st.markdown('</div>', unsafe_allow_html=True)