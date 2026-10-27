"""
Pre-designed tactical scenarios for ShadowPlayer AI.
All coordinates, players, and events are synthetic and fictional.

These scenarios are hand-authored to guarantee detectable off-ball actions.
Matches are strictly segregated by gender:
  - match-men-001 (Men's Premier League: Northvale FC vs Eastmere City)
  - match-women-001 (Women's Super League: Northvale FC Women vs Eastmere City Women)

Coordinate system: (0,0) = bottom-left, (105,68) = top-right, meters.
Home teams attack left-to-right (increasing x).
"""
from __future__ import annotations

# ─── MEN'S DIVISION ROSTERS ──────────────────────────────────────────────────

MEN_HOME_TEAM = {
    "team_id": "team-northvale-fc",
    "name": "Northvale FC [FICTIONAL]",
    "division": "Men's Premier League",
    "formation": "4-3-3",
    "players": [
        {"player_id": "p001", "name": "James Holloway [FICTIONAL]", "team_id": "team-northvale-fc", "position": "ST",  "jersey_number": 9,  "is_fictional": True, "gender": "male"},
        {"player_id": "p002", "name": "Leo Sterling [FICTIONAL]",   "team_id": "team-northvale-fc", "position": "LW",  "jersey_number": 11, "is_fictional": True, "gender": "male"},
        {"player_id": "p003", "name": "Tom Reeves [FICTIONAL]",     "team_id": "team-northvale-fc", "position": "CAM", "jersey_number": 10, "is_fictional": True, "gender": "male"},
        {"player_id": "p004", "name": "Felix Ayo [FICTIONAL]",      "team_id": "team-northvale-fc", "position": "CM",  "jersey_number": 8,  "is_fictional": True, "gender": "male"},
        {"player_id": "p005", "name": "Sam Briggs [FICTIONAL]",     "team_id": "team-northvale-fc", "position": "CM",  "jersey_number": 6,  "is_fictional": True, "gender": "male"},
        {"player_id": "p006", "name": "Yusuf Laine [FICTIONAL]",    "team_id": "team-northvale-fc", "position": "DM",  "jersey_number": 4,  "is_fictional": True, "gender": "male"},
        {"player_id": "p007", "name": "Arthur Davies [FICTIONAL]",  "team_id": "team-northvale-fc", "position": "RB",  "jersey_number": 2,  "is_fictional": True, "gender": "male"},
        {"player_id": "p008", "name": "Dev Kapoor [FICTIONAL]",     "team_id": "team-northvale-fc", "position": "CB",  "jersey_number": 5,  "is_fictional": True, "gender": "male"},
        {"player_id": "p009", "name": "Callum Wright [FICTIONAL]",  "team_id": "team-northvale-fc", "position": "CB",  "jersey_number": 3,  "is_fictional": True, "gender": "male"},
        {"player_id": "p010", "name": "Nathan Cole [FICTIONAL]",    "team_id": "team-northvale-fc", "position": "LB",  "jersey_number": 33, "is_fictional": True, "gender": "male"},
        {"player_id": "p011", "name": "Marcus Webb [FICTIONAL]",    "team_id": "team-northvale-fc", "position": "GK",  "jersey_number": 1,  "is_fictional": True, "gender": "male"},
    ],
}

MEN_AWAY_TEAM = {
    "team_id": "team-eastmere-city",
    "name": "Eastmere City [FICTIONAL]",
    "division": "Men's Premier League",
    "formation": "4-4-2",
    "players": [
        {"player_id": "p012", "name": "Kane Hollis [FICTIONAL]",      "team_id": "team-eastmere-city", "position": "ST",  "jersey_number": 9,  "is_fictional": True, "gender": "male"},
        {"player_id": "p013", "name": "Luke Vance [FICTIONAL]",       "team_id": "team-eastmere-city", "position": "RW",  "jersey_number": 7,  "is_fictional": True, "gender": "male"},
        {"player_id": "p014", "name": "Liam Osei [FICTIONAL]",        "team_id": "team-eastmere-city", "position": "CAM", "jersey_number": 10, "is_fictional": True, "gender": "male"},
        {"player_id": "p015", "name": "Julian Mercer [FICTIONAL]",    "team_id": "team-eastmere-city", "position": "CM",  "jersey_number": 8,  "is_fictional": True, "gender": "male"},
        {"player_id": "p016", "name": "Finn Johansson [FICTIONAL]",   "team_id": "team-eastmere-city", "position": "CM",  "jersey_number": 6,  "is_fictional": True, "gender": "male"},
        {"player_id": "p017", "name": "David Aluko [FICTIONAL]",      "team_id": "team-eastmere-city", "position": "DM",  "jersey_number": 4,  "is_fictional": True, "gender": "male"},
        {"player_id": "p018", "name": "Otto Brandt [FICTIONAL]",      "team_id": "team-eastmere-city", "position": "RB",  "jersey_number": 2,  "is_fictional": True, "gender": "male"},
        {"player_id": "p019", "name": "Sean Fitzpatrick [FICTIONAL]", "team_id": "team-eastmere-city", "position": "CB",  "jersey_number": 5,  "is_fictional": True, "gender": "male"},
        {"player_id": "p020", "name": "Kwame Asante [FICTIONAL]",     "team_id": "team-eastmere-city", "position": "CB",  "jersey_number": 3,  "is_fictional": True, "gender": "male"},
        {"player_id": "p021", "name": "Owen Kelly [FICTIONAL]",       "team_id": "team-eastmere-city", "position": "LB",  "jersey_number": 33, "is_fictional": True, "gender": "male"},
        {"player_id": "p022", "name": "Jake Drummond [FICTIONAL]",    "team_id": "team-eastmere-city", "position": "GK",  "jersey_number": 1,  "is_fictional": True, "gender": "male"},
    ],
}

MEN_ALL_PLAYERS = MEN_HOME_TEAM["players"] + MEN_AWAY_TEAM["players"]

# ─── WOMEN'S DIVISION ROSTERS ────────────────────────────────────────────────

