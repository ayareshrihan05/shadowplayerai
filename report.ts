export interface ReportSections {
  overview: string;
  off_ball_strengths: string;
  key_sequences: string;
  defensive_contributions: string;
  attacking_contributions: string;
  improvement_areas: string;
  limitations: string;
}

export interface ScoutingReport {
  player_id: string;
  player_name: string;
  generation_method: string;
  sections: ReportSections;
  referenced_metrics: Record<string, number>;
  disclaimer: string;
}
