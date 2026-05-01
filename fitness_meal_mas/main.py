"""CLI entry point for AI-Powered Fitness & Meal Planning MAS."""

import os
from collections.abc import Callable

from agents.fitness_profile_agent import run_fitness_profile_agent
from agents.grocery_workout_agent import run_grocery_workout_agent
from agents.meal_plan_agent import run_meal_plan_agent
from agents.nutrition_agent import run_nutrition_agent
from state.app_state import AppState
from tools.fitness_tools import (
    normalize_activity,
    normalize_allergies,
    normalize_diet_type,
    normalize_goal,
)


def _get_positive_float(prompt_text: str) -> float:
    """Prompt until a valid positive float is entered."""
    while True:
        raw_value = input(prompt_text).strip()
        try:
            value = float(raw_value)
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a valid positive number.")


def _get_validated_text(
    prompt_text: str, validator: Callable[[str], str], error_hint: str
) -> str:
    """Prompt until validator accepts the input and returns normalized value."""
    while True:
        raw_value = input(prompt_text).strip()
        if not raw_value:
            print("Input cannot be empty. Please try again.")
            continue
        try:
            return validator(raw_value)
        except ValueError:
            print(error_hint)


def _get_allergies(prompt_text: str) -> str:
    """Prompt allergies and normalize minor variants like empty/none."""
    while True:
        raw_value = input(prompt_text).strip()
        if not raw_value:
            return "none"
        try:
            normalized = normalize_allergies(raw_value)
            if not normalized:
                return "none"
            return ", ".join(normalized)
        except ValueError:
            # Kept for future-proofing if validator logic changes.
            print("Please enter comma-separated allergies or 'none'.")


def main() -> None:
    """Run the full multi-agent pipeline."""
    print("=" * 60)
    print("AI-Powered Fitness & Meal Planning MAS")
    print("=" * 60)

    app_state = AppState()

    try:
        default_model = os.getenv("OLLAMA_MODEL", "llama3:8b")
        chosen_model = input(
            f"Enter local Ollama model [default: {default_model}]: "
        ).strip()
        model = chosen_model or default_model

        user_data = {
            "weight_kg": _get_positive_float("Enter your weight (kg): "),
            "height_cm": _get_positive_float("Enter your height (cm): "),
            "goal": _get_validated_text(
                "Goal [lose weight / maintain / gain muscle]: ",
                normalize_goal,
                "Invalid goal. Choose: lose weight, maintain, or gain muscle.",
            ),
            "activity_level": _get_validated_text(
                "Activity level [sedentary / light / moderate / active / very active]: ",
                normalize_activity,
                "Invalid activity level. Choose: sedentary, light, moderate, active, very active.",
            ),
            "diet_type": _get_validated_text(
                "Diet type [vegetarian / non-vegetarian]: ",
                normalize_diet_type,
                "Invalid diet type. Choose: vegetarian or non-vegetarian.",
            ),
            "allergies": _get_allergies(
                "Allergies (comma-separated, press Enter for none): "
            ),
        }

        run_fitness_profile_agent(app_state, user_data, model)
        run_nutrition_agent(app_state, model)
        run_meal_plan_agent(app_state, model)
        final_report = run_grocery_workout_agent(app_state, model)

        print("\nPipeline completed successfully.")
        print("Final report saved to outputs/final_report.txt")
        print("\n--- Final Report ---")
        print(final_report)
    except Exception as error:  # noqa: BLE001 - explicit user-facing handling
        print(f"An error occurred: {error}")
        print("Please restart and enter valid inputs.")


if __name__ == "__main__":
    main()
