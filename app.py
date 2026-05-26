import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="لوحة إدخال السحوبات - العبقري 2", layout="wide")

# التصميم اللوني الجديد لإجبار اللوحة على شكل شبكة (Grid) متناسقة
st.markdown("""
    <style>
    /* تحويل الحاوية الأفقية إلى شبكة بـ 10 أعمدة متساوية */
    div[data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(10, 1fr) !important;
        gap: 2px !important;
        width: 100% !important;
    }
    /* إزالة الحواف والفراغات الافتراضية لأعمدة ستريملت */
    div[data-testid="column"] {
        width: 100% !important;
        padding: 0 !important;
        min-width: 0 !important;
    }
    /* تصميم الأزرار لتكون مربعة ومناسبة لشاشة الهاتف */
    .stButton>button {
        width: 100% !important;
        height: 40px !important;
        font-size: 14px !important;
        font-weight: bold !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    /* تقليل الفراغ العلوي للصفحة لتوفير مساحة */
    .block-container {
        padding-top: 2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("لوحة إدخال السحوبات اليدوية")

# تهيئة المتغيرات
if 'current_selection' not in st.session_state:
    st.session_state.current_selection = []
if 'saved_draws' not in st.session_state:
    st.session_state.saved_draws = []

def toggle_number(num):
    if num in st.session_state.current_selection:
        st.session_state.current_selection.remove(num)
    else:
        if len(st.session_state.current_selection) < 50:
            st.session_state.current_selection.append(num)
    
    if len(st.session_state.current_selection) == 50:
        sorted_draw = sorted(st.session_state.current_selection)
        st.session_state.saved_draws.append(sorted_draw)
        st.session_state.current_selection = []

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
        
        is_selected = num in st.session_state.current_selection
        label = f"✅ {num}" if is_selected else str(num)
        
        with cols[col_idx]:
            st.button(label, key=f"btn_{num}", on_click=toggle_number, args=(num,))

st.write("---")

# عرض السحوبات المحفوظة
if st.session_state.saved_draws:
    st.header("السحوبات المحفوظة:")
    for i, draw in enumerate(st.session_state.saved_draws):
        st.info(f"**السحب رقم {i+1}:** {draw}")