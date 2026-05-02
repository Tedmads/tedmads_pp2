import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")


def _load_rows():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _save_rows(rows):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


def init_db():
    """Compatibility shim: initialize JSON storage."""
    if not os.path.exists(LEADERBOARD_FILE):
        _save_rows([])
    return True


def get_or_create_player(username):
    """Compatibility shim for old DB API."""
    return username


def save_session(username, score, level_reached):
    """Save one game session to leaderboard.json."""
    rows = _load_rows()
    rows.append(
        {
            "username": str(username),
            "score": int(score),
            "level_reached": int(level_reached),
            "played_at": datetime.now().strftime("%Y-%m-%d"),
        }
    )
    _save_rows(rows)


def get_top10():
    """Return list of (rank, username, score, level, date) for top 10."""
    rows = _load_rows()
    rows.sort(key=lambda r: int(r.get("score", 0)), reverse=True)
    top = rows[:10]
    return [
        (
            i + 1,
            r.get("username", "Unknown"),
            int(r.get("score", 0)),
            int(r.get("level_reached", 1)),
            r.get("played_at", "---- -- --"),
        )
        for i, r in enumerate(top)
    ]


def get_personal_best(username):
    """Return the player's highest score, or 0 if none."""
    rows = _load_rows()
    best = 0
    for r in rows:
        if r.get("username") == username:
            best = max(best, int(r.get("score", 0)))
    return best
