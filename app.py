import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="لوحة إدخال السحوبات - العبقري 2", layout="wide")

# تصميم لوني بسيط باستخدام CSS مدمج
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("لوحة إدخال السحوبات اليدوية")

# تهيئة المتغيرات في ذاكرة الجلسة (Session State)
if 'current_selection' not in st.session_state:
    st.session_state.current_selection = []
if 'saved_draws' not in st.session_state:
    st.session_state.saved_draws = []

# دالة للتعامل مع الضغط على الأرقام
def toggle_number(num):
    if num in st.session_state.current_selection:
        st.session_state.current_selection.remove(num)
    else:
        if len(st.session_state.current_selection) < 50:
            st.session_state.current_selection.append(num)
    
    # إذا اكتمل العدد 50، يتم الحفظ التلقائي والتصفير
    if len(st.session_state.current_selection) == 50:
        sorted_draw = sorted(st.session_state.current_selection)
        st.session_state.saved_draws.append(sorted_draw)
        st.session_state.current_selection = []

# عرض العداد
count = len(st.session_state.current_selection)
if count == 50:
    st.success(f"الأرقام المحددة: {count} / 50 (تم الحفظ!)")
else:
    st.warning(f"الأرقام المحددة: {count} / 50")

st.write("---")

# إنشاء لوحة الأرقام (9 صفوف × 10 أعمدة)
for row in range(9):
    cols = st.columns(10)
    for col_idx in range(10):
        num = row * 10 + col_idx + 1
        
        # تغيير النص ليوضح أن الرقم محدد
        is_selected = num in st.session_state.current_selection
        label = f"✅ {num}" if is_selected else str(num)
        
        with cols[col_idx]:
            st.button(label, key=f"btn_{num}", on_click=toggle_number, args=(num,))

st.write("---")

# عرض السحوبات المحفوظة لتسهيل نسخها ومراجعتها
if st.session_state.saved_draws:
    st.header("السحوبات المحفوظة:")
    for i, draw in enumerate(st.session_state.saved_draws):
        st.info(f"**السحب رقم {i+1}:** {draw}")