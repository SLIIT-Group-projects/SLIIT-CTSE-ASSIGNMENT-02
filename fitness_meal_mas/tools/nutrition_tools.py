"""Nutrition-related tool functions."""


def get_activity_multiplier(activity_level: str) -> float:
    """Map activity level to calorie multiplier."""
    mapping = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very active": 1.9,
    }
    return mapping[activity_level]


def estimate_maintenance_calories(weight_kg: float, activity_level: str) -> int:
    """
    Estimate maintenance calories.

    Rule-based approximation:
    - Baseline calories = weight * 22
    - Multiply by activity multiplier
    """
    baseline = weight_kg * 22
    calories = baseline * get_activity_multiplier(activity_level)
    return int(round(calories))


def adjust_calories_for_goal(maintenance_calories: int, goal: str) -> int:
    """Adjust calorie target based on goal."""
    if goal == "lose weight":
        return maintenance_calories - 400
    if goal == "gain muscle":
        return maintenance_calories + 300
    return maintenance_calories


def calculate_macros(daily_calories: int, goal: str) -> dict[str, int]:
    """
    Calculate macro split and convert to grams.

    Protein/Carb/Fat ratios vary by goal:
    - lose weight: 35/35/30
    - maintain: 30/40/30
    - gain muscle: 30/45/25
    """
    if goal == "lose weight":
        p_ratio, c_ratio, f_ratio = 0.35, 0.35, 0.30
    elif goal == "gain muscle":
        p_ratio, c_ratio, f_ratio = 0.30, 0.45, 0.25
    else:
        p_ratio, c_ratio, f_ratio = 0.30, 0.40, 0.30

    protein_g = int(round((daily_calories * p_ratio) / 4))
    carbs_g = int(round((daily_calories * c_ratio) / 4))
    fats_g = int(round((daily_calories * f_ratio) / 9))

    return {"protein_g": protein_g, "carbs_g": carbs_g, "fats_g": fats_g}

