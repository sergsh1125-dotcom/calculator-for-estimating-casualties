"""
Нормативні радіуси ураження ядерного вибуху (в км).
Джерело: DOD/DOE (Glasstone & Dolan), FEMA Planning Guidance.
"""

RADII_DATA = {
    0.5: {
        "trauma": {"severe": 0.20, "moderate": 0.35, "light": 0.55},
        "burns": {"degree_3": 0.30, "degree_2": 0.45, "degree_1": 0.65},
        "radiation": {"degree_4": 0.40, "degree_3": 0.50, "degree_2": 0.60, "degree_1": 0.75}
    },
    1.0: {
        "trauma": {"severe": 0.25, "moderate": 0.45, "light": 0.70},
        "burns": {"degree_3": 0.45, "degree_2": 0.65, "degree_1": 0.90},
        "radiation": {"degree_4": 0.50, "degree_3": 0.65, "degree_2": 0.80, "degree_1": 1.00}
    },
    10.0: {
        "trauma": {"severe": 0.55, "moderate": 0.95, "light": 1.50},
        "burns": {"degree_3": 1.20, "degree_2": 1.60, "degree_1": 2.20},
        "radiation": {"degree_4": 0.90, "degree_3": 1.10, "degree_2": 1.30, "degree_1": 1.60}
    },
    50.0: {
        "trauma": {"severe": 1.00, "moderate": 1.70, "light": 2.60},
        "burns": {"degree_3": 2.30, "degree_2": 3.10, "degree_1": 4.20},
        "radiation": {"degree_4": 1.30, "degree_3": 1.50, "degree_2": 1.80, "degree_1": 2.20}
    },
    100.0: {
        "trauma": {"severe": 1.25, "moderate": 2.15, "light": 3.30},
        "burns": {"degree_3": 3.10, "degree_2": 4.10, "degree_1": 5.60},
        "radiation": {"degree_4": 1.50, "degree_3": 1.80, "degree_2": 2.10, "degree_1": 2.50}
    }
}