WOMEN_HOME_TEAM = {
    "team_id": "team-northvale-women",
    "name": "Northvale FC Women [FICTIONAL]",
    "division": "Women's Super League",
    "formation": "4-3-3",
    "players": [
        {"player_id": "w001", "name": "Maya Lindqvist [FICTIONAL]",       "team_id": "team-northvale-women", "position": "ST",  "jersey_number": 9,  "is_fictional": True, "gender": "female"},
        {"player_id": "w002", "name": "Mara Okonkwo [FICTIONAL]",         "team_id": "team-northvale-women", "position": "LW",  "jersey_number": 11, "is_fictional": True, "gender": "female"},
        {"player_id": "w003", "name": "Elena Vasquez [FICTIONAL]",        "team_id": "team-northvale-women", "position": "CAM", "jersey_number": 10, "is_fictional": True, "gender": "female"},
        {"player_id": "w004", "name": "Keira Walsh-Sloan [FICTIONAL]",    "team_id": "team-northvale-women", "position": "CM",  "jersey_number": 8,  "is_fictional": True, "gender": "female"},
        {"player_id": "w005", "name": "Hannah Brooks [FICTIONAL]",        "team_id": "team-northvale-women", "position": "CM",  "jersey_number": 6,  "is_fictional": True, "gender": "female"},
        {"player_id": "w006", "name": "Amara Diallo [FICTIONAL]",         "team_id": "team-northvale-women", "position": "DM",  "jersey_number": 4,  "is_fictional": True, "gender": "female"},
        {"player_id": "w007", "name": "Chloe Ndiaye [FICTIONAL]",         "team_id": "team-northvale-women", "position": "RB",  "jersey_number": 2,  "is_fictional": True, "gender": "female"},
        {"player_id": "w008", "name": "Leah Williamson-Park [FICTIONAL]", "team_id": "team-northvale-women", "position": "CB",  "jersey_number": 5,  "is_fictional": True, "gender": "female"},
        {"player_id": "w009", "name": "Aisha Torres [FICTIONAL]",         "team_id": "team-northvale-women", "position": "CB",  "jersey_number": 3,  "is_fictional": True, "gender": "female"},
        {"player_id": "w010", "name": "Rosa Fernandez [FICTIONAL]",       "team_id": "team-northvale-women", "position": "LB",  "jersey_number": 33, "is_fictional": True, "gender": "female"},
        {"player_id": "w011", "name": "Sophie Hampton [FICTIONAL]",       "team_id": "team-northvale-women", "position": "GK",  "jersey_number": 1,  "is_fictional": True, "gender": "female"},
    ],
}

WOMEN_AWAY_TEAM = {
    "team_id": "team-eastmere-women",
    "name": "Eastmere City Women [FICTIONAL]",
    "division": "Women's Super League",
    "formation": "4-4-2",
    "players": [
        {"player_id": "w012", "name": "Bethan Mead-Kelly [FICTIONAL]",   "team_id": "team-eastmere-women", "position": "ST",  "jersey_number": 9,  "is_fictional": True, "gender": "female"},
        {"player_id": "w013", "name": "Priya Menon [FICTIONAL]",         "team_id": "team-eastmere-women", "position": "RW",  "jersey_number": 7,  "is_fictional": True, "gender": "female"},
        {"player_id": "w014", "name": "Grace Hanson [FICTIONAL]",        "team_id": "team-eastmere-women", "position": "CAM", "jersey_number": 10, "is_fictional": True, "gender": "female"},
        {"player_id": "w015", "name": "Zara Chen [FICTIONAL]",           "team_id": "team-eastmere-women", "position": "CM",  "jersey_number": 8,  "is_fictional": True, "gender": "female"},
        {"player_id": "w016", "name": "Millie Brightwell [FICTIONAL]",   "team_id": "team-eastmere-women", "position": "CM",  "jersey_number": 6,  "is_fictional": True, "gender": "female"},
        {"player_id": "w017", "name": "Adaeze Ibe [FICTIONAL]",          "team_id": "team-eastmere-women", "position": "DM",  "jersey_number": 4,  "is_fictional": True, "gender": "female"},
        {"player_id": "w018", "name": "Olivia Vance [FICTIONAL]",        "team_id": "team-eastmere-women", "position": "RB",  "jersey_number": 2,  "is_fictional": True, "gender": "female"},
        {"player_id": "w019", "name": "Leila Farsi [FICTIONAL]",         "team_id": "team-eastmere-women", "position": "CB",  "jersey_number": 5,  "is_fictional": True, "gender": "female"},
        {"player_id": "w020", "name": "Lauren Hemp-Davis [FICTIONAL]",   "team_id": "team-eastmere-women", "position": "CB",  "jersey_number": 3,  "is_fictional": True, "gender": "female"},
        {"player_id": "w021", "name": "Ines Dupont [FICTIONAL]",         "team_id": "team-eastmere-women", "position": "LB",  "jersey_number": 33, "is_fictional": True, "gender": "female"},
        {"player_id": "w022", "name": "Mary Earps-Cole [FICTIONAL]",     "team_id": "team-eastmere-women", "position": "GK",  "jersey_number": 1,  "is_fictional": True, "gender": "female"},
    ],
}

WOMEN_ALL_PLAYERS = WOMEN_HOME_TEAM["players"] + WOMEN_AWAY_TEAM["players"]

# For backward compatibility
HOME_TEAM = MEN_HOME_TEAM
AWAY_TEAM = MEN_AWAY_TEAM
ALL_PLAYERS = MEN_ALL_PLAYERS
TOTAL_ALL_PLAYERS = MEN_ALL_PLAYERS + WOMEN_ALL_PLAYERS

PLAYER_MAP: dict[str, dict] = {p["player_id"]: p for p in TOTAL_ALL_PLAYERS}

