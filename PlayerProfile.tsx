import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import { ShadowProfile, PlayerSummary } from '../types';
import { useAppStore } from '../store/appStore';
import { LoadingSpinner } from '../components/shared/LoadingSpinner';
import { ConfidenceBadge } from '../components/shared/ConfidenceBadge';
import { useNavigate } from 'react-router-dom';
import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { PlayCircle, FileText, CheckCircle2, AlertCircle } from 'lucide-react';

export const PlayerProfile: React.FC = () => {
  const navigate = useNavigate();
  const currentMatchId = useAppStore((s) => s.currentMatchId);
  const selectedPlayerId = useAppStore((s) => s.selectedPlayerId);
  const setSelectedPlayerId = useAppStore((s) => s.setSelectedPlayerId);
  const setSelectedSequenceId = useAppStore((s) => s.setSelectedSequenceId);

  const [profile, setProfile] = useState<ShadowProfile | null>(null);
  const [allPlayers, setAllPlayers] = useState<PlayerSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        // Ensure selectedPlayerId matches active match gender
        let activePlayerId = selectedPlayerId;
        if (currentMatchId === 'match-women-001' && selectedPlayerId.startsWith('p')) {
          activePlayerId = 'w002';
          setSelectedPlayerId('w002');
        } else if (currentMatchId !== 'match-women-001' && selectedPlayerId.startsWith('w')) {
          activePlayerId = 'p001';
          setSelectedPlayerId('p001');
        }

        const [profData, playersList] = await Promise.all([
          api.getShadowProfile(activePlayerId, currentMatchId),
          api.getMatchPlayers(currentMatchId),
        ]);
        setProfile(profData);
        setAllPlayers(playersList);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [selectedPlayerId, currentMatchId, setSelectedPlayerId]);

  if (loading) return <LoadingSpinner message="Generating Shadow Profile..." />;
  if (!profile) return <div className="p-8 text-center text-red-400">Profile unavailable.</div>;

  const sis = profile.sis_breakdown;
  const conv = profile.conventional_stats;

  const radarData = [
    { metric: 'Space (S)', value: sis.space_creation_score, fullMark: 100 },
    { metric: 'Lanes (P)', value: sis.passing_lane_score, fullMark: 100 },
    { metric: 'Defense (D)', value: sis.defensive_support_score, fullMark: 100 },
    { metric: 'Chain (C)', value: sis.chain_reaction_score, fullMark: 100 },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 flex flex-col gap-6">
      {/* Top Selector & Profile Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-surface border border-border-subtle rounded-xl p-6">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-full bg-accent-green/10 border-2 border-accent-green flex items-center justify-center font-bold text-xl text-accent-green">
            {profile.position}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-text-primary">{profile.player_name}</h1>
              <ConfidenceBadge confidence={sis.confidence} />
            </div>
            <span className="text-xs text-text-muted font-mono block mt-0.5">
              {profile.team_id.includes('northvale') ? 'Northvale FC' : 'Eastmere City'} • {profile.minutes_played} Minutes Played
            </span>
          </div>
        </div>

        {/* Player Switcher Dropdown */}
        <div className="flex items-center gap-2">
          <select
            value={selectedPlayerId}
            onChange={(e) => setSelectedPlayerId(e.target.value)}
            className="bg-surface-elevated border border-border-subtle text-text-primary text-xs rounded-lg px-3 py-2 focus:ring-2 focus:ring-accent-green focus:outline-none"
          >
            {allPlayers.map((p) => (
              <option key={p.player_id} value={p.player_id}>
                {p.name} ({p.position})
              </option>
            ))}
          </select>

          <button
            onClick={() => navigate('/report')}
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-accent-green text-white text-xs font-bold hover:bg-emerald-400 transition-colors"
          >
            <FileText size={14} />
            <span>AI Report</span>
          </button>
        </div>
      </div>

      {/* Stats Comparison: Conventional vs Shadow Impact */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Conventional Statistics */}
        <div className="bg-surface border border-border-subtle rounded-xl p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold uppercase tracking-wider text-text-muted">
                Conventional Match Statistics
              </h3>
              <span className="text-xs text-text-muted">Direct Touches Only</span>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="bg-surface-elevated border border-border-subtle rounded-lg p-3 text-center">
                <span className="text-xs text-text-muted block">Goals</span>
                <span className="text-2xl font-bold font-mono text-text-primary">{conv.goals}</span>
              </div>
              <div className="bg-surface-elevated border border-border-subtle rounded-lg p-3 text-center">
                <span className="text-xs text-text-muted block">Assists</span>
                <span className="text-2xl font-bold font-mono text-text-primary">{conv.assists}</span>
              </div>
              <div className="bg-surface-elevated border border-border-subtle rounded-lg p-3 text-center">
                <span className="text-xs text-text-muted block">Shots</span>
                <span className="text-2xl font-bold font-mono text-text-primary">{conv.shots}</span>
              </div>
              <div className="bg-surface-elevated border border-border-subtle rounded-lg p-3 text-center">
                <span className="text-xs text-text-muted block">Passes Cmp</span>
                <span className="text-2xl font-bold font-mono text-text-primary">{conv.passes_completed}</span>
              </div>
            </div>
          </div>
          <p className="text-xs text-text-secondary mt-4 leading-relaxed">
            Conventional metrics capture less than 3% of a player's total match time.
          </p>
        </div>

        {/* Shadow Impact Score (SIS) */}
        <div className="bg-surface border border-border-subtle rounded-xl p-6">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold uppercase tracking-wider text-text-muted">
              Composite Shadow Impact Score
            </h3>
            <span className="text-xs font-mono font-bold text-accent-green px-2 py-0.5 rounded bg-accent-green/10 border border-accent-green/30">
              {sis.sis.toFixed(1)} / 100
            </span>
          </div>

          <div className="flex flex-col gap-3 mt-4">
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-metric-space font-medium">Space Creation (S • 35%)</span>
                <span className="font-mono font-bold">{sis.space_creation_score.toFixed(1)}</span>
              </div>
              <div className="w-full bg-surface-elevated h-2 rounded-full overflow-hidden">
                <div
                  className="bg-metric-space h-full rounded-full transition-all duration-500"
                  style={{ width: `${sis.space_creation_score}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-metric-lane font-medium">Passing Lanes (P • 25%)</span>
                <span className="font-mono font-bold">{sis.passing_lane_score.toFixed(1)}</span>
              </div>
              <div className="w-full bg-surface-elevated h-2 rounded-full overflow-hidden">
                <div
                  className="bg-metric-lane h-full rounded-full transition-all duration-500"
                  style={{ width: `${sis.passing_lane_score}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-metric-defense font-medium">Defensive Support (D • 20%)</span>
                <span className="font-mono font-bold">{sis.defensive_support_score.toFixed(1)}</span>
              </div>
              <div className="w-full bg-surface-elevated h-2 rounded-full overflow-hidden">
                <div
                  className="bg-metric-defense h-full rounded-full transition-all duration-500"
                  style={{ width: `${sis.defensive_support_score}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-metric-chain font-medium">Chain Reaction (C • 20%)</span>
                <span className="font-mono font-bold">{sis.chain_reaction_score.toFixed(1)}</span>
              </div>
              <div className="w-full bg-surface-elevated h-2 rounded-full overflow-hidden">
                <div
                  className="bg-metric-chain h-full rounded-full transition-all duration-500"
                  style={{ width: `${sis.chain_reaction_score}%` }}
                />
              </div>
            </div>
          </div>
          <span className="text-[10px] text-text-muted block mt-3 text-right">
            {sis.label}
          </span>
        </div>
      </div>

      {/* Radar Chart & Qualitative Insights */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Radar Chart */}
        <div className="bg-surface border border-border-subtle rounded-xl p-6 flex flex-col items-center">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-2 w-full text-left">
            Off-Ball Tactical Polygon
          </h3>
          <div className="w-full h-64">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#30363D" />
                <PolarAngleAxis dataKey="metric" tick={{ fill: '#8B949E', fontSize: 11 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#30363D" tick={false} />
                <Radar
                  name="SIS Profile"
                  dataKey="value"
                  stroke="#39D353"
                  fill="#39D353"
                  fillOpacity={0.35}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Strengths & Weaknesses */}
        <div className="bg-surface border border-border-subtle rounded-xl p-6 flex flex-col justify-between">
          <div className="flex flex-col gap-4">
            <div>
              <h3 className="text-xs font-semibold uppercase tracking-wider text-emerald-400 mb-2 flex items-center gap-1.5">
                <CheckCircle2 size={14} />
                Key Off-Ball Strengths
              </h3>
              <ul className="text-xs text-text-secondary flex flex-col gap-1.5">
                {profile.strengths.map((str, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="text-accent-green">•</span>
                    <span>{str}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="text-xs font-semibold uppercase tracking-wider text-amber-400 mb-2 flex items-center gap-1.5">
                <AlertCircle size={14} />
                Potential Weaknesses / Growth Areas
              </h3>
              <ul className="text-xs text-text-secondary flex flex-col gap-1.5">
                {profile.potential_weaknesses.map((w, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="text-amber-400">•</span>
                    <span>{w}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="pt-3 border-t border-border-subtle flex items-center justify-between text-xs text-text-muted">
            <span>Evidence coverage across match:</span>
            <span className="font-mono text-accent-green font-bold">
              {(profile.evidence_coverage * 100).toFixed(0)}%
            </span>
          </div>
        </div>
      </div>

      {/* Top Tactical Sequences */}
      <div className="bg-surface border border-border-subtle rounded-xl p-6">
        <h3 className="text-sm font-bold text-text-primary mb-4 flex items-center gap-2">
          <PlayCircle size={18} className="text-accent-green" />
          Top Off-Ball Movement Sequences
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {profile.top_sequences.map((seq) => (
            <div
              key={seq.sequence_id}
              className="bg-surface-elevated/70 border border-border-subtle rounded-lg p-3.5 flex flex-col justify-between hover:border-border-focus transition-all"
            >
              <div>
                <div className="flex items-center justify-between text-xs font-mono text-text-muted mb-1">
                  <span>t={seq.timestamp_start.toFixed(0)}s</span>
                  <ConfidenceBadge confidence={seq.confidence} />
                </div>
                <h4 className="text-xs font-bold text-text-primary">{seq.name}</h4>
                <span className="text-[11px] text-text-muted block mt-0.5">
                  Type: {seq.movement_type.replace('_', ' ')}
                </span>
              </div>
              <div className="flex items-center justify-between mt-3 pt-2 border-t border-border-subtle/50">
                <span className="text-xs text-accent-green font-mono font-bold">
                  +{seq.sis_contribution.toFixed(1)} SIS
                </span>
                {['SEQ-001', 'SEQ-002', 'SEQ-003'].includes(seq.sequence_id) && (
                  <button
                    onClick={() => {
                      setSelectedSequenceId(seq.sequence_id);
                      navigate('/replay');
                    }}
                    className="text-xs text-text-primary hover:text-accent-green font-medium flex items-center gap-1"
                  >
                    Replay →
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
