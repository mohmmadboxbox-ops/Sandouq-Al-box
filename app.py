import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="لوحة إدخال السحوبات - العبقري 2", layout="wide")

# عزل التصميم وتخصيصه للوحة الأرقام فقط
st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(10, 1fr) !important;
        gap: 6px !important;
        width: 100% !important;
        margin-bottom: 6px !important;
        direction: ltr !important;
    }
    div[data-testid="column"] {
        width: 100% !important;
        padding: 0 !important;
        min-width: 0 !important;
        display: flex;
        justify-content: center;
    }
    div[data-testid="stHorizontalBlock"] .stButton>button {
        width: 38px !important;
        height: 38px !important;
        border-radius: 50% !important;
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
    div[data-testid="stHorizontalBlock"] .stButton>button p {
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }
    div[data-testid="stHorizontalBlock"] button[kind="primary"] {
        background-color: #28a745 !important; 
        border-color: #1e7e34 !important;
        color: white !important;
        transform: scale(1.1);
    }
    /* تصميم خاص لنتائج الفلترة */
    .result-box {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-right: 5px solid #1a73e8;
        margin-bottom: 10px;
    }
    .rejected-box {
        border-right-color: #dc3545;
    }
    .accepted-box {
        border-right-color: #28a745;
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

def save_and_clear():
    sorted_draw = sorted(st.session_state.current_selection)
    st.session_state.saved_draws.append(sorted_draw)
    st.session_state.current_selection = []

count = len(st.session_state.current_selection)

# العداد وزر الحفظ
if count == 50:
    st.success(f"الأرقام المحددة: {count} / 50 (يرجى مراجعة اللوحة ثم التأكيد)")
    st.button("💾 تأكيد حفظ السحب ومسح اللوحة للبدء من جديد", on_click=save_and_clear, use_container_width=True)
else:
    st.warning(f"الأرقام المحددة: {count} / 50")

st.write("---")

# إنشاء لوحة الأرقام الدائرية
for row in range(9):
    cols = st.columns(10)
    for col_idx in range(10):
        num = row * 10 + col_idx + 1
        
        is_selected = num in st.session_state.current_selection
        btn_type = "primary" if is_selected else "secondary"
        
        with cols[col_idx]:
            st.button(str(num), key=f"btn_{num}", on_click=toggle_number, args=(num,), type=btn_type)

st.write("---")

# عرض السحوبات
if st.session_state.saved_draws:
    st.header("السحوبات المحفوظة:")
    for i, draw in enumerate(st.session_state.saved_draws):
        st.info(f"**السحب {i+1}:** {draw}")
        
    st.write("---")

# ==========================================
# خوارزمية الفلترة (العبقري 2) - تعمل فقط عند وجود سحبتين
# ==========================================
if len(st.session_state.saved_draws) >= 2:
    st.header("🧠 خوارزمية تصفية العبقري 2")
    
    if st.button("🚀 تشغيل فلتر العبقري 2 على آخر سحبتين", type="primary", use_container_width=True):
        
        # 1. سحب البيانات (السحبة الأولى والثانية)
        draw1 = set(st.session_state.saved_draws[0])
        draw2 = set(st.session_state.saved_draws[1])
        all_numbers = set(range(1, 91))
        
        # 2. استخراج المجموعات الرئيسية
        common_numbers = draw1.intersection(draw2)
        net_draw1 = draw1 - common_numbers
        net_draw2 = draw2 - common_numbers
        absent_numbers = all_numbers - (draw1 | draw2)
        
        # 3. توزيع المشترك على 9 صناديق
        boxes = {i: [] for i in range(1, 10)}
        for num in common_numbers:
            box_id = ((num - 1) // 10) + 1
            boxes[box_id].append(num)
            
        # 4. فرز الصناديق حسب عدد الأرقام بداخلها (تنازلياً)
        # إذا تعادلت الصناديق، سيتم ترتيبها بناءً على رقم الصندوق لضمان الاستقرار
        sorted_boxes = sorted(boxes.items(), key=lambda x: len(x[1]), reverse=True)
        
        top_5_boxes = sorted_boxes[:5]
        bottom_4_boxes = sorted_boxes[5:]
        
        # استخراج أرقام الصناديق المتأهلة والمستبعدة
        active_common = set([num for box_id, nums in top_5_boxes for num in nums])
        rejected_common = set([num for box_id, nums in bottom_4_boxes for num in nums])
        
        # 5. تشكيل الأوعية النهائية
        active_pool = active_common | net_draw2 | absent_numbers
        rejected_pool = rejected_common | net_draw1
        
        # ====================
        # عرض النتائج بشكل احترافي
        # ====================
        
        st.subheader("📊 تفكيك البيانات الأولي:")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("المشترك", len(common_numbers))
        col2.metric("صافي السحبة 2", len(net_draw2))
        col3.metric("صافي السحبة 1", len(net_draw1))
        col4.metric("الغائب", len(absent_numbers))
        
        st.write("---")
        
        st.subheader("📦 تحليل صناديق الأرقام المشتركة:")
        t_col1, t_col2 = st.columns(2)
        
        with t_col1:
            st.markdown("<div class='result-box accepted-box'><b>✅ أعلى 5 صناديق (متأهلة):</b><br>", unsafe_allow_html=True)
            for box_id, nums in top_5_boxes:
                st.write(f"- صندوق {box_id}: {sorted(nums)} (العدد: {len(nums)})")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with t_col2:
            st.markdown("<div class='result-box rejected-box'><b>❌ أقل 4 صناديق (مستبعدة):</b><br>", unsafe_allow_html=True)
            for box_id, nums in bottom_4_boxes:
                st.write(f"- صندوق {box_id}: {sorted(nums)} (العدد: {len(nums)})")
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("---")
        
        st.subheader("🎯 النتيجة النهائية للفرز:")
        
        st.markdown(f"<div class='result-box accepted-box'><h4>🟢 الوعاء النشط المقبول (المجموع: {len(active_pool)} رقم)</h4>"
                    f"يشمل: (أرقام الـ 5 صناديق) + (الغائب) + (صافي السحبة 2)<br><br>"
                    f"<b>الأرقام:</b> {sorted(list(active_pool))}</div>", unsafe_allow_html=True)
                    
        st.markdown(f"<div class='result-box rejected-box'><h4>🔴 الوعاء المستبعد النهائي (المجموع: {len(rejected_pool)} رقم)</h4>"
                    f"يشمل: (أرقام الـ 4 صناديق) + (صافي السحبة 1)<br><br>"
                    f"<b>الأرقام:</b> {sorted(list(rejected_pool))}</div>", unsafe_allow_html=True)
                    
        st.success("تم تنفيذ الفلترة بنجاح وبدقة 100% حسب خوارزمية العبقري 2.")