import React from 'react';

interface ConfidenceBadgeProps {
  confidence: number;
  className?: string;
}

export const ConfidenceBadge: React.FC<ConfidenceBadgeProps> = ({ confidence, className = '' }) => {
  let label = 'Low';
  let colorStyles = 'bg-red-500/10 border-red-500/30 text-red-400';

  if (confidence >= 0.75) {
    label = 'High';
    colorStyles = 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400';
  } else if (confidence >= 0.5) {
    label = 'Medium';
    colorStyles = 'bg-amber-500/10 border-amber-500/30 text-amber-400';
  }

  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-mono font-medium border ${colorStyles} ${className}`}
      title={`Confidence rating based on criteria match percentage (${(confidence * 100).toFixed(0)}%)`}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-current opacity-70" />
      <span>{label} ({(confidence * 100).toFixed(0)}%)</span>
    </span>
  );
};
