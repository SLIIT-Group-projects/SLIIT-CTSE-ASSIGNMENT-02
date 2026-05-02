"""Fitness Profile Agent implementation."""

from shared.agent_logging import log_agent_activity
from shared.app_state import AppState
from shared.llm_tools import call_ollama_json

from .fitness_tools import (
    calculate_bmi,
    get_bmi_category,
    normalize_activity,
    normalize_allergies,
    normalize_diet_type,
    normalize_goal,
)


def run_fitness_profile_agent(state: AppState, user_data: dict, model: str) -> None:
    """Process user profile, compute BMI data, and store in shared state."""
    agent_name = "Fitness Profile Agent"
    log_agent_activity(agent_name, "START", "Execution started")
    try:
        log_agent_activity(agent_name, "INPUT", user_data)

        weight_kg = float(user_data["weight_kg"])
        height_cm = float(user_data["height_cm"])
        goal = normalize_goal(user_data["goal"])
        activity_level = normalize_activity(user_data["activity_level"])
        diet_type = normalize_diet_type(user_data["diet_type"])
        allergies = normalize_allergies(user_data["allergies"])

        bmi = calculate_bmi(weight_kg, height_cm)
        prompt = f"""
You are a fitness profiling agent.
Given BMI value and user goal, classify BMI and give one short profile note.
Return ONLY valid JSON with keys:
- bmi_category (string)
- profile_note (string)

Input:
{{
  "bmi": {bmi},
  "goal": "{goal}"
}}
"""
        llm_json = call_ollama_json(prompt=prompt, model=model)
        bmi_category = llm_json.get("bmi_category", get_bmi_category(bmi))
        if bmi_category not in {"Underweight", "Normal weight", "Overweight", "Obese"}:
            bmi_category = get_bmi_category(bmi)
        profile_note = llm_json.get("profile_note", "Maintain a sustainable routine.")

        state.profile = {
            "weight_kg": weight_kg,
            "height_cm": height_cm,
            "goal": goal,
            "activity_level": activity_level,
            "diet_type": diet_type,
            "allergies": allergies,
            "bmi": bmi,
            "bmi_category": bmi_category,
            "profile_note": profile_note,
        }

        log_agent_activity(agent_name, "OUTPUT", state.profile)
        log_agent_activity(agent_name, "END", "Execution completed")
    except Exception as error:  # noqa: BLE001 - required for agent error logging
        log_agent_activity(agent_name, "ERROR", str(error))
        raise
