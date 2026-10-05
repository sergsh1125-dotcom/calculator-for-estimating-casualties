"""
data.py - Константи та функції для розрахунку зон ураження, руйнувань та втрат
при ядерному вибуху (для потужностей 0.5, 1.0, 10.0, 50.0, 100.0 Кт).
"""

# Повний масив радіусів ураження та руйнувань (в кілометрах)
RADII_DATA = {
    0.1: {
        "destruction": {"severe": 0.2, "moderate": 0.53, "light": 1.01},
        "trauma": {"severe": 0.13, "moderate": 0.18, "light": 0.32},
        "burns": {"degree_3": 0.14, "degree_2": 0.17, "degree_1": 0.24},
        "radiation": {"degree_4": 0.49, "degree_3": 0.57, "degree_2": 0.66, "degree_1": 0.75},
    },
    0.5: {
        "destruction": {"severe": 0.34, "moderate": 0.9, "light": 1.73},
        "trauma": {"severe": 0.22, "moderate": 0.32, "light": 0.55},
        "burns": {"degree_3": 0.29, "degree_2": 0.36, "degree_1": 0.51},
        "radiation": {"degree_4": 0.70, "degree_3": 0.79, "degree_2": 0.89, "degree_1": 1.00},
    },
    1.0: {
        "destruction": {"severe": 0.42, "moderate": 1.14, "light": 2.18},
        "trauma": {"severe": 0.27, "moderate": 0.40, "light": 0.69},
        "burns": {"degree_3": 0.41, "degree_2": 0.50, "degree_1": 0.71},
        "radiation": {"degree_4": 0.89, "degree_3": 0.94, "degree_2": 1.00, "degree_1": 1.12},
    },
    2.0: {
        "destruction": {"severe": 0.53, "moderate": 1.44, "light": 2.75},
        "trauma": {"severe": 0.35, "moderate": 0.50, "light": 0.87},
        "burns": {"degree_3": 0.57, "degree_2": 0.7, "degree_1": 0.98},
        "radiation": {"degree_4": 0.9, "degree_3": 1.00, "degree_2": 1.12, "degree_1": 1.23},
    },
    3.0: {
        "destruction": {"severe": 0.61, "moderate": 1.64, "light": 3.14},
        "trauma": {"severe": 0.4, "moderate": 0.57, "light": 0.99},
        "burns": {"degree_3": 0.69, "degree_2": 0.84, "degree_1": 1.2},
        "radiation": {"degree_4": 0.97, "degree_3": 1.07, "degree_2": 1.19, "degree_1": 1.31},
    },
    5.0: {
        "destruction": {"severe": 0.73, "moderate": 1.95, "light": 3.73},
        "trauma": {"severe": 0.47, "moderate": 0.68, "light": 1.18},
        "burns": {"degree_3": 0.87, "degree_2": 1.1, "degree_1": 1.5},
        "radiation": {"degree_4": 1.06, "degree_3": 1.16, "degree_2": 1.28, "degree_1": 1.41},
    },    
    10.0: {
        "destruction": {"severe": 0.91, "moderate": 2.46, "light": 4.70},
        "trauma": {"severe": 0.59, "moderate": 0.86, "light": 1.49},
        "burns": {"degree_3": 1.20, "degree_2": 1.50, "degree_1": 2.10},
        "radiation": {"degree_4": 1.27, "degree_3": 1.33, "degree_2": 1.41, "degree_1": 1.55},
    },
    20.0: {
        "destruction": {"severe": 1.16, "moderate": 3.09, "light": 5.92},
        "trauma": {"severe": 0.74, "moderate": 1.08, "light": 1.87},
        "burns": {"degree_3": 1.7, "degree_2": 2.00, "degree_1": 2.8},
        "radiation": {"degree_4": 1.3, "degree_3": 1.42, "degree_2": 1.56, "degree_1": 1.72},
    },
    30.0: {
        "destruction": {"severe": 1.32, "moderate": 3.54, "light": 6.77},
        "trauma": {"severe": 0.85, "moderate": 1.23, "light": 2.14},
        "burns": {"degree_3": 2.00, "degree_2": 2.4, "degree_1": 3.4},
        "radiation": {"degree_4": 1.39, "degree_3": 1.51, "degree_2": 1.66, "degree_1": 1.82},
    },
    50.0: {
        "destruction": {"severe": 1.56, "moderate": 4.2, "light": 8.04},
        "trauma": {"severe": 1.00, "moderate": 1.46, "light": 2.54},
        "burns": {"degree_3": 2.50, "degree_2": 3.10, "degree_1": 4.30},
        "radiation": {"degree_4": 1.61, "degree_3": 1.64, "degree_2": 1.80, "degree_1": 1.96},
    },
    100.0: {
        "destruction": {"severe": 1.97, "moderate": 5.29, "light": 10.13},
        "trauma": {"severe": 1.27, "moderate": 1.84, "light": 3.20},
        "burns": {"degree_3": 3.50, "degree_2": 4.20, "degree_1": 5.80},
        "radiation": {"degree_4": 1.69, "degree_3": 1.83, "degree_2": 1.99, "degree_1": 2.16},
    },
}

