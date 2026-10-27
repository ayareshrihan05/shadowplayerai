export interface PlayerPosition {
  player_id: string;
  x: number;
  y: number;
  vx: number;
  vy: number;
  speed: number;
  is_in_possession: boolean;
}

export interface BallState {
  x: number;
  y: number;
  vx: number;
  vy: number;
  z: number;
  speed: number;
}

export interface PassingLane {
  from_player: string;
  to_player: string;
  blocked: boolean;
  width: number;
  length: number;
}

export interface OpenSpaceZone {
  x: number;
  y: number;
  radius: number;
}

export interface FrameData {
  t: number;
  players: PlayerPosition[];
  ball: BallState;
  passing_lanes: PassingLane[];
  open_space_zones: OpenSpaceZone[];
}

export interface PlayerRecord {
  player_id: string;
  name: string;
  team_id: string;
  position: string;
  jersey_number: number;
  is_fictional: boolean;
}

export interface TeamRecord {
  team_id: string;
  name: string;
  formation: string;
  players: PlayerRecord[];
}

export interface SISLeaderboardEntry {
  player_id: string;
  name: string;
  position: string;
  sis: number;
  confidence: number;
}

export interface MatchSummary {
  match_id: string;
  home_team: TeamRecord;
  away_team: TeamRecord;
  duration_seconds: number;
  generated_at: string;
  data_label: string;
}

export interface MatchDetail {
  match_id: string;
  home_team: TeamRecord;
  away_team: TeamRecord;
  duration_seconds: number;
  event_count: number;
  frame_count: number;
  scenario_count: number;
  sis_leaderboard: SISLeaderboardEntry[];
}

export interface TeamSISSummary {
  avg_sis: number;
  top_player: string;
}

export interface MatchInsights {
  match_id: string;
  top_off_ball_contributors: SISLeaderboardEntry[];
  notable_sequences: Array<{
    sequence_id: string;
    name: string;
    focus_player_id: string;
    timestamp_start: number;
    timestamp_end: number;
    ai_summary: string;
  }>;
  team_sis_summary: Record<string, TeamSISSummary>;
}
