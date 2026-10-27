import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import { MatchDetail, PlayerSummary } from '../types';
import { FootballPitch } from '../components/pitch/FootballPitch';
import { PlayerMarker } from '../components/pitch/PlayerMarker';
import { LoadingSpinner } from '../components/shared/LoadingSpinner';
import { useAppStore } from '../store/appStore';
import { useNavigate } from 'react-router-dom';

export const MatchView: React.FC = () => {
  const navigate = useNavigate();
  const currentMatchId = useAppStore((s) => s.currentMatchId);
  const setSelectedPlayerId = useAppStore((s) => s.setSelectedPlayerId);

  const [match, setMatch] = useState<MatchDetail | null>(null);
  const [players, setPlayers] = useState<PlayerSummary[]>([]);
  const [loading, setLoading] = useState(true);

  // Formation positions for Northvale (blue, left-to-right) and Eastmere (amber, right-to-left)
  const defaultFormation: Record<string, { x: number; y: number }> = {
    // Northvale FC (4-3-3)
    p001: { x: 78.0, y: 34.0 }, // ST
    p002: { x: 72.0, y: 58.0 }, // LW
    p003: { x: 68.0, y: 34.0 }, // CAM
    p004: { x: 58.0, y: 44.0 }, // CM
    p005: { x: 58.0, y: 24.0 }, // CM
    p006: { x: 46.0, y: 34.0 }, // DM
    p007: { x: 38.0, y: 12.0 }, // RB
    p008: { x: 26.0, y: 40.0 }, // CB
    p009: { x: 26.0, y: 28.0 }, // CB
    p010: { x: 38.0, y: 56.0 }, // LB
    p011: { x: 6.0, y: 34.0 },  // GK
    // Eastmere City (4-4-2)
    p012: { x: 38.0, y: 36.0 }, // ST
    p013: { x: 48.0, y: 58.0 }, // RW
    p014: { x: 48.0, y: 34.0 }, // CAM
    p015: { x: 54.0, y: 44.0 }, // CM
    p016: { x: 54.0, y: 24.0 }, // CM
    p017: { x: 62.0, y: 34.0 }, // DM
    p018: { x: 70.0, y: 12.0 }, // RB
    p019: { x: 78.0, y: 40.0 }, // CB
    p020: { x: 78.0, y: 28.0 }, // CB
    p021: { x: 70.0, y: 56.0 }, // LB
    p022: { x: 99.0, y: 34.0 }, // GK
  };

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const [mDetail, pList] = await Promise.all([
          api.getMatchDetail(currentMatchId),
          api.getMatchPlayers(currentMatchId),
        ]);
        setMatch(mDetail);
        setPlayers(pList);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [currentMatchId]);

  if (loading) return <LoadingSpinner message="Loading match visualizer..." />;
  if (!match) return <div className="p-8 text-center text-red-400">Match data unavailable.</div>;

  const handleSelect = (pid: string) => {
    setSelectedPlayerId(pid);
    navigate('/profile');
  };

  const isWomenMatch = currentMatchId === 'match-women-001';
  const activeFormation = isWomenMatch
    ? Object.fromEntries(Object.entries(defaultFormation).map(([k, v]) => [k.replace('p', 'w'), v]))
    : defaultFormation;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 flex flex-col gap-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-xs font-mono uppercase tracking-wider text-accent-green">
            {isWomenMatch ? "Women's Super League" : "Men's Premier League"}
          </span>
          <h1 className="text-2xl font-bold text-text-primary">Match Tactical Overview</h1>
          <p className="text-xs text-text-secondary mt-1">
            Interactive formation map. Click any player marker to inspect their individual Shadow Profile.
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs font-mono bg-surface border border-border-subtle px-3 py-1.5 rounded-lg">
          <span className="text-text-muted">Active Competition:</span>
          <span className={`font-bold ${isWomenMatch ? 'text-accent-magenta' : 'text-team-northvale'}`}>
            {isWomenMatch ? "Women's Super League (WSL)" : "Men's Premier League (PL)"}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Main Pitch (3 Cols) */}
        <div className="lg:col-span-3">
          <FootballPitch>
            {Object.entries(activeFormation).map(([pid, coords]) => {
              const pInfo = players.find((p) => p.player_id === pid);
              const num = parseInt(pid.replace(/[pw]/g, ''));
              return (
                <PlayerMarker
                  key={pid}
                  playerId={pid}
                  x={coords.x}
                  y={coords.y}
                  jerseyNumber={num}
                  position={pInfo?.position}
                  name={pInfo?.name}
                  teamId={pInfo?.team_id || (num <= 11 ? 'northvale' : 'eastmere')}
                  onClick={() => handleSelect(pid)}
                />
              );
            })}
          </FootballPitch>

          <div className="flex items-center justify-between text-xs text-text-muted mt-3 px-2">
            <div className="flex items-center gap-2">
              <span className={`w-3 h-3 rounded-full ${isWomenMatch ? 'bg-accent-magenta' : 'bg-team-northvale'}`} />
              <span className="font-semibold text-text-primary">
                {isWomenMatch ? 'Northvale FC Women (4-3-3)' : 'Northvale FC (4-3-3)'}
              </span>
              <span>Attacking Left → Right</span>
            </div>
            <div className="flex items-center gap-2">
              <span>Attacking Right → Left</span>
              <span className="font-semibold text-text-primary">
                {isWomenMatch ? 'Eastmere City Women (4-4-2)' : 'Eastmere City (4-4-2)'}
              </span>
              <span className="w-3 h-3 rounded-full bg-team-eastmere" />
            </div>
          </div>
        </div>

        {/* Squad List / Sidebar */}
        <div className="bg-surface border border-border-subtle rounded-xl p-5 flex flex-col gap-4">
          <h2 className="text-sm font-bold text-text-primary">Match Roster (22 Players)</h2>
          <div className="flex flex-col gap-2 max-h-[520px] overflow-y-auto pr-1">
            {players.map((p) => (
              <div
                key={p.player_id}
                onClick={() => handleSelect(p.player_id)}
                className="p-2.5 rounded-lg bg-surface-elevated/60 hover:bg-surface-elevated border border-border-subtle cursor-pointer transition-colors flex items-center justify-between"
              >
                <div>
                  <span className="text-xs font-bold text-text-primary block">{p.name}</span>
                  <span className="text-[11px] text-text-muted">
                    {p.position} • {p.team_id.includes('northvale') ? 'Northvale' : 'Eastmere'}
                  </span>
                </div>
                <div className="text-right">
                  <span className="text-xs font-mono font-bold text-accent-green block">
                    {p.sis_breakdown.sis.toFixed(1)}
                  </span>
                  <span className="text-[10px] text-text-muted font-mono">SIS</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
