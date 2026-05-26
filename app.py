import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="العبقري 2", layout="wide")

# هذا الكود يجبر Streamlit بقوة على إبقاء الـ 10 أعمدة متجاورة في الموبايل
st.markdown("""
    <style>
    @media (max-width: 1000px) {
        div[data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 2px !important;
        }
        div[data-testid="column"] {
            width: 10% !important;
            flex: 1 1 10% !important;
            min-width: 10% !important;
            padding: 1px !important;
        }
    }
    
    /* تصميم الأزرار الدائرية الصغيرة لتناسب الموبايل */
    .stButton > button {
        width: 100% !important;
        padding: 0 !important;
        aspect-ratio: 1 / 1 !important;
        border-radius: 50% !important;
        font-size: 13px !important;
        font-weight: bold !important;
        min-height: 25px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("لوحة إدخال - العبقري 2")

# تهيئة الذاكرة
if 'sel' not in st.session_state:
    st.session_state.sel = []

# دالة التحديد (بدون الحاجة لعمل Refresh يدوي)
def toggle(n):
    if n in st.session_state.sel:
        st.session_state.sel.remove(n)
    elif len(st.session_state.sel) < 50:
        st.session_state.sel.append(n)

# العداد (تم إصلاحه وإبرازه في صندوق واضح)
count = len(st.session_state.sel)
if count == 50:
    st.success(f"✅ اكتمل العدد: {count} / 50")
else:
    st.info(f"📊 الأرقام المحددة: {count} / 50")

st.write("---")

# بناء اللوحة بالأعمدة الرسمية مع إجبارها على عدم الكسر
for row in range(9):
    cols = st.columns(10)
    for col_idx in range(10):
        num = row * 10 + col_idx + 1
        is_selected = num in st.session_state.sel
        
        with cols[col_idx]:
            # استخدام on_click يحل مشكلة العداد ويجعل الاستجابة فورية
            st.button(
                str(num), 
                key=f"btn{num}", 
                on_click=toggle, 
                args=(num,), 
                type="primary" if is_selected else "secondary"
            )