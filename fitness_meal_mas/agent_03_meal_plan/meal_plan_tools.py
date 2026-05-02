"""Meal-planning tool helpers (Agent 3; rule-based option / tests)."""


def _filter_allergies(options: list[str], allergies: list[str]) -> list[str]:
    """Filter food options that contain allergic ingredients."""
    if not allergies:
        return options
    blocked = [a.lower() for a in allergies]
    safe = []
    for item in options:
        item_lower = item.lower()
        if not any(allergen in item_lower for allergen in blocked):
            safe.append(item)
    return safe


def generate_meal_plan(diet_type: str, allergies: list[str]) -> dict[str, list[str]]:
    """Generate a simple rule-based meal plan."""
    veg_options = {
        "breakfast": ["Oats with banana", "Greek yogurt with berries", "Paneer sandwich"],
        "lunch": ["Brown rice + dal + salad", "Quinoa bowl with chickpeas", "Tofu stir-fry"],
        "snack": ["Mixed nuts", "Fruit bowl", "Protein smoothie"],
        "dinner": ["Vegetable soup + whole-grain bread", "Paneer curry + roti", "Lentil pasta"],
    }
    non_veg_options = {
        "breakfast": ["Egg omelette + toast", "Oats with milk", "Greek yogurt with berries"],
        "lunch": ["Grilled chicken + rice + veggies", "Tuna salad bowl", "Chicken wrap"],
        "snack": ["Boiled eggs", "Mixed nuts", "Protein smoothie"],
        "dinner": ["Baked fish + sweet potato", "Chicken soup + bread", "Turkey stir-fry"],
    }

    base = veg_options if diet_type == "vegetarian" else non_veg_options
    meal_plan: dict[str, list[str]] = {}

    for meal_time, options in base.items():
        safe_options = _filter_allergies(options, allergies)
        if not safe_options:
            safe_options = ["Custom allergy-safe meal needed"]
        meal_plan[meal_time] = safe_options[:2]

    return meal_plan
