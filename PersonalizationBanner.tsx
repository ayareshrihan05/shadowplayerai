import React from 'react';
import { useAppStore } from '../../store/appStore';
import { SlidersHorizontal } from 'lucide-react';

export const PersonalizationBanner: React.FC = () => {
  const tier = useAppStore((s) => s.tier);
  const setTier = useAppStore((s) => s.setTier);

  const tierLabels = {
    casual: 'Casual Fan Mode',
    analyst: 'Tactical Analyst Mode',
    coach: 'Coach & Scout Mode',
  };

  return (
    <div className="bg-surface-elevated/80 border-b border-border-subtle py-1.5 px-4 text-xs flex items-center justify-between">
      <div className="flex items-center gap-2">
        <SlidersHorizontal size={13} className="text-accent-green" />
        <span className="text-text-muted">Viewing experience:</span>
        <span className="font-semibold text-text-primary">{tierLabels[tier]}</span>
      </div>
      <div className="flex items-center gap-2">
        {(['casual', 'analyst', 'coach'] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTier(t)}
            className={`px-2.5 py-0.5 rounded text-[11px] font-semibold transition-colors ${
              tier === t
                ? 'bg-emerald-600 text-white font-bold shadow-sm'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>
    </div>
  );
};
