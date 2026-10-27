"""
SQLite connection management and in-memory cache for ShadowPlayer AI.
All data is synthetic and fictional.
"""
import json
import logging
import os
import sqlite3
from pathlib import Path

logger = logging.getLogger("shadowplayer.db")

DB_PATH = Path(os.getenv("DATABASE_PATH", "./data/match.db"))

# In-memory cache populated at startup — avoids repeated DB reads
_cache: dict = {}


def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection with Row factory."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables from schema.sql if they don't exist yet."""
    schema_path = Path(__file__).parent / "schema.sql"
    with get_connection() as conn:
        conn.execute("PRAGMA journal_mode=DELETE")
        conn.executescript(schema_path.read_text())
    logger.info("Database initialised at %s", DB_PATH)


def is_seeded() -> bool:
    """Return True if at least one match exists."""
    try:
        with get_connection() as conn:
            row = conn.execute("SELECT COUNT(*) FROM matches").fetchone()
            return row[0] > 0
    except Exception:
        return False


def get_cache() -> dict:
    """Return the in-memory cache."""
    return _cache


def populate_cache() -> None:
    """
    Load all match, sequence, and player analytics data into _cache.
    Structure:
      _cache["matches"]          -> list of match summary dicts
      _cache["match_detail"]     -> {match_id: MatchDetail dict}
      _cache["sequences"]        -> {sequence_id: SequenceDetail dict}
      _cache["profiles"]         -> {(player_id, match_id): ShadowProfile dict}
      _cache["counterfactuals"]  -> {(sequence_id, cf_type): CounterfactualResult dict}
    """
    global _cache
    _cache = {
        "matches": [],
        "match_detail": {},
        "sequences": {},
        "profiles": {},
        "counterfactuals": {},
    }
    try:
        with get_connection() as conn:
            # Load match summaries
            for row in conn.execute("SELECT match_id, data_json FROM matches"):
                data = json.loads(row["data_json"])
                _cache["match_detail"][row["match_id"]] = data
                # Build summary
                summary = {
                    "match_id": data["match_id"],
                    "home_team": data["home_team"],
                    "away_team": data["away_team"],
                    "duration_seconds": data["duration_seconds"],
                    "generated_at": data["generated_at"],
                    "data_label": "SYNTHETIC MATCH — FICTIONAL",
                }
                _cache["matches"].append(summary)

            # Load sequences
            for row in conn.execute("SELECT sequence_id, data_json FROM sequences"):
                _cache["sequences"][row["sequence_id"]] = json.loads(row["data_json"])

            # Load player analytics
            for row in conn.execute(
                "SELECT player_id, match_id, profile_json FROM player_analytics"
            ):
                key = (row["player_id"], row["match_id"])
                _cache["profiles"][key] = json.loads(row["profile_json"])

            # Load counterfactuals
            for row in conn.execute("SELECT sequence_id, cf_type, data_json FROM counterfactuals"):
                key = (row["sequence_id"], row["cf_type"])
                _cache["counterfactuals"][key] = json.loads(row["data_json"])

        logger.info(
            "Cache populated: %d matches, %d sequences, %d profiles, %d counterfactuals",
            len(_cache["matches"]),
            len(_cache["sequences"]),
            len(_cache["profiles"]),
            len(_cache["counterfactuals"]),
        )
    except Exception as exc:
        logger.error("Cache population failed: %s", exc)


def save_match(match_data: dict) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO matches (match_id, data_json, generated_at, seed) VALUES (?,?,?,?)",
            (match_data["match_id"], json.dumps(match_data),
             match_data["generated_at"], match_data["seed"]),
        )


def save_events(events: list[dict]) -> None:
    with get_connection() as conn:
        conn.executemany(
            "INSERT OR REPLACE INTO events (event_id, match_id, timestamp, event_type, player_id, data_json) "
            "VALUES (?,?,?,?,?,?)",
            [(e["event_id"], e["match_id"], e["timestamp"],
              e["event_type"], e["player_id"], json.dumps(e)) for e in events],
        )


def save_sequence(seq: dict) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO sequences (sequence_id, match_id, data_json) VALUES (?,?,?)",
            (seq["sequence_id"], seq["match_id"], json.dumps(seq)),
        )


def save_player_analytics(player_id: str, match_id: str, sis_data: dict, profile: dict) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO player_analytics "
            "(player_id, match_id, sis, S, P, D, C, confidence, profile_json) VALUES (?,?,?,?,?,?,?,?,?)",
            (player_id, match_id,
             sis_data["sis"], sis_data["S"], sis_data["P"],
             sis_data["D"], sis_data["C"], sis_data["confidence"],
             json.dumps(profile)),
        )


def save_counterfactual(sequence_id: str, cf_type: str, data: dict) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO counterfactuals (sequence_id, cf_type, data_json) VALUES (?,?,?)",
            (sequence_id, cf_type, json.dumps(data)),
        )
