"""Calorie & Nutrition Agent implementation."""

from shared.agent_logging import log_agent_activity
from shared.app_state import AppState
from shared.llm_tools import call_ollama_json


def run_nutrition_agent(state: AppState, model: str) -> None:
    """Calculate calorie target and macros from profile data."""
    agent_name = "Calorie & Nutrition Agent"
    log_agent_activity(agent_name, "START", "Execution started")
    try:
        if not state.profile:
            raise ValueError("Profile data is missing. Run Fitness Profile Agent first.")

        log_agent_activity(agent_name, "INPUT", state.profile)
        profile = state.profile

        prompt = f"""
You are a nutrition planning agent.
Create daily calorie target and macros for the user profile.
Use realistic fitness guidance and keep values practical.
Return ONLY valid JSON with integer fields:
- daily_calories
- protein_g
- carbs_g
- fats_g

Input profile:
{profile}
"""
        llm_json = call_ollama_json(prompt=prompt, model=model)

        state.nutrition = {
            "daily_calories": int(llm_json["daily_calories"]),
            "protein_g": int(llm_json["protein_g"]),
            "carbs_g": int(llm_json["carbs_g"]),
            "fats_g": int(llm_json["fats_g"]),
        }
        log_agent_activity(agent_name, "OUTPUT", state.nutrition)
        log_agent_activity(agent_name, "END", "Execution completed")
    except Exception as error:  # noqa: BLE001 - required for agent error logging
        log_agent_activity(agent_name, "ERROR", str(error))
        raise
