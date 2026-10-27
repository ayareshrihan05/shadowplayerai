import React from 'react';
import { Play, Pause, RotateCcw } from 'lucide-react';
import { useAppStore } from '../../store/appStore';

interface ReplayControlsProps {
  totalFrames: number;
  currentTimestamp: number;
}

export const ReplayControls: React.FC<ReplayControlsProps> = ({
  totalFrames,
  currentTimestamp,
}) => {
  const isPlaying = useAppStore((s) => s.replay.isPlaying);
  const currentFrameIndex = useAppStore((s) => s.replay.currentFrameIndex);
  const playbackSpeed = useAppStore((s) => s.replay.playbackSpeed);
  const togglePlay = useAppStore((s) => s.togglePlay);
  const resetReplay = useAppStore((s) => s.resetReplay);
  const setCurrentFrameIndex = useAppStore((s) => s.setCurrentFrameIndex);
  const setPlaybackSpeed = useAppStore((s) => s.setPlaybackSpeed);

  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <div className="bg-surface border border-border-subtle rounded-xl p-4 flex flex-col gap-3">
      {/* Top Bar: Play/Pause, Reset, Time indicator, Speed buttons */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <button
            onClick={togglePlay}
            className="flex items-center justify-center w-10 h-10 rounded-lg bg-emerald-600 text-white font-bold hover:bg-emerald-500 transition-colors focus:outline-none focus:ring-2 focus:ring-accent-green shadow-sm"
            aria-label={isPlaying ? 'Pause replay' : 'Play replay'}
          >
            {isPlaying ? <Pause size={20} /> : <Play size={20} className="ml-0.5" />}
          </button>

          <button
            onClick={resetReplay}
            className="flex items-center justify-center w-10 h-10 rounded-lg bg-surface-elevated text-text-primary hover:bg-surface-hover border border-border-subtle transition-colors focus:outline-none focus:ring-2 focus:ring-border-focus"
            aria-label="Reset replay to start"
          >
            <RotateCcw size={18} />
          </button>

          <div className="ml-2 font-mono text-sm text-text-secondary">
            <span className="text-accent-green font-semibold">{formatTime(currentTimestamp)}</span>
            <span className="mx-1 text-text-muted">/</span>
            <span>Frame {currentFrameIndex + 1} of {totalFrames}</span>
          </div>
        </div>

        {/* Speed Selector */}
        <div className="flex items-center gap-1 bg-surface-elevated p-1 rounded-lg border border-border-subtle text-xs">
          {[0.25, 0.5, 1, 2].map((spd) => (
            <button
              key={spd}
              onClick={() => setPlaybackSpeed(spd)}
              className={`px-2.5 py-1 rounded font-mono transition-colors ${
                playbackSpeed === spd
                  ? 'bg-emerald-600 text-white font-bold shadow-sm'
                  : 'text-text-secondary hover:text-text-primary'
              }`}
            >
              {spd}x
            </button>
          ))}
        </div>
      </div>

      {/* Timeline Slider */}
      <div className="flex items-center gap-3">
        <input
          type="range"
          min={0}
          max={Math.max(0, totalFrames - 1)}
          value={currentFrameIndex}
          onChange={(e) => setCurrentFrameIndex(Number(e.target.value))}
          className="w-full h-2 bg-surface-elevated rounded-lg appearance-none cursor-pointer accent-accent-green focus:outline-none"
          aria-label="Replay timeline progress"
        />
      </div>
    </div>
  );
};
