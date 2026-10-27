import React from 'react';
import { AlertTriangle } from 'lucide-react';

interface SyntheticLabelProps {
  label?: string;
  className?: string;
}

export const SyntheticLabel: React.FC<SyntheticLabelProps> = ({
  label = 'SYNTHETIC DATA — FICTIONAL PLAYERS',
  className = '',
}) => {
  return (
    <div
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-mono tracking-wide ${className}`}
      title="All tracking coordinates, players, events, and metrics in ShadowPlayer AI are synthetic and fictional."
    >
      <AlertTriangle size={13} className="text-amber-400 flex-shrink-0" />
      <span>{label}</span>
    </div>
  );
};
