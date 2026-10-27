import {
  ApiResponse,
  MatchSummary,
  MatchDetail,
  PlayerSummary,
  MatchInsights,
  ShadowProfile,
  SequenceDetail,
  CounterfactualResult,
  ScoutingReport,
  PersonalizationTier,
} from '../types';

const API_ORIGIN = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/+$/, '');
const BASE_URL = `${API_ORIGIN}/api`;

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${url}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!res.ok) {
    const errorJson = await res.json().catch(() => null);
    throw new Error(errorJson?.detail?.error?.message || `HTTP ${res.status}: ${res.statusText}`);
  }

  const envelope: ApiResponse<T> = await res.json();
  return envelope.data;
}

export const api = {
  getHealth: () => fetchJson<{ status: string; database_connected: boolean }>('/health'),
  
  getMatches: () => fetchJson<MatchSummary[]>('/matches'),
  
  getMatchDetail: (matchId: string) => fetchJson<MatchDetail>(`/matches/${matchId}`),
  
  getMatchPlayers: (matchId: string) => fetchJson<PlayerSummary[]>(`/matches/${matchId}/players`),
  
  getMatchInsights: (matchId: string) => fetchJson<MatchInsights>(`/matches/${matchId}/insights`),
  
  getShadowProfile: (playerId: string, matchId: string = 'match-alpha-001') =>
    fetchJson<ShadowProfile>(`/players/${playerId}/shadow-profile?match_id=${encodeURIComponent(matchId)}`),
    
  getPlayerSequences: (playerId: string, matchId: string = 'match-alpha-001', movementType?: string) => {
    const query = new URLSearchParams({ match_id: matchId });
    if (movementType) query.append('movement_type', movementType);
    return fetchJson<SequenceDetail[]>(`/players/${playerId}/sequences?${query.toString()}`);
  },
  
  getSequenceDetail: (sequenceId: string) => fetchJson<SequenceDetail>(`/sequences/${sequenceId}`),
  
  getCounterfactual: (sequenceId: string, counterfactualType: string = 'remove_movement') =>
    fetchJson<CounterfactualResult>(`/sequences/${sequenceId}/counterfactual`, {
      method: 'POST',
      body: JSON.stringify({ counterfactual_type: counterfactualType }),
    }),
    
  generateScoutingReport: (playerId: string, matchId: string = 'match-alpha-001', tier: PersonalizationTier = 'analyst') =>
    fetchJson<ScoutingReport>('/reports/player', {
      method: 'POST',
      body: JSON.stringify({ player_id: playerId, match_id: matchId, tier }),
    }),
};
