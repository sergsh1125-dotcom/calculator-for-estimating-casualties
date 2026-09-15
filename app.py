import math
import streamlit as st
from data import RADII_DATA

# Налаштування сторінки
st.set_page_config(
    page_title="Калькулятор ураження ЯВ",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Стилізація CSS під інтерфейс Платформи ХБРЯ
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #ffffff;
    }
    
    .cbrn-container {
        border: 2px solid #FFD700;
        border-radius: 4px;
        padding: 24px;
        background-color: #0b0e14;
        margin-bottom: 20px;
    }
    
    .cbrn-header {
        color: #FFD700;
        text-align: center;
        font-weight: 700;
        font-size: 20px;
        text-transform: uppercase;
        border-bottom: 1.5px solid #FFD700;
        padding-bottom: 10px;
        margin-bottom: 20px;
        letter-spacing: 0.5px;
    }
    
    .val-highlight {
        color: #38bdf8;
        font-weight: bold;
    }
    
    .results-card {
        border: 1px solid #1e293b;
        background-color: #111827;
        padding: 18px;
        border-radius: 4px;
        margin-top: 15px;
        font-size: 15px;
        line-height: 1.6;
    }
    
    .results-main-title {
        color: #FFD700;
        font-weight: bold;
        font-size: 17px;
        text-transform: uppercase;
        margin-bottom: 12px;
        border-bottom: 1px solid #334155;
        padding-bottom: 6px;
    }
    
    .category-title {
        color: #ffffff;
        font-weight: bold;
        margin-top: 12px;
        margin-bottom: 4px;
    }
    
    .indent-1 {
        margin-left: 15px;
    }
    
    .indent-2 {
        margin-left: 30px;
    }
    
    div.stButton > button:first-child {
        width: 100%;
        font-weight: bold;
        text-transform: uppercase;
        height: 45px;
        border-radius: 4px;
        border: none;
    }
    
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
        background-color: #FFD700 !important;
        color: #000000 !important;
    }
    
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
        background-color: #990000 !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

if "calculated" not in st.session_state:
    st.session_state.calculated = False

def calc_area(r_out: float, r_in: float = 0.0) -> float:
    return math.pi * (r_out**2 - r_in**2)

# --- ІНТЕРФЕЙС ---
st.markdown('<div class="cbrn-container">', unsafe_allow_html=True)
st.markdown('<div class="cbrn-header">Калькулятор втрат населення під час ядерного вибуху</div>', unsafe_allow_html=True)

yield_val = st.selectbox(
    "Потужність ядерного вибуху (Кт):",
    options=list(RADII_DATA.keys()),
    index=2
)

density_val = st.number_input(
    "Щільність населення в районі застосування (тис. осіб/кв. км):",
    min_value=0.1,
    max_value=100.0,
    value=3.5,
    step=0.1
)

st.write("")

col1, col2 = st.columns(2)
with col1:
    btn_calc = st.button("РОЗРАХУВАТИ ПОСТРАЖДАЛИХ")
with col2:
    btn_clear = st.button("ОЧИСТИТИ")

if btn_clear:
    st.session_state.calculated = False
    st.rerun()

if btn_calc:
    st.session_state.calculated = True

if st.session_state.calculated:
    data = RADII_DATA[yield_val]
    density_ppl = density_val * 1000

    # 1. Травми (кількість осіб)
    n_tr_sev = int(calc_area(data["trauma"]["severe"]) * density_ppl)
    n_tr_mod = int(calc_area(data["trauma"]["moderate"], data["trauma"]["severe"]) * density_ppl)
    n_tr_lit = int(calc_area(data["trauma"]["light"], data["trauma"]["moderate"]) * density_ppl)
    n_tr_total = n_tr_sev + n_tr_mod + n_tr_lit

    # 2. Опіки (кількість осіб)
    n_b_3 = int(calc_area(data["burns"]["degree_3"]) * density_ppl)
    n_b_2 = int(calc_area(data["burns"]["degree_2"], data["burns"]["degree_3"]) * density_ppl)
    n_b_1 = int(calc_area(data["burns"]["degree_1"], data["burns"]["degree_2"]) * density_ppl)
    n_b_total = n_b_3 + n_b_2 + n_b_1

    # 3. ГПХ (кількість осіб)
    n_r_4 = int(calc_area(data["radiation"]["degree_4"]) * density_ppl)
    n_r_3 = int(calc_area(data["radiation"]["degree_3"], data["radiation"]["degree_4"]) * density_ppl)
    n_r_2 = int(calc_area(data["radiation"]["degree_2"], data["radiation"]["degree_3"]) * density_ppl)
    n_r_1 = int(calc_area(data["radiation"]["degree_1"], data["radiation"]["degree_2"]) * density_ppl)
    n_r_total = n_r_4 + n_r_3 + n_r_2 + n_r_1

    st.markdown(f"""
    <div class="results-card">
        <div class="results-main-title">Розрахункові дані:</div>
        
        <div class="category-title">Кількість постраждалих з механічними та баротравмами:</div>
        <div class="indent-1">• всього: <span class="val-highlight">{n_tr_total:,} осіб</span></div>
        <div class="indent-1">• у тому числі:</div>
        <div class="indent-2">- важкий ступінь: <span class="val-highlight">{n_tr_sev:,} осіб</span></div>
        <div class="indent-2">- середній ступінь: <span class="val-highlight">{n_tr_mod:,} осіб</span></div>
        <div class="indent-2">- легкий ступінь: <span class="val-highlight">{n_tr_lit:,} осіб</span></div>
        
        <div class="category-title">Кількість постраждалих з опіками:</div>
        <div class="indent-1">• всього: <span class="val-highlight">{n_b_total:,} осіб</span></div>
        <div class="indent-1">• у тому числі:</div>
        <div class="indent-2">- ІІІ ступінь: <span class="val-highlight">{n_b_3:,} осіб</span></div>
        <div class="indent-2">- ІІ ступінь: <span class="val-highlight">{n_b_2:,} осіб</span></div>
        <div class="indent-2">- І ступінь: <span class="val-highlight">{n_b_1:,} осіб</span></div>
        
        <div class="category-title">Кількість постраждалих з променевою хворобою:</div>
        <div class="indent-1">• всього: <span class="val-highlight">{n_r_total:,} осіб</span></div>
        <div class="indent-1">• у тому числі:</div>
        <div class="indent-2">- IV ступінь: <span class="val-highlight">{n_r_4:,} осіб</span></div>
        <div class="indent-2">- ІІІ ступінь: <span class="val-highlight">{n_r_3:,} осіб</span></div>
        <div class="indent-2">- ІІ ступінь: <span class="val-highlight">{n_r_2:,} осіб</span></div>
        <div class="indent-2">- І ступінь: <span class="val-highlight">{n_r_1:,} осіб</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
