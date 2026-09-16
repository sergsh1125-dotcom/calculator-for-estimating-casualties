import math
import streamlit as st
import folium
from streamlit_folium import st_folium
from data import RADII_DATA, ZONE_STYLES

# 1. Широкоекрана конфігурація (двоколоночний макет)
st.set_page_config(
    page_title="Прогнозування втрат від ядерного вибуху",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Стилізація інтерфейсу подібна до хімічного калькулятора
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0e14;
        color: #ffffff;
    }
    
    /* Заголовок додатку */
    .app-title {
        color: #FFD700;
        font-size: 22px;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 20px;
        letter-spacing: 0.5px;
    }
    
    /* Заголовки секцій в лівій колонці */
    .sec-header {
        color: #FFD700;
        font-size: 15px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 8px;
    }
    
    /* Розділювальна лінія */
    .yellow-divider {
        border-top: 1px solid #334155;
        margin: 15px 0;
    }
    
    /* Верхній інфо-бар над картою */
    .map-top-bar {
        background-color: #161b22;
        border: 1px solid #FFD700;
        padding: 6px 14px;
        font-size: 13px;
        color: #FFD700;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
        border-radius: 2px 2px 0 0;
    }
    
    /* Блок результатів під картою */
    .results-card {
        border: 1px solid #1e293b;
        background-color: #0d1117;
        padding: 18px;
        border-radius: 4px;
        margin-top: 15px;
        line-height: 1.5;
    }
    .res-main-title {
        color: #FFD700;
        font-weight: 800;
        font-size: 16px;
        text-transform: uppercase;
        margin-bottom: 12px;
        border-bottom: 1px solid #334155;
        padding-bottom: 6px;
    }
    .res-section-title { color: #FFD700; font-weight: 700; font-size: 14px; margin-top: 10px; margin-bottom: 2px; }
    .res-cat-1 { color: #FFD700; font-size: 13px; margin-left: 12px; }
    .res-cat-2 { color: #FFD700; font-size: 13px; margin-left: 26px; }
    .val-white { color: #FFFFFF !important; font-weight: bold; }
    
    /* Кнопки */
    div.stButton > button:first-child {
        width: 100%;
        font-weight: bold;
        text-transform: uppercase;
        height: 42px;
        border-radius: 3px;
        border: none;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
        background-color: #FFD700 !important;
        color: #000000 !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
        background-color: #8B0000 !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

if "calculated" not in st.session_state:
    st.session_state.calculated = False

# ДВОКОЛОНКОВИЙ МАКЕТ (Ліва колонка — Параметри, Права — Карта та Результати)
col_left, col_right = st.columns([1.1, 2.0], gap="medium")

# --- ЛІВА ПАНЕЛЬ: ВХІДНІ ДАНІ ---
with col_left:
    st.markdown('<div class="app-title">Прогнозування втрат населення під час ядерного вибуху</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sec-header">Вихідні дані вибуху</div>', unsafe_allow_html=True)
    yield_val = st.selectbox(
        "Потужність ядерного вибуху (Кт):",
        options=list(RADII_DATA.keys()),
        index=2
    )
    
    st.markdown('<div class="yellow-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sec-header">Характеристики території</div>', unsafe_allow_html=True)
    density_val = st.number_input(
        "Щільність населення в районі застосування (тис. осіб/кв. км):",
        min_value=0.1,
        max_value=100.0,
        value=4.0,
        step=0.1
    )
    
    st.markdown('<div class="yellow-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sec-header">Координати епіцентру вибуху</div>', unsafe_allow_html=True)
    col_lat, col_lon = st.columns(2)
    with col_lat:
        lat_val = st.number_input("Широта (Lat):", value=50.4501, format="%.4f")
    with col_lon:
        lon_val = st.number_input("Довгота (Lon):", value=30.5234, format="%.4f")
        
    st.markdown('<div class="yellow-divider"></div>', unsafe_allow_html=True)
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        btn_calc = st.button("РОЗРАХУВАТИ")
    with btn_col2:
        btn_clear = st.button("ОЧИСТИТИ")

if btn_clear:
    st.session_state.calculated = False
    st.rerun()

if btn_calc:
    st.session_state.calculated = True

# --- ПРАВА ПАНЕЛЬ: КАРТА ТА РОЗРАХУНКИ ---
with col_right:
    data = RADII_DATA[yield_val]
    max_radius = max(
        data["trauma"]["light"],
        data["burns"]["degree_1"],
        data["radiation"]["degree_1"]
    )
    max_area = math.pi * (max_radius ** 2)

    # Верхній інфо-бар
    st.markdown(
        f'''<div class="map-top-bar">
            <span>Максимальний радіус зони ураження: {max_radius:.2f} км</span>
            <span>Площа зони ураження: {max_area:.2f} км²</span>
        </div>''', 
        unsafe_allow_html=True
    )

    # Карта з підтримкою шарів OpenStreetMap та Esri Satellite
    m = folium.Map(location=[lat_val, lon_val], zoom_start=11, tiles=None)
    
    folium.TileLayer('openstreetmap', name='OpenStreetMap').add_to(m)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Супутникова карта'
    ).add_to(m)

    # Побудова зон ураження
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

    for zone in zones_to_draw:
        folium.Circle(
            location=[lat_val, lon_val],
            radius=zone["radius_m"],
            color=zone["color"],
            fill=True,
            fill_color=zone["color"],
            fill_opacity=zone["fill_opacity"],
            weight=1.2,
            popup=f"<b>{zone['name']}</b><br>Радіус: {zone['radius_km']:.2f} км"
        ).add_to(m)

    folium.Marker(
        [lat_val, lon_val],
        popup="<b>Епіцентр вибуху</b>",
        icon=folium.Icon(color="red", icon="warning-sign")
    ).add_to(m)

    folium.LayerControl(position='topright').add_to(m)
    st_folium(m, width=None, height=460, use_container_width=True)

    # Вивід результатів розрахунку
    if st.session_state.calculated:
        density_ppl = density_val * 1000

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
<div class="res-cat-2">- термомеханічні (Травма + Опік): <span class="val-white">{int(double_thermo_mech):,} осіб</span></div>
<div class="res-cat-2">- радіаційно-термічні (Опік + ГПХ): <span class="val-white">{int(double_rad_burn):,} осіб</span></div>
<div class="res-cat-2">- радіаційно-механічні (Травма + ГПХ): <span class="val-white">{int(double_rad_trauma):,} осіб</span></div>

<div class="res-section-title">3. Однофакторні (ізольовані) ураження:</div>
<div class="res-cat-1">• всього: <span class="val-white">{int(iso_total):,} осіб</span></div>
<div class="res-cat-2">- тільки термічні опіки: <span class="val-white">{int(iso_burn):,} осіб</span></div>
<div class="res-cat-2">- тільки механічні травми: <span class="val-white">{int(iso_trauma):,} осіб</span></div>
<div class="res-cat-2">- тільки променева хвороба: <span class="val-white">{int(iso_rad):,} осіб</span></div>
</div>
"""
        st.markdown(html_results, unsafe_allow_html=True)
