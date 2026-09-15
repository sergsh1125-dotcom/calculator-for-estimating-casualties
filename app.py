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
        padding: 16px;
        border-radius: 4px;
        margin-top: 15px;
    }
    
    .results-card h4 {
        color: #FFD700;
        margin-top: 10px;
        margin-bottom: 8px;
        font-size: 15px;
        text-transform: uppercase;
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

    # 1. Травми
    s_tr_s = calc_area(data["trauma"]["severe"])
    s_tr_m = calc_area(data["trauma"]["moderate"], data["trauma"]["severe"])
    s_tr_l = calc_area(data["trauma"]["light"], data["trauma"]["moderate"])

    # 2. Опіки
    s_b_3 = calc_area(data["burns"]["degree_3"])
    s_b_2 = calc_area(data["burns"]["degree_2"], data["burns"]["degree_3"])
    s_b_1 = calc_area(data["burns"]["degree_1"], data["burns"]["degree_2"])

    # 3. ГПХ
    s_r_4 = calc_area(data["radiation"]["degree_4"])
    s_r_3 = calc_area(data["radiation"]["degree_3"], data["radiation"]["degree_4"])
    s_r_2 = calc_area(data["radiation"]["degree_2"], data["radiation"]["degree_3"])
    s_r_1 = calc_area(data["radiation"]["degree_1"], data["radiation"]["degree_2"])

    st.markdown(f"""
    <div class="results-card">
        <h4>1. Травми (Ударна хвиля):</h4>
        • Важкий ступінь: <span class="val-highlight">{int(s_tr_s * density_ppl):,} осіб</span> (S = {s_tr_s:.2f} км²)<br>
        • Середній ступінь: <span class="val-highlight">{int(s_tr_m * density_ppl):,} осіб</span> (S = {s_tr_m:.2f} км²)<br>
        • Легкий ступінь: <span class="val-highlight">{int(s_tr_l * density_ppl):,} осіб</span> (S = {s_tr_l:.2f} км²)
        
        <h4>2. Термічні опіки (Світлове випромінювання):</h4>
        • III ступінь: <span class="val-highlight">{int(s_b_3 * density_ppl):,} осіб</span> (S = {s_b_3:.2f} км²)<br>
        • II ступінь: <span class="val-highlight">{int(s_b_2 * density_ppl):,} осіб</span> (S = {s_b_2:.2f} км²)<br>
        • I ступінь: <span class="val-highlight">{int(s_b_1 * density_ppl):,} осіб</span> (S = {s_b_1:.2f} км²)
        
        <h4>3. Гостра променева хвороба (Проникаюча радіація):</h4>
        • IV ступінь: <span class="val-highlight">{int(s_r_4 * density_ppl):,} осіб</span> (S = {s_r_4:.2f} км²)<br>
        • III ступінь: <span class="val-highlight">{int(s_r_3 * density_ppl):,} осіб</span> (S = {s_r_3:.2f} км²)<br>
        • II ступінь: <span class="val-highlight">{int(s_r_2 * density_ppl):,} осіб</span> (S = {s_r_2:.2f} км²)<br>
        • I ступінь: <span class="val-highlight">{int(s_r_1 * density_ppl):,} осіб</span> (S = {s_r_1:.2f} км²)
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
