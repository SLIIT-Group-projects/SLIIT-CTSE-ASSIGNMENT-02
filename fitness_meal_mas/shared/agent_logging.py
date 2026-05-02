"""Timestamped pipeline logging shared by all agents."""

import json
from datetime import datetime
from typing import Any

from shared.paths import LOG_FILE


def log_agent_activity(agent_name: str, data_type: str, payload: Any) -> None:
    """Append timestamped agent input/output logs."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rendered_payload = payload
    if isinstance(payload, (dict, list, tuple)):
        rendered_payload = json.dumps(payload, ensure_ascii=True, sort_keys=True)
    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] [{agent_name}] [{data_type}] {rendered_payload}\n")
