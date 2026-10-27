import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import { SequenceDetail } from '../types';
import { useAppStore } from '../store/appStore';
import { FootballPitch, toSVGCoords } from '../components/pitch/FootballPitch';
import { PlayerMarker } from '../components/pitch/PlayerMarker';
import { BallMarker } from '../components/pitch/BallMarker';
import { TrajectoryTrail } from '../components/pitch/TrajectoryTrail';
import { PassingLaneOverlay } from '../components/pitch/PassingLaneOverlay';
import { DefenderArrow } from '../components/pitch/DefenderArrow';
import { ReplayControls } from '../components/replay/ReplayControls';
import { TogglePanel } from '../components/replay/TogglePanel';
import { ExplanationPanel } from '../components/replay/ExplanationPanel';
import { LoadingSpinner } from '../components/shared/LoadingSpinner';
import { useReplayAnimation } from '../hooks/useReplayAnimation';
import { useNavigate } from 'react-router-dom';
import { GitCompare } from 'lucide-react';

export const ReplayView: React.FC = () => {
  const navigate = useNavigate();
  const selectedSequenceId = useAppStore((s) => s.selectedSequenceId);
  const setSelectedSequenceId = useAppStore((s) => s.setSelectedSequenceId);
  const currentMatchId = useAppStore((s) => s.currentMatchId);
  const replay = useAppStore((s) => s.replay);
  const resetReplay = useAppStore((s) => s.resetReplay);

  const [sequence, setSequence] = useState<SequenceDetail | null>(null);
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
        resetReplay();
        const data = await api.getSequenceDetail(selectedSequenceId);
        setSequence(data);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [selectedSequenceId]);

  const frames = sequence?.frames || [];
  const currentFrame = frames[replay.currentFrameIndex] || frames[0];

  // Drive animation
  useReplayAnimation(frames.length);

  if (loading) return <LoadingSpinner message="Loading tactical sequence coordinates and frames..." />;
  if (!sequence || !currentFrame) return <div className="p-8 text-center text-red-400">Sequence data unavailable.</div>;

  // Build trail for focus player up to current frame
  const focusPlayerHistory = frames
    .slice(0, replay.currentFrameIndex + 1)
    .map((f) => {
      const p = f.players.find((pl) => pl.player_id === sequence.focus_player_id);
      return p ? { x: p.x, y: p.y } : null;
    })
    .filter((pt): pt is { x: number; y: number } => pt !== null);

  // Build trail for key responding defender (e.g. p020 in SEQ-001, p018 in SEQ-002, p006 in SEQ-003)
  const defenderId =
    sequence.sequence_id === 'SEQ-001'
      ? 'p020'
      : sequence.sequence_id === 'SEQ-002'
      ? 'p018'
      : 'p017';

  const defenderHistory = frames
    .slice(0, replay.currentFrameIndex + 1)
    .map((f) => {
      const p = f.players.find((pl) => pl.player_id === defenderId);
      return p ? { x: p.x, y: p.y } : null;
    })
    .filter((pt): pt is { x: number; y: number } => pt !== null);

  const focusPlayerPos = currentFrame.players.find((p) => p.player_id === sequence.focus_player_id);
  const defenderPos = currentFrame.players.find((p) => p.player_id === defenderId);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 flex flex-col gap-6">
      {/* Top Bar: Scenario Switcher Tabs */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-xs font-mono uppercase tracking-wider text-accent-green">
            Flagship Analytics Engine
          </span>
          <h1 className="text-2xl font-bold text-text-primary">Invisible Impact Replay</h1>
        </div>

        <div className="flex items-center gap-2">
          {availableSequences.map((id) => (
            <button
              key={id}
              onClick={() => setSelectedSequenceId(id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold border transition-colors ${
                selectedSequenceId === id
                  ? 'bg-accent-green text-white border-accent-green'
                  : 'bg-surface border-border-subtle text-text-secondary hover:text-text-primary hover:bg-surface-elevated'
              }`}
            >
              {id}
            </button>
          ))}

          <button
            onClick={() => navigate('/counterfactual')}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-surface-elevated border border-border-subtle text-xs font-medium text-text-primary hover:border-accent-amber hover:text-accent-amber transition-colors ml-2"
          >
            <GitCompare size={14} />
            <span>Counterfactual</span>
          </button>
        </div>
      </div>

      {/* Main Pitch View */}
      <div className="relative">
        <FootballPitch>
          {/* 1. Open Space Zones (underlay) */}
          {replay.showSpaceZones &&
            currentFrame.open_space_zones?.map((zone, i) => {
              const { svgX, svgY } = toSVGCoords(zone.x, zone.y);
              return (
                <circle
                  key={i}
                  cx={svgX}
                  cy={svgY}
                  r={zone.radius * 10}
                  fill="#39D353"
                  fillOpacity="0.15"
                  stroke="#39D353"
                  strokeWidth="2"
                  strokeDasharray="4 2"
                />
              );
            })}

          {/* 2. Passing Lanes */}
          {replay.showPassingLanes && (
            <PassingLaneOverlay
              lanes={currentFrame.passing_lanes}
              players={currentFrame.players}
            />
          )}

          {/* 3. Trajectory Trails */}
          {replay.showTrails && (
            <>
              <TrajectoryTrail points={focusPlayerHistory} color="#39D353" strokeWidth={3.5} />
              <TrajectoryTrail points={defenderHistory} color="#EF4444" strokeWidth={2.5} />
            </>
          )}

          {/* 4. Defender Reaction Vector Arrow */}
          {replay.showDefenders && focusPlayerPos && defenderPos && (
            <DefenderArrow
              startX={defenderPos.x}
              startY={defenderPos.y}
              endX={focusPlayerPos.x}
              endY={focusPlayerPos.y}
              color="#EF4444"
              label="Track"
            />
          )}

          {/* 5. All 22 Player Markers */}
          {currentFrame.players.map((pl) => (
            <PlayerMarker
              key={pl.player_id}
              playerId={pl.player_id}
              x={pl.x}
              y={pl.y}
              jerseyNumber={parseInt(pl.player_id.replace('p', ''))}
              isInPossession={pl.is_in_possession}
              isFocusPlayer={pl.player_id === sequence.focus_player_id}
              speed={pl.speed}
            />
          ))}

          {/* 6. Ball Marker */}
          <BallMarker x={currentFrame.ball.x} y={currentFrame.ball.y} speed={currentFrame.ball.speed} />
        </FootballPitch>
      </div>

      {/* Replay Controls & Overlays Panel */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 flex flex-col gap-4">
          <ReplayControls
            totalFrames={frames.length}
            currentTimestamp={currentFrame.t}
          />
          <TogglePanel />
        </div>

        <div>
          <ExplanationPanel sequence={sequence} />
        </div>
      </div>
    </div>
  );
};
