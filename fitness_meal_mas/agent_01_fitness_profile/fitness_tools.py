"""Fitness-related tool functions (Agent 1)."""


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Calculate BMI using weight in kg and height in cm."""
    height_m = height_cm / 100
    return round(weight_kg / (height_m**2), 2)


def get_bmi_category(bmi: float) -> str:
    """Return a standard BMI category string."""
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal weight"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def normalize_goal(goal: str) -> str:
    """Normalize and validate user goal."""
    clean_goal = goal.strip().lower()
    goal_aliases = {
        "lose": "lose weight",
        "lose fat": "lose weight",
        "maintain": "maintain",
        "gain": "gain muscle",
        "build muscle": "gain muscle",
    }
    clean_goal = goal_aliases.get(clean_goal, clean_goal)
    if clean_goal not in {"lose weight", "maintain", "gain muscle"}:
        raise ValueError("Goal must be: lose weight, maintain, or gain muscle.")
    return clean_goal


def normalize_activity(activity_level: str) -> str:
    """Normalize and validate activity level."""
    clean_level = activity_level.strip().lower()
    valid_levels = {"sedentary", "light", "moderate", "active", "very active"}
    if clean_level not in valid_levels:
        raise ValueError(
            "Activity level must be one of: sedentary, light, moderate, active, very active."
        )
    return clean_level


def normalize_diet_type(diet_type: str) -> str:
    """Normalize and validate diet type."""
    clean_diet = diet_type.strip().lower()
    if clean_diet not in {"vegetarian", "non-vegetarian"}:
        raise ValueError("Diet type must be 'vegetarian' or 'non-vegetarian'.")
    return clean_diet


def normalize_allergies(allergies: str) -> list[str]:
    """Convert comma-separated allergies into a normalized list."""
    allergies = allergies.strip().lower()
    if allergies in {"none", "no", "n/a"}:
        return []
    return [item.strip() for item in allergies.split(",") if item.strip()]
