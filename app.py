import math
import streamlit as st
import folium
from streamlit_folium import st_folium
from data import RADII_DATA, ZONE_STYLES

# 1. Налаштування сторінки
st.set_page_config(
    page_title="Калькулятор та карта ураження ЯВ",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Стилізація CSS
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #ffffff; }
    .cbrn-header {
        color: #FFD700; text-align: center; font-weight: 700; font-size: 20px;
        text-transform: uppercase; border-bottom: 1.5px solid #FFD700;
        padding-bottom: 10px; margin-bottom: 25px; letter-spacing: 0.5px;
    }
    .results-card {
        border: 1px solid #1e293b; background-color: #0b0e14;
        padding: 20px; border-radius: 4px; margin-top: 20px; line-height: 1.6;
    }
    .res-main-title {
        color: #FFD700; font-weight: 800; font-size: 18px;
        text-transform: uppercase; margin-bottom: 15px;
        border-bottom: 1px solid #334155; padding-bottom: 8px;
    }
    .res-section-title { color: #FFD700; font-weight: 700; font-size: 16px; margin-top: 14px; margin-bottom: 4px; }
    .res-cat-1 { color: #FFD700; font-size: 14px; margin-left: 15px; }
    .res-cat-2 { color: #FFD700; font-size: 14px; margin-left: 30px; }
    .val-white { color: #FFFFFF !important; font-weight: bold; }
    
    div.stButton > button:first-child {
        width: 100%; font-weight: bold; text-transform: uppercase;
        height: 45px; border-radius: 4px; border: none;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
        background-color: #FFD700 !important; color: #000000 !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
        background-color: #990000 !important; color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

if "calculated" not in st.session_state:
    st.session_state.calculated = False

# --- ІНТЕРФЕЙС ---
st.markdown('<div class="cbrn-header">Калькулятор та карта втрат під час ядерного вибуху</div>', unsafe_allow_html=True)

col_lat, col_lon = st.columns(2)
with col_lat:
    lat_val = st.number_input("Широта епіцентру (Lat):", value=50.4501, format="%.4f")
with col_lon:
    lon_val = st.number_input("Довгота епіцентру (Lon):", value=30.5234, format="%.4f")

yield_val = st.selectbox("Потужність ядерного вибуху (Кт):", options=list(RADII_DATA.keys()), index=2)
density_val = st.number_input("Щільність населення в районі застосування (тис. осіб/кв. км):", min_value=0.1, max_value=100.0, value=4.0, step=0.1)

st.write("")
col1, col2 = st.columns(2)
with col1: btn_calc = st.button("РОЗРАХУВАТИ ТА ВІДОБРАЗИТИ")
with col2: btn_clear = st.button("ОЧИСТИТИ")

if btn_clear:
    st.session_state.calculated = False
    st.rerun()

if btn_calc:
    st.session_state.calculated = True

if st.session_state.calculated:
    data = RADII_DATA[yield_val]
    density_ppl = density_val * 1000

    # 1. ГЕНЕРАЦІЯ КАРТИ
    m = folium.Map(location=[lat_val, lon_val], zoom_start=12, tiles="OpenStreetMap")
    
    # Сортування зон за радіусом від найбільшого до найменшого для коректного накладання
    zones_to_draw = []
    for style in ZONE_STYLES:
        cat, subcat = style["key"]
        r_km = data[cat][subcat]
        zones_to_draw.append({
            "name": style["name"],
            "radius_m": r_km * 1000,
            "radius_km": r_km,
            "color": style["color"],
            "fill_opacity": style["fill_opacity"]
        })
    zones_to_draw.sort(key=lambda x: x["radius_m"], reverse=True)

    # Додавання кіл на карту
    for zone in zones_to_draw:
        folium.Circle(
            location=[lat_val, lon_val],
            radius=zone["radius_m"],
            color=zone["color"],
            fill=True,
            fill_color=zone["color"],
            fill_opacity=zone["fill_opacity"],
            weight=1.5,
            popup=f"<b>{zone['name']}</b><br>Радіус: {zone['radius_km']:.2f} км"
        ).add_to(m)

    # Маркер епіцентру
    folium.Marker(
        [lat_val, lon_val],
        popup="<b>Епіцентр вибуху</b>",
        icon=folium.Icon(color="black", icon="warning-sign")
    ).add_to(m)

    st.markdown("<br>", unsafe_allow_html=True)
    st_folium(m, width=700, height=450)

    # 2. РОЗРАХУНОК КОМБІНОВАНИХ УРАЖЕНЬ
    r_tr_sev, r_tr_mod, r_tr_lit = data["trauma"]["severe"], data["trauma"]["moderate"], data["trauma"]["light"]
    r_b_3, r_b_2, r_b_1 = data["burns"]["degree_3"], data["burns"]["degree_2"], data["burns"]["degree_1"]
    r_r_4, r_r_3, r_r_2, r_r_1 = data["radiation"]["degree_4"], data["radiation"]["degree_3"], data["radiation"]["degree_2"], data["radiation"]["degree_1"]

    all_radii = sorted(list(set([0.0, r_tr_sev, r_tr_mod, r_tr_lit, r_b_3, r_b_2, r_b_1, r_r_4, r_r_3, r_r_2, r_r_1])))

    triple_comb = double_rad_burn = double_rad_trauma = double_thermo_mech = 0
    iso_burn = iso_trauma = iso_rad = 0

    for i in range(len(all_radii) - 1):
        r_in, r_out = all_radii[i], all_radii[i+1]
        r_mid = (r_in + r_out) / 2.0
        area = math.pi * (r_out**2 - r_in**2)
        pop = area * density_ppl

        has_tr = r_mid <= r_tr_lit
        has_b = r_mid <= r_b_1
        has_r = r_mid <= r_r_1

        if has_tr and has_b and has_r: triple_comb += pop
        elif has_b and has_r: double_rad_burn += pop
        elif has_tr and has_r: double_rad_trauma += pop
        elif has_tr and has_b: double_thermo_mech += pop
        elif has_b: iso_burn += pop
        elif has_tr: iso_trauma += pop
        elif has_r: iso_rad += pop

    total_unique = triple_comb + double_rad_burn + double_rad_trauma + double_thermo_mech + iso_burn + iso_trauma + iso_rad
    double_total = double_rad_burn + double_rad_trauma + double_thermo_mech
    iso_total = iso_burn + iso_trauma + iso_rad

    html_results = f"""
<div class="results-card">
<div class="res-main-title">РОЗРАХУНКОВІ ДАНІ (КОМБІНОВАНІ УРАЖЕННЯ):</div>
<div class="res-section-title">Загальна кількість унікальних постраждалих:</div>
<div class="res-cat-1">• всього поранених та уражених: <span class="val-white">{int(total_unique):,} осіб</span></div>
<div class="res-section-title">1. Потрійні комбіновані ураження (Травми + Опіки + ГПХ):</div>
<div class="res-cat-1">• всього: <span class="val-white">{int(triple_comb):,} осіб</span></div>
<div class="res-section-title">2. Двокомпонентні комбіновані ураження:</div>
<div class="res-cat-1">• всього: <span class="val-white">{int(double_total):,} осіб</span></div>
<div class="res-cat-1">• у тому числі:</div>
<div class="res-cat-2">- термомеханічні (Травма + Опік): <span class="val-white">{int(double_thermo_mech):,} осіб</span></div>
<div class="res-cat-2">- радіаційно-термічні (Опік + ГПХ): <span class="val-white">{int(double_rad_burn):,} осіб</span></div>
<div class="res-cat-2">- радіаційно-механічні (Травма + ГПХ): <span class="val-white">{int(double_rad_trauma):,} осіб</span></div>
<div class="res-section-title">3. Однофакторні (ізольовані) ураження:</div>
<div class="res-cat-1">• всього: <span class="val-white">{int(iso_total):,} осіб</span></div>
<div class="res-cat-1">• у тому числі:</div>
<div class="res-cat-2">- тільки термічні опіки: <span class="val-white">{int(iso_burn):,} осіб</span></div>
<div class="res-cat-2">- тільки механічні травми: <span class="val-white">{int(iso_trauma):,} осіб</span></div>
<div class="res-cat-2">- тільки променева хвороба: <span class="val-white">{int(iso_rad):,} осіб</span></div>
</div>
"""
    st.markdown(html_results, unsafe_allow_html=True)
