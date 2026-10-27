import { FrameData } from './match';

export interface MovementDetection {
  movement_id: string;
  player_id: string;
  movement_type: string;
  timestamp_start: number;
  timestamp_end: number;
  confidence: number;
  confidence_label: string;
  evidence_event_ids: string[];
  evidence_frame_ids: string[];
  criteria_met: Record<string, boolean>;
  sis_components: {
    S: number;
    P: number;
    D: number;
    C: number;
  };
}

export interface AIExplanation {
  text: string;
  evidence_refs: string[];
  generation_method: string;
  disclaimer: string;
}

export interface SequenceDetail {
  sequence_id: string;
  name: string;
  match_id: string;
  focus_player_id: string;
  timestamp_start: number;
  timestamp_end: number;
  frames: FrameData[];
  key_events: string[];
  movement_detections: MovementDetection[];
  ai_explanation: AIExplanation;
}
