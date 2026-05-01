"""Unit tests for rule-based MAS tool functions."""

import unittest

from tools.fitness_tools import calculate_bmi
from tools.meal_tools import generate_grocery_list
from tools.nutrition_tools import (
    adjust_calories_for_goal,
    calculate_macros,
    estimate_maintenance_calories,
)


class TestFitnessTools(unittest.TestCase):
    """Tests for fitness tool functions."""

    def test_calculate_bmi(self) -> None:
        """BMI should be rounded to two decimals."""
        self.assertEqual(calculate_bmi(70, 175), 22.86)


class TestNutritionTools(unittest.TestCase):
    """Tests for nutrition tool functions."""

    def test_maintenance_calories(self) -> None:
        """Maintenance calories should use activity multiplier."""
        self.assertEqual(estimate_maintenance_calories(70, "moderate"), 2387)

    def test_adjust_calories_for_goal(self) -> None:
        """Goal-specific calorie adjustments should match rules."""
        self.assertEqual(adjust_calories_for_goal(2387, "lose weight"), 1987)
        self.assertEqual(adjust_calories_for_goal(2387, "maintain"), 2387)
        self.assertEqual(adjust_calories_for_goal(2387, "gain muscle"), 2687)

    def test_macro_calculation(self) -> None:
        """Macros should contain positive grams for all categories."""
        macros = calculate_macros(2400, "maintain")
        self.assertEqual(set(macros.keys()), {"protein_g", "carbs_g", "fats_g"})
        self.assertGreater(macros["protein_g"], 0)
        self.assertGreater(macros["carbs_g"], 0)
        self.assertGreater(macros["fats_g"], 0)


class TestMealTools(unittest.TestCase):
    """Tests for meal-related tool functions."""

    def test_grocery_generation(self) -> None:
        """Grocery list should include parsed ingredient tokens."""
        meal_plan = {
            "breakfast": ["Oats with banana", "Greek yogurt with berries"],
            "lunch": ["Brown rice + dal + salad"],
            "snack": ["Mixed nuts"],
            "dinner": ["Vegetable soup + whole-grain bread"],
        }
        grocery = generate_grocery_list(meal_plan)

        self.assertIsInstance(grocery, list)
        self.assertTrue(any(item.startswith("oats ") for item in grocery))
        self.assertTrue(any(item.startswith("banana ") for item in grocery))
        self.assertTrue(any(item.startswith("rice ") for item in grocery))


if __name__ == "__main__":
    unittest.main()