# Formation starting positions
FORMATION_POSITIONS: dict[str, tuple[float, float]] = {
    # Home (attacks left to right)
    "001": (78.0, 34.0),  # ST
    "002": (72.0, 58.0),  # LW
    "003": (68.0, 34.0),  # CAM
    "004": (58.0, 42.0),  # CM
    "005": (58.0, 26.0),  # CM
    "006": (48.0, 34.0),  # DM
    "007": (42.0, 10.0),  # RB
    "008": (28.0, 38.0),  # CB
    "009": (28.0, 28.0),  # CB
    "010": (22.0, 58.0),  # LB
    "011": (5.0,  34.0),  # GK
    # Away (attacks right to left)
    "012": (38.0, 38.0),  # ST
    "013": (45.0, 58.0),  # RW
    "014": (48.0, 34.0),  # CAM
    "015": (52.0, 42.0),  # CM
    "016": (52.0, 26.0),  # CM
    "017": (60.0, 34.0),  # DM
    "018": (68.0, 10.0),  # RB
    "019": (76.0, 38.0),  # CB
    "020": (76.0, 28.0),  # CB
    "021": (80.0, 58.0),  # LB
    "022": (100.0, 34.0), # GK
}

HOME_FORMATION_POSITIONS = {f"p{k}": v for k, v in FORMATION_POSITIONS.items() if int(k) <= 11}
HOME_FORMATION_POSITIONS.update({f"w{k}": v for k, v in FORMATION_POSITIONS.items() if int(k) <= 11})

AWAY_FORMATION_POSITIONS = {f"p{k}": v for k, v in FORMATION_POSITIONS.items() if int(k) > 11}
AWAY_FORMATION_POSITIONS.update({f"w{k}": v for k, v in FORMATION_POSITIONS.items() if int(k) > 11})

ALL_FORMATION_POSITIONS = {**HOME_FORMATION_POSITIONS, **AWAY_FORMATION_POSITIONS}


# ─── MEN'S SCENARIOS ─────────────────────────────────────────────────────────

