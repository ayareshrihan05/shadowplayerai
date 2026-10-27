import { FrameData } from './match';

export interface ScenarioMetrics {
  space_created_m2: number;
  passing_lanes_available: number;
  defensive_coverage_pct: number;
  estimated_chance_quality: number;
}

export interface ScenarioState {
  frames: FrameData[];
  metrics: ScenarioMetrics;
}

export interface CounterfactualDelta {
  delta_space_m2: number;
  delta_passing_lanes: number;
  delta_defensive_coverage_pct: number;
  delta_chance_quality: number;
}

export interface CounterfactualResult {
  sequence_id: string;
  counterfactual_type: string;
  observed: ScenarioState;
  counterfactual: ScenarioState;
  delta: CounterfactualDelta;
  label: string;
}
