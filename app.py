import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="لوحة إدخال السحوبات - العبقري 2", layout="wide")

# التصميم اللوني لعمل أزرار دائرية خضراء عند التحديد ومنع انقسام الأرقام
st.markdown("""
    <style>
    /* إجبار الشبكة لتكون 10 أعمدة متناسقة المسافات */
    div[data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(10, 1fr) !important;
        gap: 6px !important;
        width: 100% !important;
        margin-bottom: 6px !important;
    }
    div[data-testid="column"] {
        width: 100% !important;
        padding: 0 !important;
        min-width: 0 !important;
        display: flex;
        justify-content: center;
    }
    /* تصميم الدائرة للأرقام وتوسيطها */
    .stButton>button {
        width: 36px !important;
        height: 36px !important;
        border-radius: 50% !important; /* تحويل الزر إلى دائرة */
        padding: 0 !important;
        margin: 0 !important;
        font-size: 15px !important;
        font-weight: bold !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 0 !important;
        min-width: 0 !important;
        border: 1px solid #ddd !important;
    }
    /* منع النص من الانقسام عمودياً */
    .stButton>button p {
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }
    /* تحويل الزر المحدد (Primary) إلى اللون الأخضر بالكامل */
    button[kind="primary"] {
        background-color: #28a745 !important; 
        border-color: #1e7e34 !important;
        color: white !important;
        transform: scale(1.1); /* تكبير الدائرة قليلاً عند التحديد لإبرازها */
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

# إنشاء لوحة الأرقام 
for row in range(9):
    cols = st.columns(10)
    for col_idx in range(10):
        num = row * 10 + col_idx + 1
        
        is_selected = num in st.session_state.current_selection
        # إذا كان الرقم محدداً، يأخذ نوع 'primary' الذي صممناه ليكون أخضر
        btn_type = "primary" if is_selected else "secondary"
        
        with cols[col_idx]:
            # نضع الرقم فقط بدون أي علامات صح لمنع تشوه التصميم
            st.button(str(num), key=f"btn_{num}", on_click=toggle_number, args=(num,), type=btn_type)

st.write("---")

# عرض السحوبات المحفوظة
if st.session_state.saved_draws:
    st.header("السحوبات المحفوظة:")
    for i, draw in enumerate(st.session_state.saved_draws):
        st.info(f"**السحب رقم {i+1}:** {draw}")