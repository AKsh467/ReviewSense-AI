"""
ReviewSense AI — History Manager
Provides reliable local persistence for analysis runs using JSON storage.
"""

import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from config import HISTORY_FILE


def _read_raw_history() -> List[Dict[str, Any]]:
    """Read history list from disk safely."""
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        return []


def _write_raw_history(entries: List[Dict[str, Any]]) -> bool:
    """Save history entries to disk atomically."""
    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def get_all_history() -> List[Dict[str, Any]]:
    """Return all saved analysis entries sorted by timestamp descending."""
    entries = _read_raw_history()
    entries.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return entries


def save_history_entry(
    source_name: str,
    review_count: int,
    reviews: List[str],
    result: Dict[str, Any],
    model_name: str = "Unknown",
    is_demo: bool = False,
) -> str:
    """Save a new analysis entry and return its unique identifier."""
    entries = _read_raw_history()
    entry_id = str(uuid.uuid4())[:8]
    now = datetime.now()
    
    overall_sentiment = (
        result.get("overall_sentiment", {}).get("classification", "Unknown")
        if isinstance(result.get("overall_sentiment"), dict)
        else "Unknown"
    )

    new_record = {
        "id": entry_id,
        "title": source_name,
        "created_at": now.isoformat(),
        "display_time": now.strftime("%b %d, %Y • %I:%M %p"),
        "review_count": review_count,
        "overall_sentiment": overall_sentiment,
        "model_name": model_name,
        "is_demo": is_demo,
        "reviews": reviews,
        "result": result,
    }

    entries.insert(0, new_record)
    # Cap stored history to 50 most recent records to maintain snappy performance
    if len(entries) > 50:
        entries = entries[:50]
    _write_raw_history(entries)
    return entry_id


def get_history_entry(entry_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a single history entry by its ID."""
    entries = _read_raw_history()
    for entry in entries:
        if entry.get("id") == entry_id:
            return entry
    return None


def delete_history_entry(entry_id: str) -> bool:
    """Delete a single history entry by its ID."""
    entries = _read_raw_history()
    filtered = [e for e in entries if e.get("id") != entry_id]
    if len(filtered) != len(entries):
        return _write_raw_history(filtered)
    return False


def clear_all_history() -> bool:
    """Clear all analysis history entries."""
    return _write_raw_history([])