# Опорні радіуси руйнування будівель для масштабування на довільну потужність (10 Кт)
DESTRUCTION_ZONES_10KT = {
    "severe": {
        "name_ua": "Зона значних руйнувань (44.8 кПа)",
        "overpressure_kpa": 44.8,
        "r10_km": 0.91,
    },
    "moderate": {
        "name_ua": "Зона середніх руйнувань (10.3 кПа)",
        "overpressure_kpa": 10.3,
        "r10_km": 2.46,
    },
    "light": {
        "name_ua": "Зона слабких руйнувань (3.45 кПа)",
        "overpressure_kpa": 3.45,
        "r10_km": 4.70,
    },
}


def calculate_blast_radii(yield_kt: float) -> dict[str, float]:
    """
    Розраховує радіуси зон руйнувань будівель (км) за кубічним законом масштабування
    для довільної потужності заряду W (Кт).
    """
    if yield_kt <= 0:
        raise ValueError("Потужність вибуху повинна бути більшою за 0")

    scale_factor = (yield_kt / 10.0) ** (1 / 3)

    return {
        zone_key: round(zone_data["r10_km"] * scale_factor, 2)
        for zone_key, zone_data in DESTRUCTION_ZONES_10KT.items()
    }


def get_radii_for_yield(yield_kt: float) -> dict:
    """
    Повертає словник радіусів із предрозрахованої таблиці RADII_DATA або
    розраховує руйнування динамічно, якщо потужності немає в таблиці.
    """
    if yield_kt in RADII_DATA:
        return RADII_DATA[yield_kt]

    # Якщо потужність не стандартна (наприклад, 20 Кт), розраховуємо руйнування динамічно
    return {
        "destruction": calculate_blast_radii(yield_kt),
        "trauma": {},
        "burns": {},
        "radiation": {},
    }


# Стилі зон для відображення на інтерактивній карті (Folium / Streamlit)
ZONE_STYLES = [
    {
        "key": ("destruction", "light"),
        "name": "Слабкі руйнування будівель (3.45 кПа)",
        "color": "#708090",
        "fill_opacity": 0.20,
    },
    {
        "key": ("burns", "degree_1"),
        "name": "Опіки I-ІІІ ступенів",
        "color": "#FFD700",
        "fill_opacity": 0.25,
    },
    {
        "key": ("destruction", "moderate"),
        "name": "Середні руйнування будівель (10.3 кПа)",
        "color": "#FF8C00",
        "fill_opacity": 0.35,
    },
    {
        "key": ("trauma", "light"),
        "name": "Травми легкого ступеня",
        "color": "#FFA500",
        "fill_opacity": 0.25,
    },
    {
        "key": ("radiation", "degree_4"),
        "name": "Проникаюча радіація (ГПХ IV ст. / вкрай важка)",
        "color": "#32CD32",
        "fill_opacity": 0.40,
    },
    {
        "key": ("destruction", "severe"),
        "name": "Значні руйнування будівель (44.8 кПа)",
        "color": "#8B0000",
        "fill_opacity": 0.50,
    },
]
