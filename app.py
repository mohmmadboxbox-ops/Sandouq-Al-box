import streamlit as st

st.set_page_config(page_title="العبقري 2", layout="wide")

st.title("العبقري 2: لوحة الإدخال")

# قائمة الأرقام من 1 إلى 90
all_numbers = list(range(1, 91))

# القائمة الذكية للإدخال (مضمونة 100% على الموبايل)
selected_numbers = st.multiselect(
    "اضغط هنا لاختيار الأرقام (يمكنك كتابة الرقم للبحث السريع):",
    options=all_numbers,
    max_selections=50,
    placeholder="اختر الأرقام..."
)

# العداد المدمج
count = len(selected_numbers)
if count == 50:
    st.success(f"✅ اكتمل العدد: {count} / 50")
else:
    st.info(f"📊 الأرقام المحددة: {count} / 50")

st.write("الأرقام التي اخترتها:", sorted(selected_numbers))