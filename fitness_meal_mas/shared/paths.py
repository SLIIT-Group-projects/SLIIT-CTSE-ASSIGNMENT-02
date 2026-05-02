"""Project root paths for logs and outputs."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT_ROOT / "logs" / "agent_logs.txt"
REPORT_FILE = PROJECT_ROOT / "outputs" / "final_report.txt"
