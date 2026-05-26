import streamlit as st
import random

st.set_page_config(page_title="العبقري 2", layout="wide")

# CSS "الحديد": يمنع الأرقام من أن تترتب عمودياً ويجبرها على الشبكة
st.markdown("""
    <style>
    .grid-container {
        display: grid !important;
        grid-template-columns: repeat(10, 1fr) !important;
        gap: 2px !important;
        width: 100% !important;
    }
    .grid-container button {
        width: 100% !important;
        border-radius: 50% !important;
        aspect-ratio: 1 / 1 !important;
        font-weight: bold !important;
        padding: 0 !important;
        font-size: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("العبقري 2: الدقة المطلقة")

if 'sel' not in st.session_state: st.session_state.sel = []
if 'draws' not in st.session_state: st.session_state.draws = []

def toggle(n):
    if n in st.session_state.sel: st.session_state.sel.remove(n)
    elif len(st.session_state.sel) < 50: st.session_state.sel.append(n)

if st.button("حفظ السحب"):
    if len(st.session_state.sel) > 0:
        st.session_state.draws.append(sorted(st.session_state.sel))
        st.session_state.sel = []

# عرض الشبكة بإجبار الـ CSS
st.markdown('<div class="grid-container">', unsafe_allow_html=True)
for i in range(1, 91):
    if st.button(str(i), key=f"b{i}", type="primary" if i in st.session_state.sel else "secondary"):
        toggle(i)
st.markdown('</div>', unsafe_allow_html=True)

if len(st.session_state.draws) >= 2:
    if st.button("🚀 توليد نهائي"):
        d1, d2 = set(st.session_state.draws[-2]), set(st.session_state.draws[-1])
        pool = sorted(list((d1 & d2) | (d2 - d1) | (set(range(1, 91)) - (d1 | d2))))
        
        # دالة حماية من التكرار
        def finalize(c, p):
            c_set = set(c)
            while len(c_set) < 5:
                options = [n for n in p if n not in c_set]
                if not options: break
                c_set.add(random.choice(options))
            return sorted(list(c_set)[:5])

        low, high = [n for n in pool if n<=45], [n for n in pool if n>45]
        
        # التوليد
        results = {
            'تيبيت': finalize(sorted(pool)[:3] + sorted(pool, reverse=True)[:2], pool),
            'جرانفيل': finalize(random.sample(low, min(len(low), 3)) + random.sample(high, min(len(high), 2)), pool),
            'متجاورة': finalize([n for n in pool if n+1 in pool][:2] + [n+1 for n in pool if n+1 in pool][:2], pool),
            'انحياز': finalize(random.sample(low if random.random()>0.5 else high, min(len(low if random.random()>0.5 else high), 5)), pool),
            'قنص': finalize([n for n in pool if 40<=n<=50][:3] + [n for n in pool if 20<=n<=30][:2], pool),
            'عمودي': finalize([n for n in pool if n%10 == 1], pool)
        }

        for name, nums in results.items():
            st.write(f"**{name}:** {' - '.join(map(str, nums))}")