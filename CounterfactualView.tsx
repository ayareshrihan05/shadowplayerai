import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import { CounterfactualResult, SequenceDetail } from '../types';
import { useAppStore } from '../store/appStore';
import { FootballPitch } from '../components/pitch/FootballPitch';
import { PlayerMarker } from '../components/pitch/PlayerMarker';
import { BallMarker } from '../components/pitch/BallMarker';
import { PassingLaneOverlay } from '../components/pitch/PassingLaneOverlay';
import { LoadingSpinner } from '../components/shared/LoadingSpinner';
import { ArrowUpRight, ArrowDownRight, AlertTriangle } from 'lucide-react';

export const CounterfactualView: React.FC = () => {
  const selectedSequenceId = useAppStore((s) => s.selectedSequenceId);
  const setSelectedSequenceId = useAppStore((s) => s.setSelectedSequenceId);
  const currentMatchId = useAppStore((s) => s.currentMatchId);

  const [cfResult, setCfResult] = useState<CounterfactualResult | null>(null);
  const [seqDetail, setSeqDetail] = useState<SequenceDetail | null>(null);
  const [loading, setLoading] = useState(true);

  const availableSequences = currentMatchId === 'match-women-001' 
    ? ['SEQ-002', 'SEQ-004'] 
    : ['SEQ-001', 'SEQ-003'];

  useEffect(() => {
    if (!availableSequences.includes(selectedSequenceId)) {
      setSelectedSequenceId(availableSequences[0]);
    }
  }, [currentMatchId, selectedSequenceId, setSelectedSequenceId]);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const [cfData, seqData] = await Promise.all([
          api.getCounterfactual(selectedSequenceId),
          api.getSequenceDetail(selectedSequenceId),
        ]);
        setCfResult(cfData);
        setSeqDetail(seqData);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [selectedSequenceId]);

  if (loading) return <LoadingSpinner message="Simulating alternative tactical counterfactuals..." />;
  if (!cfResult || !seqDetail) return <div className="p-8 text-center text-red-400">Simulation data unavailable.</div>;

  const obsFrame = cfResult.observed.frames[Math.floor(cfResult.observed.frames.length / 2)] || cfResult.observed.frames[0];
  const cfFrame = cfResult.counterfactual.frames[Math.floor(cfResult.counterfactual.frames.length / 2)] || cfResult.counterfactual.frames[0];
  const delta = cfResult.delta;
  const obsMetrics = cfResult.observed.metrics;
  const cfMetrics = cfResult.counterfactual.metrics;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 flex flex-col gap-6">
      {/* Top Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-xs font-mono uppercase tracking-wider text-accent-amber">
            Counterfactual Simulation Lab
          </span>
          <h1 className="text-2xl font-bold text-text-primary">What If The Movement Never Happened?</h1>
          <p className="text-xs text-text-secondary mt-1">
            Comparing the observed match event against a controlled simulation where the player remains stationary.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {availableSequences.map((id) => (
            <button
              key={id}
              onClick={() => setSelectedSequenceId(id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold border transition-colors ${
                selectedSequenceId === id
                  ? 'bg-accent-amber text-white border-accent-amber'
                  : 'bg-surface border-border-subtle text-text-secondary hover:text-text-primary hover:bg-surface-elevated'
              }`}
            >
              {id}
            </button>
          ))}
        </div>
      </div>

      {/* Delta Metrics Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-surface border border-border-subtle rounded-xl p-4 flex flex-col justify-between">
          <span className="text-xs text-text-muted font-medium">Space Created</span>
          <div className="flex items-baseline gap-2 my-2">
            <span className="text-2xl font-bold font-mono text-metric-space">
              +{delta.delta_space_m2.toFixed(1)} m²
            </span>
            <ArrowUpRight size={18} className="text-metric-space" />
          </div>
          <span className="text-[11px] text-text-secondary">
            Observed {obsMetrics.space_created_m2}m² vs CF {cfMetrics.space_created_m2}m²
          </span>
        </div>

        <div className="bg-surface border border-border-subtle rounded-xl p-4 flex flex-col justify-between">
          <span className="text-xs text-text-muted font-medium">Passing Lanes</span>
          <div className="flex items-baseline gap-2 my-2">
            <span className="text-2xl font-bold font-mono text-metric-lane">
              +{delta.delta_passing_lanes} Open
            </span>
            <ArrowUpRight size={18} className="text-metric-lane" />
          </div>
          <span className="text-[11px] text-text-secondary">
            Observed {obsMetrics.passing_lanes_available} vs CF {cfMetrics.passing_lanes_available}
          </span>
        </div>

        <div className="bg-surface border border-border-subtle rounded-xl p-4 flex flex-col justify-between">
          <span className="text-xs text-text-muted font-medium">Defensive Density</span>
          <div className="flex items-baseline gap-2 my-2">
            <span className="text-2xl font-bold font-mono text-emerald-400">
              {delta.delta_defensive_coverage_pct > 0 ? `+${delta.delta_defensive_coverage_pct}` : delta.delta_defensive_coverage_pct}%
            </span>
            <ArrowDownRight size={18} className="text-emerald-400" />
          </div>
          <span className="text-[11px] text-text-secondary">
            Coverage reduced from {cfMetrics.defensive_coverage_pct}% to {obsMetrics.defensive_coverage_pct}%
          </span>
        </div>

        <div className="bg-surface border border-border-subtle rounded-xl p-4 flex flex-col justify-between">
          <span className="text-xs text-text-muted font-medium">Estimated Chance Quality</span>
          <div className="flex items-baseline gap-2 my-2">
            <span className="text-2xl font-bold font-mono text-accent-green">
              +{delta.delta_chance_quality.toFixed(2)}
            </span>
            <ArrowUpRight size={18} className="text-accent-green" />
          </div>
          <span className="text-[11px] text-text-secondary">
            Quality uplift generated by off-ball run
          </span>
        </div>
      </div>

      {/* Dual Pitch Comparison */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Observed Scenario */}
        <div className="bg-surface border border-border-subtle rounded-xl p-4 flex flex-col gap-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-accent-green" />
              <h3 className="text-sm font-bold text-text-primary">Observed Match Action</h3>
            </div>
            <span className="text-xs font-mono text-accent-green font-semibold">Decoy Run Executed</span>
          </div>

          <div className="border border-border-subtle rounded-lg overflow-hidden">
            {obsFrame && (
              <FootballPitch>
                <PassingLaneOverlay lanes={obsFrame.passing_lanes} players={obsFrame.players} />
                {obsFrame.players.map((pl) => (
                  <PlayerMarker
                    key={pl.player_id}
                    playerId={pl.player_id}
                    x={pl.x}
                    y={pl.y}
                    jerseyNumber={parseInt(pl.player_id.replace('p', ''))}
                    isFocusPlayer={pl.player_id === seqDetail.focus_player_id}
                    isInPossession={pl.is_in_possession}
                  />
                ))}
                <BallMarker x={obsFrame.ball.x} y={obsFrame.ball.y} />
              </FootballPitch>
            )}
          </div>
          <p className="text-xs text-text-secondary leading-relaxed">
            Player makes dynamic run pulling defender out of central corridor, opening up direct through-ball option.
          </p>
        </div>

        {/* Right: Counterfactual Simulation */}
        <div className="bg-surface border border-border-subtle rounded-xl p-4 flex flex-col gap-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-accent-amber" />
              <h3 className="text-sm font-bold text-text-primary">Simulated Counterfactual</h3>
            </div>
            <span className="text-xs font-mono text-accent-amber font-semibold">Player Stationary</span>
          </div>

          <div className="border border-border-subtle rounded-lg overflow-hidden">
            {cfFrame && (
              <FootballPitch>
                <PassingLaneOverlay lanes={cfFrame.passing_lanes} players={cfFrame.players} />
                {cfFrame.players.map((pl) => (
                  <PlayerMarker
                    key={pl.player_id}
                    playerId={pl.player_id}
                    x={pl.x}
                    y={pl.y}
                    jerseyNumber={parseInt(pl.player_id.replace('p', ''))}
                    isFocusPlayer={pl.player_id === seqDetail.focus_player_id}
                    isInPossession={pl.is_in_possession}
                  />
                ))}
                <BallMarker x={cfFrame.ball.x} y={cfFrame.ball.y} />
              </FootballPitch>
            )}
          </div>
          <p className="text-xs text-text-secondary leading-relaxed">
            Player stays in starting position. Defender remains central. The forward passing lane remains closed.
          </p>
        </div>
      </div>

      {/* Mandatory Counterfactual Disclaimer */}
      <div className="bg-surface border border-amber-500/30 rounded-xl p-4 flex items-center gap-3 text-xs text-amber-400">
        <AlertTriangle size={18} className="flex-shrink-0" />
        <p className="leading-relaxed">
          <strong>{cfResult.label}:</strong> Counterfactual analysis estimates alternative tactical outcomes through deterministic simulation. It illustrates potential outcomes rather than asserting real-world certainty.
        </p>
      </div>
    </div>
  );
};
