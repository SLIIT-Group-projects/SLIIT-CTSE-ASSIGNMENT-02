"""Final report formatting and persistence (Agent 4)."""

from typing import Any

from shared.paths import REPORT_FILE


def build_final_report(state_data: dict[str, Any]) -> str:
    """Compose final text report from shared state."""
    profile = state_data["profile"]
    nutrition = state_data["nutrition"]
    meal_plan = state_data["meal_plan"]
    grocery = state_data["grocery_list"]
    workout = state_data["workout_plan"]

    lines = [
        "AI-Powered Fitness & Meal Planning MAS",
        "FINAL PERSONALIZED REPORT",
        "=" * 62,
        "",
        "[1] FITNESS PROFILE",
        "-" * 62,
        f"Weight (kg)       : {profile['weight_kg']}",
        f"Height (cm)       : {profile['height_cm']}",
        f"Goal              : {profile['goal']}",
        f"Activity Level    : {profile['activity_level']}",
        f"Diet Type         : {profile['diet_type']}",
        f"Allergies         : {', '.join(profile['allergies']) if profile['allergies'] else 'None'}",
        f"BMI               : {profile['bmi']}",
        f"BMI Category      : {profile['bmi_category']}",
        "",
        "[2] DAILY NUTRITION TARGETS",
        "-" * 62,
        f"Daily Calories    : {nutrition['daily_calories']} kcal",
        f"Protein           : {nutrition['protein_g']} g",
        f"Carbohydrates     : {nutrition['carbs_g']} g",
        f"Fats              : {nutrition['fats_g']} g",
        "",
        "[3] MEAL PLAN",
        "-" * 62,
    ]

    for meal_time, items in meal_plan.items():
        lines.append(f"{meal_time.title():<18}: {', '.join(items)}")

    lines.extend(["", "[4] GROCERY LIST", "-" * 62])
    for item in grocery:
        lines.append(f"- {item}")

    lines.extend(["", "[5] 7-DAY WORKOUT PLAN", "-" * 62])
    for workout_day in workout:
        lines.append(f"- {workout_day}")

    return "\n".join(lines)


def save_final_report(report_text: str) -> None:
    """Persist final report text to output path."""
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_FILE.open("w", encoding="utf-8") as file:
        file.write(report_text)
