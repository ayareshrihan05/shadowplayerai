-- ShadowPlayer AI — SQLite Schema
-- All data stored is synthetic and fictional.

CREATE TABLE IF NOT EXISTS matches (
    match_id    TEXT PRIMARY KEY,
    data_json   TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    seed        INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    event_id    TEXT PRIMARY KEY,
    match_id    TEXT NOT NULL,
    timestamp   REAL NOT NULL,
    event_type  TEXT NOT NULL,
    player_id   TEXT NOT NULL,
    data_json   TEXT NOT NULL,
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

CREATE TABLE IF NOT EXISTS sequences (
    sequence_id TEXT PRIMARY KEY,
    match_id    TEXT NOT NULL,
    data_json   TEXT NOT NULL,
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

CREATE TABLE IF NOT EXISTS player_analytics (
    player_id   TEXT NOT NULL,
    match_id    TEXT NOT NULL,
    sis         REAL NOT NULL,
    S           REAL NOT NULL,
    P           REAL NOT NULL,
    D           REAL NOT NULL,
    C           REAL NOT NULL,
    confidence  REAL NOT NULL,
    profile_json TEXT NOT NULL,
    PRIMARY KEY (player_id, match_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

CREATE TABLE IF NOT EXISTS counterfactuals (
    sequence_id TEXT NOT NULL,
    cf_type     TEXT NOT NULL,
    data_json   TEXT NOT NULL,
    PRIMARY KEY (sequence_id, cf_type)
);

CREATE TABLE IF NOT EXISTS scouting_reports (
    report_id       TEXT PRIMARY KEY,
    player_id       TEXT NOT NULL,
    match_id        TEXT NOT NULL,
    tier            TEXT NOT NULL,
    report_json     TEXT NOT NULL,
    generation_method TEXT NOT NULL,
    generated_at    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_events_match ON events(match_id);
CREATE INDEX IF NOT EXISTS idx_events_player ON events(player_id);
CREATE INDEX IF NOT EXISTS idx_sequences_match ON sequences(match_id);
