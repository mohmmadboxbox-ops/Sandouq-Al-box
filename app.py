import streamlit as st
import random

st.set_page_config(page_title="العبقري 2 - التدقيق الجذري", layout="wide")

st.markdown("""
    <style>
    .number-grid { display: grid; grid-template-columns: repeat(10, 1fr); gap: 4px; margin-bottom: 20px; }
    .number-grid button { width: 100%; border-radius: 50%; aspect-ratio: 1; font-weight: bold; border: 1px solid #ccc; font-size: 14px; }
    button[kind="primary"] { background-color: #28a745 !important; color: white !important; }
    .card-box { background: #ffffff; border: 2px solid #28a745; padding: 12px; border-radius: 8px; margin-bottom: 10px; text-align: center; }
    .card-title { font-size: 13px; color: #444; font-weight: bold; margin-bottom: 5px; }
    .card-numbers { font-size: 20px; font-weight: bold; color: #1a73e8; letter-spacing: 3px; direction: ltr; }
    </style>
""", unsafe_allow_html=True)

st.title("العبقري 2: الدقة المطلقة (نسخة التدقيق الجذري)")

if 'sel' not in st.session_state: st.session_state.sel = []
if 'draws' not in st.session_state: st.session_state.draws = []

def toggle(n):
    if n in st.session_state.sel: st.session_state.sel.remove(n)
    elif len(st.session_state.sel) < 50: st.session_state.sel.append(n)

if st.button("حفظ السحب"):
    if len(st.session_state.sel) > 0:
        st.session_state.draws.append(sorted(st.session_state.sel))
        st.session_state.sel = []

st.markdown('<div class="number-grid">', unsafe_allow_html=True)
for i in range(1, 91):
    if st.button(str(i), key=f"b{i}", type="primary" if i in st.session_state.sel else "secondary"): toggle(i)
st.markdown('</div>', unsafe_allow_html=True)

if len(st.session_state.draws) >= 2:
    if st.button("🚀 توليد نهائي ودقيق"):
        d1, d2 = set(st.session_state.draws[-2]), set(st.session_state.draws[-1])
        pool = sorted(list((d1 & d2) | (d2 - d1) | (set(range(1, 91)) - (d1 | d2))))
        
        def finalize(c, p):
            c_set = set(c)
            attempts = 0
            while len(c_set) < 5 and attempts < 100:
                n = random.choice(p)
                c_set.add(n)
                attempts += 1
            return sorted(list(c_set)[:5])

        low, high = [n for n in pool if n<=45], [n for n in pool if n>45]
        
        # خوارزمية الأعمدة المحسنة
        cols_map = {i: [n for n in pool if n % 10 == i] for i in range(10)}
        best_col = max(cols_map.values(), key=len)
        
        results = {
            'تيبيت': finalize(sorted(pool)[:3] + sorted(pool, reverse=True)[:2], pool),
            'جرانفيل': finalize(random.sample(low, min(len(low), 3)) + random.sample(high, min(len(high), 2)), pool),
            'متجاورة': finalize([n for n in pool if n+1 in pool][:2] + [n+1 for n in pool if n+1 in pool][:2], pool),
            'انحياز': finalize(random.sample(low if random.random() > 0.5 else high, min(len(low if random.random() > 0.5 else high), 5)), pool),
            'قنص': finalize([n for n in pool if 40<=n<=50][:3] + [n for n in pool if 20<=n<=30][:2], pool),
            'عمودي': finalize(best_col, pool)
        }

        for name, nums in results.items():
            st.markdown(f"<div class='card-box'><div class='card-title'>{name}</div><div class='card-numbers'>{' - '.join(map(str, nums))}</div></div>", unsafe_allow_html=True)