"""Utilities for local SLM calls through Ollama."""

import json
from urllib import error, request


def _extract_json_object(raw_text: str) -> dict:
    """Extract and parse the first JSON object found in text."""
    text = raw_text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to recover when model wraps JSON with extra text.
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("Model output does not contain a JSON object.") from None
        return json.loads(text[start : end + 1])


def call_ollama_json(
    prompt: str, model: str = "llama3:8b", host: str = "http://localhost:11434"
) -> dict:
    """Call Ollama and parse response as JSON object."""
    url = f"{host}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=90) as response:
            response_data = json.loads(response.read().decode("utf-8"))
    except error.URLError as exc:
        raise RuntimeError(
            "Could not connect to Ollama. Start Ollama and ensure a model is pulled."
        ) from exc

    model_text = response_data.get("response", "").strip()
    if not model_text:
        raise ValueError("Ollama returned an empty response.")
    return _extract_json_object(model_text)

