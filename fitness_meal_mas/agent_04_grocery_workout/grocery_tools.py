"""Grocery list generation from a meal plan (Agent 4)."""

from collections import Counter


def generate_grocery_list(meal_plan: dict[str, list[str]]) -> list[str]:
    """Generate grocery list by tokenizing meal names."""
    ingredient_words: list[str] = []
    for meal_items in meal_plan.values():
        for dish in meal_items:
            cleaned = dish.replace("+", " ").replace("-", " ").lower()
            for token in cleaned.split():
                if token in {"with", "and", "custom", "allergy", "safe", "meal", "needed"}:
                    continue
                ingredient_words.append(token)

    counts = Counter(ingredient_words)
    sorted_items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [f"{name} x{qty}" for name, qty in sorted_items]
