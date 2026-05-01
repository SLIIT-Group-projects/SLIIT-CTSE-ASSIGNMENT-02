"""Meal Plan Generator Agent implementation."""

from state.app_state import AppState
from tools.llm_tools import call_ollama_json
from tools.report_tools import log_agent_activity


def run_meal_plan_agent(state: AppState, model: str) -> None:
    """Generate allergy-aware meal options and store in state."""
    agent_name = "Meal Plan Generator Agent"
    log_agent_activity(agent_name, "START", "Execution started")
    try:
        if not state.profile or not state.nutrition:
            raise ValueError(
                "Required data missing. Run Fitness Profile and Nutrition agents first."
            )

        payload = {
            "diet_type": state.profile["diet_type"],
            "allergies": state.profile["allergies"],
            "nutrition_targets": state.nutrition,
        }
        log_agent_activity(agent_name, "INPUT", payload)

        prompt = f"""
You are a meal plan generation agent.
Generate 2 options each for breakfast, lunch, snack, and dinner.
Respect diet type and avoid allergic ingredients.
Return ONLY valid JSON with this structure:
{{
  "breakfast": ["item1", "item2"],
  "lunch": ["item1", "item2"],
  "snack": ["item1", "item2"],
  "dinner": ["item1", "item2"]
}}

Input:
{payload}
"""
        llm_json = call_ollama_json(prompt=prompt, model=model)
        state.meal_plan = {
            "breakfast": [str(x) for x in llm_json["breakfast"]][:2],
            "lunch": [str(x) for x in llm_json["lunch"]][:2],
            "snack": [str(x) for x in llm_json["snack"]][:2],
            "dinner": [str(x) for x in llm_json["dinner"]][:2],
        }
        log_agent_activity(agent_name, "OUTPUT", state.meal_plan)
        log_agent_activity(agent_name, "END", "Execution completed")
    except Exception as error:  # noqa: BLE001 - required for agent error logging
        log_agent_activity(agent_name, "ERROR", str(error))
        raise