# ── SEQ-001: The Decoy Diagonal (Men's Match) ────────────────────────────────
def _build_seq001_frames() -> list[dict]:
    frames = []
    holloway_path = [
        (72.4, 35.2), (73.3, 34.1), (74.4, 33.0), (75.6, 31.8), (76.8, 30.5),
        (77.9, 29.2), (79.0, 28.0), (80.1, 26.8), (80.1, 25.5), (80.1, 25.3),
        (80.1, 25.3), (80.1, 25.3), (80.1, 25.3), (80.1, 25.3), (80.1, 25.3),
    ]
    p020_path = [
        (76.0, 28.0), (76.4, 27.4), (76.8, 26.7), (77.3, 26.0), (77.8, 25.3),
        (78.3, 24.7), (78.7, 24.0), (79.1, 23.5), (79.4, 23.2), (79.4, 23.2),
        (79.4, 23.2), (79.4, 23.2), (79.4, 23.2), (79.4, 23.2), (79.4, 23.2),
    ]
    p009_ball = [(68.1, 34.7)] * 13 + [(68.1, 34.7), (68.1, 34.7)]
    p003_path = [
        (66.0, 34.0), (66.2, 34.0), (66.5, 34.0), (66.8, 34.0), (67.0, 34.1),
        (67.2, 34.1), (67.5, 34.2), (67.8, 34.2), (68.0, 34.3), (68.0, 34.3),
        (68.0, 34.3), (68.0, 34.3), (74.0, 34.5), (76.2, 34.6), (78.0, 34.7),
    ]

    for i in range(15):
        t = 360.0 + i
        hx, hy = holloway_path[i]
        p20x, p20y = p020_path[i]
        p09x, p09y = p009_ball[i]
        p03x, p03y = p003_path[i]

        hvx = (holloway_path[i+1][0] - hx) if i < 8 else 0.0
        hvy = (holloway_path[i+1][1] - hy) if i < 8 else 0.0
        h_speed = (hvx**2 + hvy**2) ** 0.5

        p20_vx = (p020_path[i+1][0] - p20x) if i < 8 else 0.0
        p20_vy = (p020_path[i+1][1] - p20y) if i < 8 else 0.0

        players = [
            {"player_id": "p001", "x": hx,   "y": hy,   "vx": hvx,  "vy": hvy,  "speed": h_speed, "is_in_possession": False},
            {"player_id": "p009", "x": p09x,  "y": p09y, "vx": 0.0,  "vy": 0.0,  "speed": 0.1, "is_in_possession": i < 12},
            {"player_id": "p003", "x": p03x,  "y": p03y, "vx": 0.0,  "vy": 0.0,  "speed": 0.2 if i < 12 else 3.1, "is_in_possession": i >= 12},
            {"player_id": "p020", "x": p20x,  "y": p20y, "vx": p20_vx, "vy": p20_vy, "speed": (p20_vx**2+p20_vy**2)**0.5, "is_in_possession": False},
            {"player_id": "p002", "x": 72.0, "y": 58.0, "vx": 0.0, "vy": 0.0, "speed": 0.5, "is_in_possession": False},
            {"player_id": "p004", "x": 60.0, "y": 42.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "p005", "x": 60.0, "y": 26.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "p006", "x": 50.0, "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "p007", "x": 44.0, "y": 10.0, "vx": 0.0, "vy": 0.0, "speed": 0.4, "is_in_possession": False},
            {"player_id": "p008", "x": 30.0, "y": 38.0, "vx": 0.0, "vy": 0.0, "speed": 0.1, "is_in_possession": False},
            {"player_id": "p010", "x": 24.0, "y": 58.0, "vx": 0.0, "vy": 0.0, "speed": 0.4, "is_in_possession": False},
            {"player_id": "p011", "x": 5.0,  "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.0, "is_in_possession": False},
            {"player_id": "p012", "x": 40.0, "y": 38.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "p013", "x": 45.0, "y": 58.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "p014", "x": 52.0, "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "p015", "x": 55.0, "y": 42.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "p016", "x": 55.0, "y": 26.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "p017", "x": 62.0, "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "p018", "x": 70.0, "y": 10.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "p019", "x": 78.0, "y": 38.0, "vx": 0.0, "vy": 0.0, "speed": 0.1, "is_in_possession": False},
            {"player_id": "p021", "x": 82.0, "y": 58.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "p022", "x": 100.0,"y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.0, "is_in_possession": False},
        ]

        central_lane_blocked = i < 3
        passing_lanes = [
            {"from_player": "p009", "to_player": "p003", "blocked": central_lane_blocked, "width": 4.2 if not central_lane_blocked else 0.8, "length": 6.2},
            {"from_player": "p009", "to_player": "p005", "blocked": True, "width": 0.5, "length": 12.0},
        ]
        open_zones = [{"x": 74.0, "y": 30.0, "radius": 4.0 + i * 0.3}] if i >= 3 else []

        frames.append({
            "t": t,
            "players": players,
            "ball": {"x": p09x if i < 12 else p03x, "y": p09y if i < 12 else p03y,
                     "vx": 0.0, "vy": 0.0, "z": 0.0, "speed": 0.0 if i < 12 else 8.5},
            "passing_lanes": passing_lanes,
            "open_space_zones": open_zones,
        })
    return frames


SEQ_001_EVENTS = [
    {
        "event_id": "evt-0142", "match_id": "match-men-001", "timestamp": 360.0,
        "frame_id": "frm-0360", "event_type": "run_start", "player_id": "p001",
        "team_id": "team-northvale-fc", "location": {"x": 72.4, "y": 35.2},
        "metadata": {"initial_location": {"x": 72.4, "y": 35.2}, "run_type": "decoy_diagonal", "trigger_event_id": None},
        "sequence_tags": ["SEQ-001"],
    },
    {
        "event_id": "evt-0147", "match_id": "match-men-001", "timestamp": 363.0,
        "frame_id": "frm-0363", "event_type": "change_direction", "player_id": "p020",
        "team_id": "team-eastmere-city", "location": {"x": 77.3, "y": 26.0},
        "metadata": {"response_to": "p001", "direction": "toward_player"},
        "sequence_tags": ["SEQ-001"],
    },
    {
        "event_id": "evt-0153", "match_id": "match-men-001", "timestamp": 372.0,
        "frame_id": "frm-0372", "event_type": "pass", "player_id": "p009",
        "team_id": "team-northvale-fc", "location": {"x": 68.1, "y": 34.7},
        "metadata": {
            "target_player_id": "p003", "target_location": {"x": 78.0, "y": 34.7},
            "outcome": "complete", "pass_length": 10.1, "is_forward": True, "pressure_applied": False,
        },
        "sequence_tags": ["SEQ-001"],
    },
    {
        "event_id": "evt-0158", "match_id": "match-men-001", "timestamp": 374.0,
        "frame_id": "frm-0374", "event_type": "run_end", "player_id": "p001",
        "team_id": "team-northvale-fc", "location": {"x": 80.1, "y": 25.3},
        "metadata": {"final_location": {"x": 80.1, "y": 25.3}, "distance": 12.4, "duration": 14.0, "received_ball": False},
        "sequence_tags": ["SEQ-001"],
    },
]

SCENARIO_DECOY_DIAGONAL = {
    "sequence_id": "SEQ-001",
    "name": "The Decoy Diagonal",
    "match_id": "match-men-001",
    "focus_player_id": "p001",
    "timestamp_start": 360.0,
    "timestamp_end": 375.0,
    "frames": _build_seq001_frames(),
    "key_events": ["evt-0142", "evt-0147", "evt-0153"],
    "movement_detections": [
        {
            "movement_id": "mov-001",
            "player_id": "p001",
            "movement_type": "decoy_diagonal",
            "timestamp_start": 360.0,
            "timestamp_end": 368.0,
            "confidence": 0.88,
            "confidence_label": "high",
            "evidence_event_ids": ["evt-0142", "evt-0147"],
            "evidence_frame_ids": ["frm-0360", "frm-0363", "frm-0366"],
            "criteria_met": {
                "speed_threshold": True,
                "opponent_response": True,
                "no_ball_received": True,
                "min_distance": True,
                "diagonal_angle": True,
            },
            "sis_components": {"S": 72.4, "P": 61.0, "D": 0.0, "C": 65.7},
        }
    ],
    "ai_explanation": {
        "text": (
            "Holloway's diagonal run (evt-0142) pulled the opposing centre-back Kwame Asante "
            "4.3 meters from the central channel over 8 seconds, creating a passing lane "
            "with 4.2m of unobstructed space (up from 0.8m at sequence start). "
            "Teammate Tom Reeves (p003) exploited this opening to receive the through ball "
            "(evt-0153) 12 seconds after the run began. "
            "Space Creation Score: 72.4. Confidence: 0.88 (high)."
        ),
        "evidence_refs": ["evt-0142", "evt-0147", "evt-0153", "mov-001"],
        "generation_method": "fallback_template",
        "disclaimer": "Based on synthetic data and experimental metrics. All players and events are fictional.",
    },
}

# ── SEQ-003: The Press Cascade (Men's Match) ─────────────────────────────────
def _build_seq003_frames() -> list[dict]:
    frames = []
    ayo_path = [
        (58.0, 34.0), (59.5, 34.1), (61.2, 34.2), (63.1, 34.3), (64.8, 34.2),
        (66.2, 34.1), (67.3, 34.0), (67.8, 34.0), (67.8, 34.0), (67.8, 34.0),
        (67.0, 34.0), (65.5, 34.0), (64.0, 34.0), (63.0, 34.0), (62.0, 34.0),
        (61.0, 34.0), (60.0, 34.0), (60.0, 34.0),
    ]
    p017_path = [
        (62.0, 34.0), (61.8, 34.0), (61.5, 34.0), (61.2, 34.0), (61.0, 34.0),
        (60.8, 34.0), (60.5, 34.0), (59.0, 34.0),
        (59.0, 34.0), (59.0, 34.0), (59.0, 34.0), (59.0, 34.0), (59.0, 34.0),
        (59.0, 34.0), (59.0, 34.0), (59.0, 34.0), (59.0, 34.0), (59.0, 34.0),
    ]
    laine_path = [
        (47.0, 34.0), (47.3, 34.0), (47.8, 34.1), (48.5, 34.1), (49.5, 34.2),
        (51.0, 34.2), (52.8, 34.3), (54.5, 34.3), (55.5, 34.3), (56.0, 34.3),
        (57.0, 34.2), (58.2, 34.2), (59.0, 34.2), (59.0, 34.0), (59.5, 33.8),
        (61.0, 33.5), (63.0, 33.2), (65.0, 33.0),
    ]

    for i in range(18):
        t = 4330.0 + i
        ax, ay = ayo_path[i]
        p17x, p17y = p017_path[i]
        lx, ly = laine_path[i]

        avx = (ayo_path[i+1][0] - ax) if i < 7 else 0.0
        avy = (ayo_path[i+1][1] - ay) if i < 7 else 0.0
        a_speed = (avx**2 + avy**2) ** 0.5

        lvx = (laine_path[i+1][0] - lx) if i < 14 else 2.0
        lvy = (laine_path[i+1][1] - ly) if i < 14 else -0.2
        l_speed = (lvx**2 + lvy**2) ** 0.5

        eastmere_has_ball = i < 7

        players = [
            {"player_id": "p004", "x": ax,   "y": ay,   "vx": avx, "vy": avy, "speed": a_speed, "is_in_possession": False},
            {"player_id": "p006", "x": lx,   "y": ly,   "vx": lvx, "vy": lvy, "speed": l_speed, "is_in_possession": i >= 14},
            {"player_id": "p017", "x": p17x, "y": p17y, "vx": -0.3, "vy": 0.0, "speed": 0.3, "is_in_possession": eastmere_has_ball},
            {"player_id": "p001", "x": 78.0, "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "p002", "x": 72.0, "y": 55.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "p003", "x": 68.0, "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "p005", "x": 60.0, "y": 26.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "p007", "x": 44.0, "y": 10.0, "vx": 0.0, "vy": 0.0, "speed": 0.4, "is_in_possession": False},
            {"player_id": "p008", "x": 30.0, "y": 38.0, "vx": 0.0, "vy": 0.0, "speed": 0.1, "is_in_possession": False},
            {"player_id": "p009", "x": 28.0, "y": 28.0, "vx": 0.0, "vy": 0.0, "speed": 0.1, "is_in_possession": False},
            {"player_id": "p010", "x": 38.0, "y": 55.0, "vx": 0.0, "vy": 0.0, "speed": 0.4, "is_in_possession": False},
            {"player_id": "p011", "x": 5.0,  "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.0, "is_in_possession": False},
            {"player_id": "p012", "x": 38.0, "y": 36.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "p013", "x": 45.0, "y": 58.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "p014", "x": 55.0, "y": 38.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "p015", "x": 57.0, "y": 44.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "p016", "x": 57.0, "y": 24.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "p018", "x": 72.0, "y": 10.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "p019", "x": 76.0, "y": 38.0, "vx": 0.0, "vy": 0.0, "speed": 0.1, "is_in_possession": False},
            {"player_id": "p020", "x": 76.0, "y": 28.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "p021", "x": 80.0, "y": 58.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "p022", "x": 100.0,"y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.0, "is_in_possession": False},
        ]

        pressing_lane_cut = i >= 4
        passing_lanes = [
            {"from_player": "p017", "to_player": "p014", "blocked": pressing_lane_cut, "width": 0.6 if pressing_lane_cut else 3.2, "length": 7.0},
            {"from_player": "p017", "to_player": "p016", "blocked": True, "width": 0.4, "length": 5.0},
        ]
        open_zones = [{"x": 55.0, "y": 34.0, "radius": 4.0}] if i >= 14 else []

        frames.append({
            "t": t,
            "players": players,
            "ball": {
                "x": p17x if eastmere_has_ball else lx,
                "y": p17y if eastmere_has_ball else ly,
                "vx": 0.0, "vy": 0.0, "z": 0.0,
                "speed": 0.0 if i != 7 else 6.0,
            },
            "passing_lanes": passing_lanes,
            "open_space_zones": open_zones,
        })
    return frames


SEQ_003_EVENTS = [
    {
        "event_id": "evt-0410", "match_id": "match-men-001", "timestamp": 4330.0,
        "frame_id": "frm-4330", "event_type": "press_start", "player_id": "p004",
        "team_id": "team-northvale-fc", "location": {"x": 58.0, "y": 34.0},
        "metadata": {"target_player_id": "p017", "target_location": {"x": 62.0, "y": 34.0}},
        "sequence_tags": ["SEQ-003"],
    },
    {
        "event_id": "evt-0417", "match_id": "match-men-001", "timestamp": 4337.0,
        "frame_id": "frm-4337", "event_type": "pass", "player_id": "p017",
        "team_id": "team-eastmere-city", "location": {"x": 60.5, "y": 34.0},
        "metadata": {
            "target_player_id": None, "target_location": {"x": 50.0, "y": 34.0},
            "outcome": "intercepted", "pass_length": 10.5, "is_forward": False, "pressure_applied": True,
        },
        "sequence_tags": ["SEQ-003"],
    },
    {
        "event_id": "evt-0418", "match_id": "match-men-001", "timestamp": 4337.5,
        "frame_id": "frm-4337", "event_type": "interception", "player_id": "p006",
        "team_id": "team-northvale-fc", "location": {"x": 55.5, "y": 34.3},
        "metadata": {},
        "sequence_tags": ["SEQ-003"],
    },
    {
        "event_id": "evt-0420", "match_id": "match-men-001", "timestamp": 4344.0,
        "frame_id": "frm-4344", "event_type": "press_end", "player_id": "p004",
        "team_id": "team-northvale-fc", "location": {"x": 67.8, "y": 34.0},
        "metadata": {"outcome": "forced_backward_pass", "duration": 14.0},
        "sequence_tags": ["SEQ-003"],
    },
]

SCENARIO_PRESS_CASCADE = {
    "sequence_id": "SEQ-003",
    "name": "The Press Cascade",
    "match_id": "match-men-001",
    "focus_player_id": "p004",
    "timestamp_start": 4330.0,
    "timestamp_end": 4348.0,
    "frames": _build_seq003_frames(),
    "key_events": ["evt-0410", "evt-0417", "evt-0418"],
    "movement_detections": [
        {
            "movement_id": "mov-003",
            "player_id": "p004",
            "movement_type": "pressing_movement",
            "timestamp_start": 4330.0,
            "timestamp_end": 4337.0,
            "confidence": 0.91,
            "confidence_label": "high",
            "evidence_event_ids": ["evt-0410", "evt-0417", "evt-0418"],
            "evidence_frame_ids": ["frm-4330", "frm-4334", "frm-4337"],
            "criteria_met": {
                "speed_threshold": True,
                "distance_decrease": True,
                "backward_pass_forced": True,
                "possession_changed": True,
            },
            "sis_components": {"S": 22.1, "P": 38.4, "D": 74.6, "C": 68.2},
        }
    ],
    "ai_explanation": {
        "text": (
            "Felix Ayo (p004, CM) pressed Eastmere's DM (p017) at a speed of 3.8 m/s "
            "(evt-0410), closing 9 meters in 7 seconds. His pressing angle cut off "
            "forward passing options, forcing a hurried backward pass intercepted by "
            "Yusuf Laine (p006, evt-0418). "
            "Defensive Support Score: 74.6. Chain Reaction Score: 68.2. Confidence: 0.91 (high)."
        ),
        "evidence_refs": ["evt-0410", "evt-0417", "evt-0418", "mov-003"],
        "generation_method": "fallback_template",
        "disclaimer": "Based on synthetic data and experimental metrics. All players and events are fictional.",
    },
}

MEN_SCENARIOS = [SCENARIO_DECOY_DIAGONAL, SCENARIO_PRESS_CASCADE]
MEN_SCENARIO_EVENTS = SEQ_001_EVENTS + SEQ_003_EVENTS


# ─── WOMEN'S SCENARIOS ───────────────────────────────────────────────────────

# ── SEQ-002: The Overlapping Override (Women's Match) ────────────────────────
def _build_seq002_frames() -> list[dict]:
    frames = []
    rosa_path = [
        (55.0, 60.0), (57.5, 61.2), (60.2, 62.5), (63.0, 63.8), (66.1, 64.8),
        (69.3, 65.5), (72.4, 65.8), (75.0, 65.9), (77.0, 65.8), (78.2, 65.5),
        (79.0, 65.2), (79.5, 64.8), (79.5, 64.5), (79.5, 64.5), (79.5, 64.5),
        (79.5, 64.5), (79.5, 64.5), (79.5, 64.5),
    ]
    w018_path = [
        (70.0, 10.0), (70.0, 10.0), (70.2, 12.0), (70.5, 16.0), (71.0, 20.5),
        (72.0, 25.0), (73.5, 30.0), (74.8, 34.0), (75.5, 38.0), (75.8, 42.0),
        (76.0, 46.0), (76.0, 50.0), (76.0, 54.0), (76.0, 58.0), (76.2, 61.0),
        (76.5, 63.0), (76.5, 64.0), (76.5, 64.5),
    ]
    w002_path = [
        (70.0, 58.0), (70.0, 58.0), (70.0, 58.0), (70.0, 58.0), (70.0, 58.0),
        (69.5, 56.0), (68.8, 53.5), (68.0, 51.0), (67.5, 49.0), (67.0, 47.5),
        (66.8, 46.5), (66.5, 45.8), (66.5, 45.5), (66.5, 45.5), (66.5, 45.5),
        (66.5, 45.5), (66.5, 45.5), (66.5, 45.5),
    ]

    for i in range(18):
        t = 2302.0 + i
        rx, ry = rosa_path[i]
        w18x, w18y = w018_path[i]
        w02x, w02y = w002_path[i]

        rvx = (rosa_path[i+1][0] - rx) if i < 12 else 0.0
        rvy = (rosa_path[i+1][1] - ry) if i < 12 else 0.0
        r_speed = (rvx**2 + rvy**2) ** 0.5

        players = [
            {"player_id": "w010", "x": rx,   "y": ry,   "vx": rvx, "vy": rvy, "speed": r_speed, "is_in_possession": False},
            {"player_id": "w002", "x": w02x, "y": w02y, "vx": 0.0, "vy": -1.5 if i>5 else 0.0, "speed": 1.5 if i>5 else 0.1, "is_in_possession": False},
            {"player_id": "w004", "x": 62.0, "y": 44.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": i<10},
            {"player_id": "w018", "x": w18x, "y": w18y, "vx": 0.0, "vy": 2.0 if i>3 else 0.0, "speed": 2.0 if i>3 else 0.0, "is_in_possession": False},
            {"player_id": "w001", "x": 76.0, "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "w003", "x": 68.0, "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "w005", "x": 55.0, "y": 26.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "w006", "x": 47.0, "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "w007", "x": 44.0, "y": 10.0, "vx": 0.0, "vy": 0.0, "speed": 0.4, "is_in_possession": False},
            {"player_id": "w008", "x": 30.0, "y": 38.0, "vx": 0.0, "vy": 0.0, "speed": 0.1, "is_in_possession": False},
            {"player_id": "w009", "x": 28.0, "y": 28.0, "vx": 0.0, "vy": 0.0, "speed": 0.1, "is_in_possession": False},
            {"player_id": "w011", "x": 5.0,  "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.0, "is_in_possession": False},
            {"player_id": "w012", "x": 36.0, "y": 36.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "w013", "x": 42.0, "y": 58.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "w014", "x": 50.0, "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "w015", "x": 54.0, "y": 42.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "w016", "x": 54.0, "y": 26.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "w017", "x": 60.0, "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "w019", "x": 76.0, "y": 38.0, "vx": 0.0, "vy": 0.0, "speed": 0.1, "is_in_possession": False},
            {"player_id": "w020", "x": 78.0, "y": 28.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "w021", "x": 78.0 + i*0.1, "y": 60.0 - i*0.3, "vx": 0.0, "vy": -0.3, "speed": 0.3, "is_in_possession": False},
            {"player_id": "w022", "x": 100.0,"y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.0, "is_in_possession": False},
        ]

        cross_lane_blocked = i < 8
        passing_lanes = [
            {"from_player": "w004", "to_player": "w010", "blocked": False, "width": 5.0, "length": 22.0},
            {"from_player": "w004", "to_player": "w002", "blocked": cross_lane_blocked, "width": 2.0 if cross_lane_blocked else 5.5, "length": 10.0},
        ]
        open_zones = [{"x": 80.0, "y": 64.0, "radius": 5.0 + i * 0.5}] if i >= 6 else []

        frames.append({
            "t": t,
            "players": players,
            "ball": {"x": 62.0, "y": 44.0, "vx": 0.0, "vy": 0.0, "z": 0.0, "speed": 0.0},
            "passing_lanes": passing_lanes,
            "open_space_zones": open_zones,
        })
    return frames


SEQ_002_EVENTS = [
    {
        "event_id": "evt-0280", "match_id": "match-women-001", "timestamp": 2302.0,
        "frame_id": "frm-2302", "event_type": "run_start", "player_id": "w010",
        "team_id": "team-northvale-women", "location": {"x": 55.0, "y": 60.0},
        "metadata": {"initial_location": {"x": 55.0, "y": 60.0}, "run_type": "overlapping_run", "trigger_event_id": None},
        "sequence_tags": ["SEQ-002"],
    },
    {
        "event_id": "evt-0285", "match_id": "match-women-001", "timestamp": 2306.0,
        "frame_id": "frm-2306", "event_type": "change_direction", "player_id": "w018",
        "team_id": "team-eastmere-women", "location": {"x": 71.0, "y": 20.5},
        "metadata": {"response_to": "w010", "direction": "toward_player"},
        "sequence_tags": ["SEQ-002"],
    },
    {
        "event_id": "evt-0291", "match_id": "match-women-001", "timestamp": 2312.0,
        "frame_id": "frm-2312", "event_type": "pass", "player_id": "w004",
        "team_id": "team-northvale-women", "location": {"x": 62.0, "y": 44.0},
        "metadata": {
            "target_player_id": "w010", "target_location": {"x": 79.5, "y": 65.0},
            "outcome": "complete", "pass_length": 24.2, "is_forward": True, "pressure_applied": False,
        },
        "sequence_tags": ["SEQ-002"],
    },
]

SCENARIO_OVERLAPPING_OVERRIDE = {
    "sequence_id": "SEQ-002",
    "name": "The Overlapping Override",
    "match_id": "match-women-001",
    "focus_player_id": "w010",
    "timestamp_start": 2302.0,
    "timestamp_end": 2320.0,
    "frames": _build_seq002_frames(),
    "key_events": ["evt-0280", "evt-0285", "evt-0291"],
    "movement_detections": [
        {
            "movement_id": "mov-002",
            "player_id": "w010",
            "movement_type": "overlapping_run",
            "timestamp_start": 2302.0,
            "timestamp_end": 2314.0,
            "confidence": 0.82,
            "confidence_label": "high",
            "evidence_event_ids": ["evt-0280", "evt-0285"],
            "evidence_frame_ids": ["frm-2302", "frm-2306", "frm-2310"],
            "criteria_met": {
                "lb_position": True,
                "advanced_beyond_ball": True,
                "toward_byline": True,
                "team_possession": True,
            },
            "sis_components": {"S": 58.3, "P": 71.2, "D": 18.5, "C": 44.1},
        }
    ],
    "ai_explanation": {
        "text": (
            "Rosa Fernandez (w010, LB) advanced 24 meters along the left flank (evt-0280), "
            "surpassing the ball carrier and moving to within 3m of the byline. "
            "This forced Eastmere Women's RB (w018) to track across, creating a wide corridor "
            "that increased passing lane width from 2.0m to 5.5m. Keira Walsh-Sloan (w004) "
            "delivered the overlap pass (evt-0291) 12 seconds after the run began. "
            "Passing Lane Score: 71.2. Space Creation Score: 58.3. Confidence: 0.82 (high)."
        ),
        "evidence_refs": ["evt-0280", "evt-0285", "evt-0291", "mov-002"],
        "generation_method": "fallback_template",
        "disclaimer": "Based on synthetic data and experimental metrics. All players and events are fictional.",
    },
}

# ── SEQ-004: The Blindside Channel Run (Women's Match) ───────────────────────
def _build_seq004_frames() -> list[dict]:
    frames = []
    mara_path = [
        (65.0, 56.0), (67.2, 53.5), (69.8, 50.0), (72.5, 46.2), (75.0, 42.5),
        (77.2, 39.0), (79.0, 36.5), (80.5, 35.0), (81.0, 34.5), (81.0, 34.5),
        (81.0, 34.5), (81.0, 34.5), (81.0, 34.5), (81.0, 34.5), (81.0, 34.5),
    ]
    cb_path = [
        (76.0, 38.0), (76.5, 38.5), (77.2, 39.0), (78.0, 39.2), (78.8, 39.0),
        (79.5, 38.5), (80.0, 37.8), (80.5, 37.0), (80.8, 36.8), (80.8, 36.8),
        (80.8, 36.8), (80.8, 36.8), (80.8, 36.8), (80.8, 36.8), (80.8, 36.8),
    ]

    for i in range(15):
        t = 1410.0 + i
        mx, my = mara_path[i]
        cx, cy = cb_path[i]

        mvx = (mara_path[i+1][0] - mx) if i < 8 else 0.0
        mvy = (mara_path[i+1][1] - my) if i < 8 else 0.0
        m_speed = (mvx**2 + mvy**2) ** 0.5

        players = [
            {"player_id": "w002", "x": mx,   "y": my,   "vx": mvx, "vy": mvy, "speed": m_speed, "is_in_possession": False},
            {"player_id": "w019", "x": cx,   "y": cy,   "vx": 0.0, "vy": 0.0, "speed": 0.8 if i < 8 else 0.1, "is_in_possession": False},
            {"player_id": "w009", "x": 48.0, "y": 30.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": i < 11},
            {"player_id": "w001", "x": 75.0, "y": 28.0 + (i*0.3 if i>6 else 0), "vx": 0.0, "vy": 0.3, "speed": 1.2 if i>6 else 0.2, "is_in_possession": i >= 11},
            {"player_id": "w003", "x": 62.0, "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "w004", "x": 58.0, "y": 44.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "w005", "x": 56.0, "y": 22.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "w006", "x": 44.0, "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "w007", "x": 40.0, "y": 10.0, "vx": 0.0, "vy": 0.0, "speed": 0.4, "is_in_possession": False},
            {"player_id": "w008", "x": 28.0, "y": 38.0, "vx": 0.0, "vy": 0.0, "speed": 0.1, "is_in_possession": False},
            {"player_id": "w010", "x": 35.0, "y": 58.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "w011", "x": 5.0,  "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.0, "is_in_possession": False},
            {"player_id": "w012", "x": 36.0, "y": 36.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "w013", "x": 42.0, "y": 58.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "w014", "x": 50.0, "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "w015", "x": 54.0, "y": 42.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "w016", "x": 54.0, "y": 26.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "w017", "x": 60.0, "y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.3, "is_in_possession": False},
            {"player_id": "w018", "x": 68.0, "y": 10.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "w020", "x": 78.0, "y": 28.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "w021", "x": 80.0, "y": 58.0, "vx": 0.0, "vy": 0.0, "speed": 0.2, "is_in_possession": False},
            {"player_id": "w022", "x": 100.0,"y": 34.0, "vx": 0.0, "vy": 0.0, "speed": 0.0, "is_in_possession": False},
        ]

        lane_open = i >= 4
        passing_lanes = [
            {"from_player": "w009", "to_player": "w001", "blocked": not lane_open, "width": 4.8 if lane_open else 0.9, "length": 27.0},
        ]
        open_zones = [{"x": 75.0, "y": 32.0, "radius": 4.5 + i * 0.4}] if i >= 4 else []

        frames.append({
            "t": t,
            "players": players,
            "ball": {"x": 48.0 if i < 11 else 75.0, "y": 30.0 if i < 11 else 31.0, "vx": 0.0, "vy": 0.0, "z": 0.0, "speed": 0.0 if i < 11 else 9.0},
            "passing_lanes": passing_lanes,
            "open_space_zones": open_zones,
        })
    return frames


SEQ_004_EVENTS = [
    {
        "event_id": "evt-0610", "match_id": "match-women-001", "timestamp": 1410.0,
        "frame_id": "frm-1410", "event_type": "run_start", "player_id": "w002",
        "team_id": "team-northvale-women", "location": {"x": 65.0, "y": 56.0},
        "metadata": {"initial_location": {"x": 65.0, "y": 56.0}, "run_type": "decoy_diagonal", "trigger_event_id": None},
        "sequence_tags": ["SEQ-004"],
    },
    {
        "event_id": "evt-0615", "match_id": "match-women-001", "timestamp": 1414.0,
        "frame_id": "frm-1414", "event_type": "change_direction", "player_id": "w019",
        "team_id": "team-eastmere-women", "location": {"x": 78.0, "y": 39.2},
        "metadata": {"response_to": "w002", "direction": "toward_player"},
        "sequence_tags": ["SEQ-004"],
    },
    {
        "event_id": "evt-0621", "match_id": "match-women-001", "timestamp": 1421.0,
        "frame_id": "frm-1421", "event_type": "pass", "player_id": "w009",
        "team_id": "team-northvale-women", "location": {"x": 48.0, "y": 30.0},
        "metadata": {
            "target_player_id": "w001", "target_location": {"x": 75.0, "y": 31.0},
            "outcome": "complete", "pass_length": 27.0, "is_forward": True, "pressure_applied": False,
        },
        "sequence_tags": ["SEQ-004"],
    },
]

SCENARIO_BLINDSIDE_CHANNEL = {
    "sequence_id": "SEQ-004",
    "name": "The Blindside Channel Run",
    "match_id": "match-women-001",
    "focus_player_id": "w002",
    "timestamp_start": 1410.0,
    "timestamp_end": 1425.0,
    "frames": _build_seq004_frames(),
    "key_events": ["evt-0610", "evt-0615", "evt-0621"],
    "movement_detections": [
        {
            "movement_id": "mov-004",
            "player_id": "w002",
            "movement_type": "decoy_diagonal",
            "timestamp_start": 1410.0,
            "timestamp_end": 1418.0,
            "confidence": 0.89,
            "confidence_label": "high",
            "evidence_event_ids": ["evt-0610", "evt-0615"],
            "evidence_frame_ids": ["frm-1410", "frm-1414", "frm-1418"],
            "criteria_met": {
                "speed_threshold": True,
                "opponent_response": True,
                "no_ball_received": True,
                "min_distance": True,
                "diagonal_angle": True,
            },
            "sis_components": {"S": 76.5, "P": 68.0, "D": 0.0, "C": 71.2},
        }
    ],
    "ai_explanation": {
        "text": (
            "Mara Okonkwo (w002, LW) made an incisive blindside cut across the central channel "
            "(evt-0610), drawing Eastmere CB Leila Farsi (w019) out of position by 5.2 meters. "
            "This opened up a 27-meter passing lane for Aisha Torres (w009) to find striker Maya Lindqvist (w001), "
            "directly leading to an uncontested strike on target (evt-0621). "
            "Space Creation Score: 76.5. Chain Reaction Score: 71.2. Confidence: 0.89 (high)."
        ),
        "evidence_refs": ["evt-0610", "evt-0615", "evt-0621", "mov-004"],
        "generation_method": "fallback_template",
        "disclaimer": "Based on synthetic data and experimental metrics. All players and events are fictional.",
    },
}

WOMEN_SCENARIOS = [SCENARIO_OVERLAPPING_OVERRIDE, SCENARIO_BLINDSIDE_CHANNEL]
WOMEN_SCENARIO_EVENTS = SEQ_002_EVENTS + SEQ_004_EVENTS

ALL_SCENARIOS = MEN_SCENARIOS + WOMEN_SCENARIOS
ALL_SCENARIO_EVENTS = MEN_SCENARIO_EVENTS + WOMEN_SCENARIO_EVENTS
