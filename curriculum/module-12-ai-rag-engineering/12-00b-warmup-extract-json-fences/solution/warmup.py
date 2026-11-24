import json


def parse_llm_json(raw: str) -> dict[str, object]:
    """Extract first-to-last {...} JSON object from a noisy LLM response."""
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("No JSON object found")
    return dict(json.loads(raw[start : end + 1]))
