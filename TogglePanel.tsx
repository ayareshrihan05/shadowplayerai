import React from 'react';
import { useAppStore } from '../../store/appStore';

export const TogglePanel: React.FC = () => {
  const replay = useAppStore((s) => s.replay);
  const toggleTrails = useAppStore((s) => s.toggleTrails);
  const toggleDefenders = useAppStore((s) => s.toggleDefenders);
  const togglePassingLanes = useAppStore((s) => s.togglePassingLanes);
  const toggleSpaceZones = useAppStore((s) => s.toggleSpaceZones);
  const toggleCounterfactual = useAppStore((s) => s.toggleCounterfactual);

  const toggles = [
    { label: 'Movement Trails', active: replay.showTrails, toggle: toggleTrails, color: 'bg-accent-green' },
    { label: 'Defender Response', active: replay.showDefenders, toggle: toggleDefenders, color: 'bg-metric-defense' },
    { label: 'Passing Lanes', active: replay.showPassingLanes, toggle: togglePassingLanes, color: 'bg-metric-lane' },
    { label: 'Open Space Zones', active: replay.showSpaceZones, toggle: toggleSpaceZones, color: 'bg-metric-space' },
    { label: 'Counterfactual Mode', active: replay.showCounterfactual, toggle: toggleCounterfactual, color: 'bg-accent-amber' },
  ];

  return (
    <div className="bg-surface border border-border-subtle rounded-xl p-4">
      <h3 className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-3">
        Visualization Overlays
      </h3>
      <div className="flex flex-wrap gap-2">
        {toggles.map((item) => (
          <button
            key={item.label}
            role="switch"
            aria-checked={item.active}
            onClick={item.toggle}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-medium transition-all ${
              item.active
                ? 'bg-surface-elevated border-border-focus text-text-primary shadow-sm'
                : 'bg-surface border-border-subtle text-text-secondary opacity-60 hover:opacity-90'
            }`}
          >
            <span
              className={`w-2 h-2 rounded-full ${item.active ? item.color : 'bg-text-muted'}`}
            />
            {item.label}
          </button>
        ))}
      </div>
    </div>
  );
};
