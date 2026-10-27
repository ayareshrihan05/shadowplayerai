export interface ConventionalStats {
  goals: number;
  assists: number;
  shots: number;
  passes_completed: number;
}

export interface SISBreakdown {
  space_creation_score: number;
  passing_lane_score: number;
  defensive_support_score: number;
  chain_reaction_score: number;
  sis: number;
  confidence: number;
  label: string;
}

export interface SequenceSummary {
  sequence_id: string;
  name: string;
  timestamp_start: number;
  timestamp_end: number;
  movement_type: string;
  sis_contribution: number;
  confidence: number;
}

export interface PlayerSummary {
  player_id: string;
  name: string;
  team_id: string;
  position: string;
  sis_breakdown: SISBreakdown;
}

export interface ShadowProfile {
  player_id: string;
  player_name: string;
  team_id: string;
  position: string;
  match_id: string;
  minutes_played: number;
  conventional_stats: ConventionalStats;
  sis_breakdown: SISBreakdown;
  top_sequences: SequenceSummary[];
  strengths: string[];
  potential_weaknesses: string[];
  evidence_coverage: number;
  data_label: string;
}
