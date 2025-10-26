import json
from typing import Any, Dict


def safe_json_loads(data: str, default: Any = None) -> Any:
    """Safely load JSON data, returning default if parsing fails."""
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(data: Any, default: str = "{}") -> str:
    """Safely dump data to JSON string."""
    try:
        return json.dumps(data)
    except (TypeError, ValueError):
        return default
