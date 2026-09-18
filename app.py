import math
import streamlit as st
import folium
from streamlit_folium import st_folium
from data import RADII_DATA

# 1. Конфігурація сторінки
st.set_page_config(
    page_title="Прогнозування втрат населення під час ядерного вибуху",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Стилізація інтерфейсу
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0e14;
        color: #ffffff;
    }
    
    .app-title {
        color: #FFD700;
        font-size: 22px;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 20px;
        letter-spacing: 0.5px;
    }
    
    .sec-header {
        color: #FFD700;
        font-size: 15px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 8px;
    }
    
    .yellow-divider {
        border-top: 1px solid #334155;
        margin: 12px 0;
    }
    
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
    
    .results-card {
        border: 1px solid #1e293b;
        background-color: #0d1117;
        padding: 18px;
        border-radius: 4px;
        margin-top: 15px;
        line-height: 1.6;
        height: 100%;
    }
    .res-main-title {
        color: #FFD700;
        font-weight: 800;
        font-size: 15px;
        text-transform: uppercase;
        margin-bottom: 12px;
        border-bottom: 1px solid #334155;
        padding-bottom: 6px;
    }
    .res-section-title { 
        color: #FFD700; 
        font-weight: 700; 
        font-size: 13px; 
        margin-top: 10px; 
        margin-bottom: 4px; 
    }
    .res-cat-1 { font-size: 13px; margin-left: 8px; margin-top: 3px; color: #E0E0E0; }
    .res-cat-2 { font-size: 13px; margin-left: 24px; margin-top: 2px; }
    .val-white { color: #FFFFFF !important; font-weight: bold; }
    
    .color-sev { color: #FF0000 !important; font-weight: bold; }
    .color-mod { color: #FF8C00 !important; font-weight: bold; }
    .color-lit { color: #FFD700 !important; font-weight: bold; }
    .color-tr  { color: #1E90FF !important; font-weight: bold; }
    .color-b   { color: #A52A2A !important; font-weight: bold; }
    .color-r   { color: #FF69B4 !important; font-weight: bold; }
    
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

# ДВОКОЛОНКОВИЙ МАКЕТ GOЛОВНОЇ СТОРІНКИ
col_left, col_right = st.columns([1.1, 2.0], gap="medium")

# --- ЛІВА ПАНЕЛЬ: ВХІДНІ ДАНІ ---
with col_left:
    st.markdown('<div class="app-title">Прогнозування втрат населення під час ядерного вибуху</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sec-header">Вихідні дані</div>', unsafe_allow_html=True)
    yield_val = st.selectbox(
        "Потужність ядерного вибуху (Кт):",
        options=list(RADII_DATA.keys()),
        index=2
    )
    
    st.markdown('<div class="yellow-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sec-header">Координати епіцентру ядерного вибуху</div>', unsafe_allow_html=True)
    col_lat, col_lon = st.columns(2)
    with col_lat:
        lat_val = st.number_input("Широта (Lat):", value=50.4501, format="%.4f")
    with col_lon:
        lon_val = st.number_input("Довгота (Lon):", value=30.5234, format="%.4f")
        
    st.markdown('<div class="yellow-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sec-header">Населення</div>', unsafe_allow_html=True)
    density_val = st.number_input(
        "Щільність населення в районі ядерного вибуху (тис. осіб/кв. км):",
        min_value=0.1,
        max_value=100.0,
        value=4.0,
        step=0.1
    )
    
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

# --- ПРАВА ПАНЕЛЬ: КАРТА ТА РЕЗУЛЬТАТИ ---
with col_right:
    data = RADII_DATA[yield_val]
    
    r_rad_max = data["radiation"]["degree_1"]
    
    max_radius = max(
        data["destruction"]["light"],
        data["trauma"]["light"],
        data["burns"]["degree_1"],
        r_rad_max
    )
    max_area = math.pi * (max_radius ** 2)

    st.markdown(
        f'''<div class="map-top-bar">
            <span>Максимальний радіус дії чинників: {max_radius:.2f} км</span>
            <span>Загальна площа зони дій вибуху: {max_area:.2f} км²</span>
        </div>''', 
        unsafe_allow_html=True
    )

    MAP_ZONE_STYLES = [
        {"cat": "destruction", "sub": "severe",   "name": "Зона сильних руйнувань (44.8 кПа)",       "color": "#FF0000", "fill_opacity": 0.40},
        {"cat": "destruction", "sub": "moderate", "name": "Зона помірних руйнувань (10.3 кПа)",      "color": "#FF8C00", "fill_opacity": 0.35},
        {"cat": "destruction", "sub": "light",    "name": "Зона слабких руйнувань (3.45 кПа)",       "color": "#FFD700", "fill_opacity": 0.25},
        {"cat": "trauma",      "sub": "light",    "name": "Зона травмування (радіус легких травм)",  "color": "#1E90FF", "fill_opacity": 0.25},
        {"cat": "burns",       "sub": "degree_1", "name": "Зона опіків (опіки I ступеня)",           "color": "#A52A2A", "fill_opacity": 0.25},
        {"cat": "radiation",   "sub": "degree_1", "name": "Зона променевої хвороби (ГПХ I ст.)",     "color": "#FF69B4", "fill_opacity": 0.30},
    ]

    m = folium.Map(location=[lat_val, lon_val], zoom_start=11, tiles=None)
    
    folium.TileLayer('openstreetmap', name='OpenStreetMap').add_to(m)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Супутникова карта'
    ).add_to(m)

    zones_to_draw = []
    for style in MAP_ZONE_STYLES:
        cat, sub = style["cat"], style["sub"]
        if cat in data and sub in data[cat]:
            r_km = data[cat][sub]
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
            weight=1.5,
            popup=f"<b>{zone['name']}</b><br>Радіус: {zone['radius_km']:.2f} км"
        ).add_to(m)

    # Темний маркер епіцентру (для контрасту з червоним колом)
    folium.Marker(
        [lat_val, lon_val],
        popup="<b>Епіцентр вибуху</b>",
        icon=folium.Icon(color="black", icon="warning-sign")
    ).add_to(m)

    folium.LayerControl(position='topright').add_to(m)
    st_folium(m, width=None, height=440, use_container_width=True)

    # --- ВИВІД РЕЗУЛЬТАТІВ У ДВІ КОЛОНКИ ПІД КАРТОЮ ---
    if st.session_state.calculated:
        density_ppl = density_val * 1000

        # Радіуси руйнувань
        r_dest_sev = data["destruction"]["severe"]
        r_dest_mod = data["destruction"]["moderate"]
        r_dest_lit = data["destruction"]["light"]

        # Радіуси травм
        r_tr_sev = data["trauma"]["severe"]
        r_tr_mod = data["trauma"]["moderate"]
        r_tr_lit = data["trauma"]["light"]

        # Радіуси опіків та радіації
        r_b_3, r_b_2, r_b_1 = data["burns"]["degree_3"], data["burns"]["degree_2"], data["burns"]["degree_1"]
        r_r_4, r_r_3, r_r_2, r_r_1 = data["radiation"]["degree_4"], data["radiation"]["degree_3"], data["radiation"]["degree_2"], data["radiation"]["degree_1"]

        # Обчислення площ зон (кв. км)
        s_dest_sev = math.pi * (r_dest_sev ** 2)
        s_dest_mod = math.pi * (r_dest_mod ** 2)
        s_dest_lit = math.pi * (r_dest_lit ** 2)

        s_tr_lit = math.pi * (r_tr_lit ** 2)
        s_tr_mod = math.pi * (r_tr_mod ** 2)
        s_tr_sev = math.pi * (r_tr_sev ** 2)

        s_b_1 = math.pi * (r_b_1 ** 2)
        s_r_1 = math.pi * (r_r_1 ** 2)

        # Інтегрування населення та втрат
        all_radii = sorted(list(set([
            0.0, r_dest_sev, r_dest_mod, r_dest_lit,
            r_tr_sev, r_tr_mod, r_tr_lit,
            r_b_3, r_b_2, r_b_1,
            r_r_4, r_r_3, r_r_2, r_r_1
        ])))

        pop_all_zones = 0.0
        pop_dest_sev = 0.0
        pop_dest_mod = 0.0
        pop_dest_lit = 0.0

        total_casualties = 0.0

        has_trauma_total = 0.0
        has_burns_total = 0.0
        has_rad_total = 0.0

        for i in range(len(all_radii) - 1):
            r_in, r_out = all_radii[i], all_radii[i+1]
            r_mid = (r_in + r_out) / 2.0
            
            area = math.pi * (r_out**2 - r_in**2)
            pop = area * density_ppl

            in_dest_sev = r_mid <= r_dest_sev
            in_dest_mod = (r_mid <= r_dest_mod) and not in_dest_sev
            in_dest_lit = (r_mid <= r_dest_lit) and not (in_dest_sev or in_dest_mod)
            in_any_dest = r_mid <= r_dest_lit

            has_tr = r_mid <= r_tr_lit
            has_b = r_mid <= r_b_1
            has_r = r_mid <= r_r_1

            if in_any_dest or has_tr or has_b or has_r:
                pop_all_zones += pop

            if in_dest_sev:
                pop_dest_sev += pop
            elif in_dest_mod:
                pop_dest_mod += pop
            elif in_dest_lit:
                pop_dest_lit += pop

            is_casualty = has_tr or has_b or has_r
            if is_casualty:
                total_casualties += pop

                if has_tr:
                    has_trauma_total += pop
                if has_b:
                    has_burns_total += pop
                if has_r:
                    has_rad_total += pop

        pop_dest_total = pop_dest_sev + pop_dest_mod + pop_dest_lit

        def fmt_int(val: float) -> str:
            return f"{int(round(val)):,}".replace(",", " ")

        def fmt_float(val: float) -> str:
            return f"{val:.2f}".replace(".", ",")

        res_col1, res_col2 = st.columns(2, gap="medium")

        with res_col1:
            html_losses = f"""<div class="results-card">
<div class="res-main-title">РОЗРАХУНКОВІ ДАНІ ВТРАТ НАСЕЛЕННЯ</div>
<div class="res-section-title">1. Кількість людей, яка опинилася у зонах дій вибуху:</div>
<div class="res-cat-1">• У ВСІХ ЗОНАХ РАЗОМ: <span class="val-white">{fmt_int(pop_all_zones)} осіб</span></div>
<div class="res-cat-1">• У зонах руйнування ОКРЕМО: <span class="val-white">{fmt_int(pop_dest_total)} осіб</span></div>
<div class="res-cat-2 color-sev">- зона сильних руйнувань: <span class="val-white">{fmt_int(pop_dest_sev)} осіб</span></div>
<div class="res-cat-2 color-mod">- зона помірних руйнувань: <span class="val-white">{fmt_int(pop_dest_mod)} осіб</span></div>
<div class="res-cat-2 color-lit">- зона слабких руйнувань: <span class="val-white">{fmt_int(pop_dest_lit)} осіб</span></div>

<div class="res-section-title">2. Кількість постраждалих:</div>
<div class="res-cat-1">• ВСЬОГО: <span class="val-white">{fmt_int(total_casualties)} осіб</span></div>
<div class="res-cat-1">• У ТОМУ ЧИСЛІ:</div>
<div class="res-cat-2 color-tr">- з травмами (разом легкі, середні та важкі): <span class="val-white">{fmt_int(has_trauma_total)} осіб</span></div>
<div class="res-cat-2 color-b">- з опіками (всіх ступенів разом): <span class="val-white">{fmt_int(has_burns_total)} осіб</span></div>
<div class="res-cat-2 color-r">- з гострою променевою хворобою (всіх ступенів разом): <span class="val-white">{fmt_int(has_rad_total)} осіб</span></div>
</div>"""
            st.markdown(html_losses, unsafe_allow_html=True)

        with res_col2:
            html_radii = f"""<div class="results-card">
<div class="res-main-title">РАДІУСИ ТА ПЛОЩА ЗОН УРАЖЕННЯ ЯДЕРНОГО ВИБУХУ</div>
<div class="res-section-title">Параметри зон руйнувань:</div>
<div class="res-cat-1 color-sev">• R зони значних руйнувань (Р=44,8 кПа) — <span class="val-white">{fmt_float(r_dest_sev)} км</span> (площа — <span class="val-white">{fmt_float(s_dest_sev)} кв.км</span>)</div>
<div class="res-cat-1 color-mod">• R зони помірних руйнувань (Р=10,3 кПа) — <span class="val-white">{fmt_float(r_dest_mod)} км</span> (площа — <span class="val-white">{fmt_float(s_dest_mod)} кв.км</span>)</div>
<div class="res-cat-1 color-lit">• R зони слабких руйнувань (Р=3,45 кПа) — <span class="val-white">{fmt_float(r_dest_lit)} км</span> (площа — <span class="val-white">{fmt_float(s_dest_lit)} кв.км</span>)</div>

<div class="res-section-title">Параметри зон травмування:</div>
<div class="res-cat-1 color-tr">• R зони травмування (легке) (Р=20 кПа) — <span class="val-white">{fmt_float(r_tr_lit)} км</span> (площа — <span class="val-white">{fmt_float(s_tr_lit)} кв.км</span>)</div>
<div class="res-cat-1 color-tr">• R зони травмування (середнє) (Р=50 кПа) — <span class="val-white">{fmt_float(r_tr_mod)} км</span> (площа — <span class="val-white">{fmt_float(s_tr_mod)} кв.км</span>)</div>
<div class="res-cat-1 color-tr">• R зони травмування (важке) (Р=100 кПа) — <span class="val-white">{fmt_float(r_tr_sev)} км</span> (площа — <span class="val-white">{fmt_float(s_tr_sev)} кв.км</span>)</div>

<div class="res-section-title">Параметри світлового та радіаційного ураження:</div>
<div class="res-cat-1 color-b">• R зони опіків шкіри без захисту (I-ІІІ ступенів) — <span class="val-white">{fmt_float(r_b_1)} км</span> (площа — <span class="val-white">{fmt_float(s_b_1)} кв.км</span>)</div>
<div class="res-cat-1 color-r">• R зони гострої променевої хвороби (І-ІII ступенів) — <span class="val-white">{fmt_float(r_r_1)} км</span> (площа — <span class="val-white">{fmt_float(s_r_1)} кв.км</span>)</div>
</div>"""
            st.markdown(html_radii, unsafe_allow_html=True)
