# AI-Powered Fitness & Meal Planning MAS

A local, rule-based Python CLI Multi-Agent System that generates:
- Fitness profile insights (BMI + category)
- Calorie and macro targets
- Allergy-aware meal plan
- Grocery list and 7-day workout plan

## Project Structure

Individual agents live in numbered folders (agent + domain tools per member). Shared infrastructure (`AppState`, Ollama JSON client, unified log path) sits under `shared/`.

```
fitness_meal_mas/
├── main.py                 # Runs agents 1→2→3→4 in order
├── requirements.txt
├── README.md
├── shared/
│   ├── app_state.py        # Shared blackboard state
│   ├── paths.py            # logs/ and outputs/ paths
│   ├── llm_tools.py        # Ollama JSON calls (all agents)
│   └── agent_logging.py    # Timestamped agent_logs.txt
├── agent_01_fitness_profile/
│   ├── agent.py
│   └── fitness_tools.py
├── agent_02_nutrition/
│   ├── agent.py
│   └── nutrition_tools.py
├── agent_03_meal_plan/
│   ├── agent.py
│   └── meal_plan_tools.py
├── agent_04_grocery_workout/
│   ├── agent.py
│   ├── grocery_tools.py
│   └── report_tools.py
├── logs/
├── outputs/
└── tests/
```

## Requirements

- Python 3.10+
- Ollama installed and running locally
- A local Small Language Model (SLM), e.g. `llama3:8b`, `phi3`, `qwen`
- No external APIs
- No OpenAI usage

## Setup

From your project root:

```bash
cd fitness_meal_mas
python -m venv .venv
```

Activate the virtual environment:

- **Windows (PowerShell)**:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **macOS/Linux**:
  ```bash
  source .venv/bin/activate
  ```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install/pull a local SLM with Ollama:

```bash
ollama pull llama3:8b
```

## Run the CLI

```bash
python main.py
```

When prompted, provide your local model name (or press Enter for default).

## Run Tests

```bash
python -m unittest tests/test_tools.py -v
```

## Agent Flow

1. **Fitness Profile Agent**
   - Inputs: weight, height, goal, activity level, diet type, allergies
   - Computes BMI + BMI category
   - Saves profile data to shared state

2. **Calorie & Nutrition Agent**
   - Uses profile data
   - Computes daily calories and macros (protein/carbs/fats)
   - Saves nutrition data to shared state

3. **Meal Plan Generator Agent**
   - Uses nutrition targets + diet type + allergies
   - Generates breakfast, lunch, snack, dinner options
   - Avoids meals matching allergens
   - Saves meal plan to shared state

4. **Grocery & Workout Plan Agent**
   - Uses meal plan + goal
   - Generates grocery list + 7-day workout plan
   - Saves final report to `outputs/final_report.txt`

## Logs and Output

- Agent execution logs: `logs/agent_logs.txt`
- Final report: `outputs/final_report.txt`

## Sample CLI Input

```text
Weight: 70
Height: 175
Goal: maintain
Activity level: moderate
Diet type: vegetarian
Allergies: none
```

## Sample Report Output (Excerpt)

```text
AI-Powered Fitness & Meal Planning MAS
FINAL PERSONALIZED REPORT
==============================================================

[1] FITNESS PROFILE
--------------------------------------------------------------
Weight (kg)       : 70.0
Height (cm)       : 175.0
Goal              : maintain
Activity Level    : moderate
Diet Type         : vegetarian
Allergies         : None
BMI               : 22.86
BMI Category      : Normal weight
```

