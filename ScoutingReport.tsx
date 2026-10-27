import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import { ScoutingReport as IScoutingReport, PlayerSummary } from '../types';
import { useAppStore } from '../store/appStore';
import { LoadingSpinner } from '../components/shared/LoadingSpinner';
import { Sparkles, ShieldAlert } from 'lucide-react';

export const ScoutingReport: React.FC = () => {
  const currentMatchId = useAppStore((s) => s.currentMatchId);
  const selectedPlayerId = useAppStore((s) => s.selectedPlayerId);
  const setSelectedPlayerId = useAppStore((s) => s.setSelectedPlayerId);
  const tier = useAppStore((s) => s.tier);
  const setTier = useAppStore((s) => s.setTier);

  const [report, setReport] = useState<IScoutingReport | null>(null);
  const [allPlayers, setAllPlayers] = useState<PlayerSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        let activePlayerId = selectedPlayerId;
        if (currentMatchId === 'match-women-001' && selectedPlayerId.startsWith('p')) {
          activePlayerId = 'w002';
          setSelectedPlayerId('w002');
        } else if (currentMatchId !== 'match-women-001' && selectedPlayerId.startsWith('w')) {
          activePlayerId = 'p001';
          setSelectedPlayerId('p001');
        }

        const [reportData, playersList] = await Promise.all([
          api.generateScoutingReport(activePlayerId, currentMatchId, tier),
          api.getMatchPlayers(currentMatchId),
        ]);
        setReport(reportData);
        setAllPlayers(playersList);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [selectedPlayerId, currentMatchId, tier, setSelectedPlayerId]);

  if (loading) return <LoadingSpinner message="Generating AI Scouting Report with verified metrics..." />;
  if (!report) return <div className="p-8 text-center text-red-400">Report generation failed.</div>;

  const sections = report.sections;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 flex flex-col gap-6">
      {/* Top Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-surface border border-border-subtle rounded-xl p-5">
        <div>
          <span className="text-xs font-mono uppercase tracking-wider text-accent-green">
            AI Narrative Intelligence
          </span>
          <h1 className="text-2xl font-bold text-text-primary">Player Scouting Dossier</h1>
        </div>

        <div className="flex items-center gap-3">
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

          <div className="flex rounded-lg bg-surface-elevated p-1 border border-border-subtle text-xs">
            {(['casual', 'analyst', 'coach'] as const).map((t) => (
              <button
                key={t}
                onClick={() => setTier(t)}
                className={`px-2.5 py-1 rounded capitalize font-medium transition-colors ${
                  tier === t
                    ? 'bg-accent-green text-white font-bold'
                    : 'text-text-secondary hover:text-text-primary'
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Report Document */}
      <div className="bg-surface border border-border-subtle rounded-2xl p-6 sm:p-8 flex flex-col gap-6">
        {/* Document Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-border-subtle gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-mono text-accent-green">DOSSIER REF: SP-AI-{report.player_id.toUpperCase()}</span>
              <span className="text-xs text-text-muted">•</span>
              <span className="text-xs font-mono text-text-muted">TIER: {tier.toUpperCase()}</span>
            </div>
            <h2 className="text-2xl font-extrabold text-text-primary">{report.player_name}</h2>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs font-mono px-2.5 py-1 rounded bg-surface-elevated border border-border-subtle text-text-secondary flex items-center gap-1.5">
              <Sparkles size={13} className="text-accent-green" />
              Engine: {report.generation_method === 'ms_foundry' ? 'Microsoft Foundry' : 'Deterministic Fallback'}
            </span>
          </div>
        </div>

        {/* Verified Metrics Strip */}
        <div className="bg-surface-elevated border border-border-subtle rounded-xl p-4">
          <span className="text-[11px] font-mono uppercase tracking-wider text-text-muted block mb-2">
            Verified Input Metrics from Synthetic Tracking Engine
          </span>
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 text-center">
            <div>
              <span className="text-xs text-text-muted block">SIS</span>
              <span className="text-base font-bold font-mono text-accent-green">
                {report.referenced_metrics.sis?.toFixed(1)}
              </span>
            </div>
            <div>
              <span className="text-xs text-text-muted block">Space (S)</span>
              <span className="text-base font-bold font-mono text-metric-space">
                {report.referenced_metrics.space_creation_score?.toFixed(1)}
              </span>
            </div>
            <div>
              <span className="text-xs text-text-muted block">Lanes (P)</span>
              <span className="text-base font-bold font-mono text-metric-lane">
                {report.referenced_metrics.passing_lane_score?.toFixed(1)}
              </span>
            </div>
            <div>
              <span className="text-xs text-text-muted block">Defense (D)</span>
              <span className="text-base font-bold font-mono text-metric-defense">
                {report.referenced_metrics.defensive_support_score?.toFixed(1)}
              </span>
            </div>
            <div>
              <span className="text-xs text-text-muted block">Chain (C)</span>
              <span className="text-base font-bold font-mono text-metric-chain">
                {report.referenced_metrics.chain_reaction_score?.toFixed(1)}
              </span>
            </div>
          </div>
        </div>

        {/* Narrative Sections */}
        <div className="flex flex-col gap-5 text-sm leading-relaxed">
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-text-muted mb-1.5">
              1. Executive Performance Overview
            </h3>
            <p className="text-text-primary whitespace-pre-line">{sections.overview}</p>
          </div>

          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-text-muted mb-1.5">
              2. Key Off-Ball Strengths
            </h3>
            <p className="text-text-primary whitespace-pre-line">{sections.off_ball_strengths}</p>
          </div>

          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-text-muted mb-1.5">
              3. Critical Sequence Analysis
            </h3>
            <p className="text-text-primary whitespace-pre-line">{sections.key_sequences}</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-surface-elevated/40 border border-border-subtle rounded-lg p-3.5">
              <h4 className="text-xs font-bold uppercase tracking-wider text-metric-defense mb-1">
                4. Defensive Contributions
              </h4>
              <p className="text-xs text-text-secondary">{sections.defensive_contributions}</p>
            </div>
            <div className="bg-surface-elevated/40 border border-border-subtle rounded-lg p-3.5">
              <h4 className="text-xs font-bold uppercase tracking-wider text-metric-space mb-1">
                5. Attacking Contributions
              </h4>
              <p className="text-xs text-text-secondary">{sections.attacking_contributions}</p>
            </div>
          </div>

          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-text-muted mb-1.5">
              6. Development & Training Areas
            </h3>
            <p className="text-text-primary whitespace-pre-line">{sections.improvement_areas}</p>
          </div>

          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-text-muted mb-1.5">
              7. Analytical Uncertainty & Limitations
            </h3>
            <p className="text-xs text-text-secondary whitespace-pre-line">{sections.limitations}</p>
          </div>
        </div>

        {/* Footer Disclaimer */}
        <div className="pt-4 border-t border-border-subtle flex items-center gap-2 text-xs text-text-muted">
          <ShieldAlert size={14} className="text-amber-500/80 flex-shrink-0" />
          <span>{report.disclaimer}</span>
        </div>
      </div>
    </div>
  );
};
