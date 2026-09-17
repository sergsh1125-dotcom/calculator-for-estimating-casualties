RADII_DATA = {
    0.5: {
        "trauma": {"severe": 0.22, "moderate": 0.32, "light": 0.55},
        "burns": {"degree_3": 0.29, "degree_2": 0.36, "degree_1": 0.51},
        "radiation": {"degree_4": 0.70, "degree_3": 0.79, "degree_2": 0.89, "degree_1": 1.00}
    },
    1.0: {
        "trauma": {"severe": 0.27, "moderate": 0.40, "light": 0.69},
        "burns": {"degree_3": 0.41, "degree_2": 0.50, "degree_1": 0.71},
        "radiation": {"degree_4": 0.89, "degree_3": 0.94, "degree_2": 1.00, "degree_1": 1.12}
    },
    10.0: {
        "trauma": {"severe": 0.59, "moderate": 0.86, "light": 1.49},
        "burns": {"degree_3": 1.20, "degree_2": 1.50, "degree_1": 2.10},
        "radiation": {"degree_4": 1.27, "degree_3": 1.33, "degree_2": 1.41, "degree_1": 1.55}
    },
    50.0: {
        "trauma": {"severe": 1.00, "moderate": 1.46, "light": 2.54},
        "burns": {"degree_3": 2.50, "degree_2": 3.10, "degree_1": 4.30},
        "radiation": {"degree_4": 1.61, "degree_3": 1.64, "degree_2": 1.80, "degree_1": 1.96}
    },
    100.0: {
        "trauma": {"severe": 1.27, "moderate": 1.84, "light": 3.20},
        "burns": {"degree_3": 3.50, "degree_2": 4.20, "degree_1": 5.80},
        "radiation": {"degree_4": 1.69, "degree_3": 1.83, "degree_2": 1.99, "degree_1": 2.16}
    }
}
"""
data.py - Константи та функції розрахунку радіусів зон руйнувань ядерного вибуху.
Розраховано за законом масштабування кубічного кореня: R(W) = R_10 * (W / 10)^(1/3)
"""

# Опорні радіуси для потужності 10 Кт (в кілометрах)
DESTRUCTION_ZONES_10KT = {
    "severe": {
        "name_ua": "Зона значних руйнувань",
        "overpressure_kpa": 44.8,
        "r10_km": 0.8,
    },
    "moderate": {
        "name_ua": "Зона середніх руйнувань",
        "overpressure_kpa": 10.3,
        "r10_km": 1.6,
    },
    "light": {
        "name_ua": "Зона слабких руйнувань",
        "overpressure_kpa": 3.45,
        "r10_km": 4.7,
    },
}

# Таблиця предрозрахованих радіусів для фіксованих потужностей (в км)
DESTRUCTION_RADIIS_TABLE = {
    0.5: {
        "severe": 0.29,
        "moderate": 0.59,
        "light": 1.73,
    },
    1.0: {
        "severe": 0.37,
        "moderate": 0.74,
        "light": 2.18,
    },
    10.0: {
        "severe": 0.80,
        "moderate": 1.60,
        "light": 4.70,
    },
    50.0: {
        "severe": 1.37,
        "moderate": 2.74,
        "light": 8.04,
    },
    100.0: {
        "severe": 1.72,
        "moderate": 3.45,
        "light": 10.13,
    },
}


def calculate_blast_radii(yield_kt: float) -> dict[str, float]:
    """
    Розраховує радіуси зон руйнувань (км) для довільної потужності вибуху (Кт)
    на основі кубічного закону масштабування відносно опорного заряду 10 Кт.

    :param yield_kt: Потужність вибуху в кілотонах (Кт)
    :return: Словник з радіусами зон у км ('severe', 'moderate', 'light')
    """
    if yield_kt <= 0:
        raise ValueError("Потужність вибуху повинна бути більшою за 0")

    scale_factor = (yield_kt / 10.0) ** (1 / 3)

    return {
        zone_key: round(zone_data["r10_km"] * scale_factor, 2)
        for zone_key, zone_data in DESTRUCTION_ZONES_10KT.items()
    }
# Кольорова гама та стиль зон для інтерактивної карти
ZONE_STYLES = [
    {"key": ("trauma", "light"), "name": "Слабкі руйнування (3.5 кПа)", "color": "#708090", "fill_opacity": 0.25},
    {"key": ("burns", "degree_1"), "name": "Опіки IІ ступеня", "color": "#FFD700", "fill_opacity": 0.20},
    {"key": ("trauma", "moderate"), "name": "Помірні руйнування (10 кПа)", "color": "#FF8C00", "fill_opacity": 0.35},
    {"key": ("radiation", "degree_4"), "name": "Проникаюча радіація (ГПХ І ст.)", "color": "#32CD32", "fill_opacity": 0.40},
    {"key": ("trauma", "severe"), "name": "Значні руйнування (45 кПа)", "color": "#8B0000", "fill_opacity": 0.50},
]
