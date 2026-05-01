"""Grocery & Workout Plan Agent implementation."""

from state.app_state import AppState
from tools.meal_tools import generate_grocery_list
from tools.llm_tools import call_ollama_json
from tools.report_tools import (
    build_final_report,
    log_agent_activity,
    save_final_report,
)


def run_grocery_workout_agent(state: AppState, model: str) -> str:
    """Create grocery list and workout plan, then save final report."""
    agent_name = "Grocery & Workout Plan Agent"
    log_agent_activity(agent_name, "START", "Execution started")
    try:
        if not state.profile or not state.meal_plan:
            raise ValueError("Required data missing. Run prior agents first.")

        input_payload = {"goal": state.profile["goal"], "meal_plan": state.meal_plan}
        log_agent_activity(agent_name, "INPUT", input_payload)

        prompt = f"""
You are a grocery and workout planning agent.
From the meal plan and goal, generate:
1) grocery_list as a list of concise strings
2) workout_plan as a 7-day list of strings

Return ONLY valid JSON:
{{
  "grocery_list": ["item", "item"],
  "workout_plan": ["Day 1: ...", "Day 2: ...", "... up to Day 7"]
}}

Input:
{input_payload}
"""
        llm_json = call_ollama_json(prompt=prompt, model=model)
        state.grocery_list = [str(x) for x in llm_json.get("grocery_list", [])]
        if not state.grocery_list:
            # Lightweight fallback from existing local tool if model returns empty data.
            state.grocery_list = generate_grocery_list(state.meal_plan)
        state.workout_plan = [str(x) for x in llm_json.get("workout_plan", [])][:7]
        if len(state.workout_plan) < 7:
            raise ValueError("SLM did not return a complete 7-day workout plan.")

        report_text = build_final_report(
            {
                "profile": state.profile,
                "nutrition": state.nutrition,
                "meal_plan": state.meal_plan,
                "grocery_list": state.grocery_list,
                "workout_plan": state.workout_plan,
            }
        )
        save_final_report(report_text)

        output_payload = {
            "grocery_list_count": len(state.grocery_list),
            "workout_days": len(state.workout_plan),
            "report_saved": "outputs/final_report.txt",
        }
        log_agent_activity(agent_name, "OUTPUT", output_payload)
        log_agent_activity(agent_name, "END", "Execution completed")
        return report_text
    except Exception as error:  # noqa: BLE001 - required for agent error logging
        log_agent_activity(agent_name, "ERROR", str(error))
        raise

