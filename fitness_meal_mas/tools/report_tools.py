"""Logging, workout, and reporting tool functions."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

LOG_FILE = Path(__file__).resolve().parents[1] / "logs" / "agent_logs.txt"
REPORT_FILE = Path(__file__).resolve().parents[1] / "outputs" / "final_report.txt"


def log_agent_activity(agent_name: str, data_type: str, payload: Any) -> None:
    """Append timestamped agent input/output logs."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rendered_payload = payload
    if isinstance(payload, (dict, list, tuple)):
        rendered_payload = json.dumps(payload, ensure_ascii=True, sort_keys=True)
    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] [{agent_name}] [{data_type}] {rendered_payload}\n")


def generate_workout_plan(goal: str) -> list[str]:
    """Return a simple 7-day workout schedule based on goal."""
    if goal == "lose weight":
        return [
            "Day 1: Brisk walk 45 min + core 15 min",
            "Day 2: Full body HIIT 30 min",
            "Day 3: Yoga + mobility 40 min",
            "Day 4: Jogging 35 min + bodyweight circuit",
            "Day 5: Cycling 45 min",
            "Day 6: Strength training (light-moderate) 40 min",
            "Day 7: Active recovery walk 30 min",
        ]
    if goal == "gain muscle":
        return [
            "Day 1: Upper body strength",
            "Day 2: Lower body strength",
            "Day 3: Core + light cardio",
            "Day 4: Push day",
            "Day 5: Pull day",
            "Day 6: Legs + mobility",
            "Day 7: Rest and stretching",
        ]
    return [
        "Day 1: Full body strength 35 min",
        "Day 2: Walk or jog 30 min",
        "Day 3: Yoga 30 min",
        "Day 4: Full body strength 35 min",
        "Day 5: Cycling or brisk walk 30 min",
        "Day 6: Core + mobility 25 min",
        "Day 7: Active recovery",
    ]


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

