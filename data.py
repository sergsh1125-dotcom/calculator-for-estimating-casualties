"""
Нормативні радіуси ураження ядерного вибуху (в км) та параметри візуалізації.
Джерело: DOD/DOE (Glasstone & Dolan), FEMA Planning Guidance.
"""

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

# Кольорова гама та стиль зон для інтерактивної карти
ZONE_STYLES = [
    {"key": ("trauma", "light"), "name": "Слабкі руйнування (10 кПа / 1 psi)", "color": "#708090", "fill_opacity": 0.25},
    {"key": ("burns", "degree_1"), "name": "Опіки I ступеня", "color": "#FFD700", "fill_opacity": 0.20},
    {"key": ("trauma", "moderate"), "name": "Помірні руйнування (30 кПа / 3-5 psi)", "color": "#FF8C00", "fill_opacity": 0.35},
    {"key": ("burns", "degree_3"), "name": "Опіки III ступеня", "color": "#FF4500", "fill_opacity": 0.35},
    {"key": ("radiation", "degree_4"), "name": "Проникаюча радіація (ГПХ IV ст.)", "color": "#32CD32", "fill_opacity": 0.40},
    {"key": ("trauma", "severe"), "name": "Сильні руйнування (50 кПа / 20 psi)", "color": "#8B0000", "fill_opacity": 0.50},
]
