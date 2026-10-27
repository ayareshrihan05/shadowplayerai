import React from 'react';
import { SequenceDetail } from '../../types';
import { ConfidenceBadge } from '../shared/ConfidenceBadge';
import { Sparkles, ShieldAlert } from 'lucide-react';

interface ExplanationPanelProps {
  sequence: SequenceDetail;
}

export const ExplanationPanel: React.FC<ExplanationPanelProps> = ({ sequence }) => {
  const explanation = sequence.ai_explanation;
  const detection = sequence.movement_detections[0];

  return (
    <div className="bg-surface border border-border-subtle rounded-xl p-5 flex flex-col gap-4">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <span className="text-xs font-mono uppercase tracking-wider text-accent-green">
            {sequence.sequence_id} • {detection ? detection.movement_type.replace('_', ' ') : 'Tactical Sequence'}
          </span>
          <h2 className="text-lg font-bold text-text-primary mt-0.5">{sequence.name}</h2>
        </div>
        {detection && <ConfidenceBadge confidence={detection.confidence} />}
      </div>

      {/* AI Explanation Narrative */}
      <div className="bg-surface-elevated/70 border border-border-subtle rounded-lg p-4">
        <div className="flex items-center gap-2 mb-2 text-xs font-semibold text-text-secondary">
          <Sparkles size={14} className="text-accent-green" />
          <span>AI Tactical Explanation</span>
          <span className="text-text-muted font-mono ml-auto">
            via {explanation.generation_method === 'ms_foundry' ? 'Microsoft Foundry' : 'Deterministic Engine'}
          </span>
        </div>
        <p className="text-sm text-text-primary leading-relaxed">{explanation.text}</p>
      </div>

      {/* SIS Component Breakdown Chips */}
      {detection && detection.sis_components && (
        <div>
          <h4 className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-2">
            Estimated Impact Breakdown
          </h4>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            <div className="bg-surface-elevated border border-border-subtle rounded-lg p-2.5 text-center">
              <span className="text-xs text-text-muted block">Space (S)</span>
              <span className="text-base font-bold text-metric-space">
                {detection.sis_components.S.toFixed(1)}
              </span>
            </div>
            <div className="bg-surface-elevated border border-border-subtle rounded-lg p-2.5 text-center">
              <span className="text-xs text-text-muted block">Lane (P)</span>
              <span className="text-base font-bold text-metric-lane">
                {detection.sis_components.P.toFixed(1)}
              </span>
            </div>
            <div className="bg-surface-elevated border border-border-subtle rounded-lg p-2.5 text-center">
              <span className="text-xs text-text-muted block">Defense (D)</span>
              <span className="text-base font-bold text-metric-defense">
                {detection.sis_components.D.toFixed(1)}
              </span>
            </div>
            <div className="bg-surface-elevated border border-border-subtle rounded-lg p-2.5 text-center">
              <span className="text-xs text-text-muted block">Chain (C)</span>
              <span className="text-base font-bold text-metric-chain">
                {detection.sis_components.C.toFixed(1)}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Supporting Evidence Event IDs */}
      {explanation.evidence_refs && explanation.evidence_refs.length > 0 && (
        <div className="flex flex-wrap items-center gap-1.5 text-xs text-text-secondary">
          <span className="text-text-muted">Evidence citations:</span>
          {explanation.evidence_refs.map((ref) => (
            <span
              key={ref}
              className="px-2 py-0.5 rounded bg-surface-elevated border border-border-subtle font-mono text-xs text-text-secondary hover:text-accent-green hover:border-accent-green transition-colors cursor-pointer"
            >
              {ref}
            </span>
          ))}
        </div>
      )}

      {/* Disclaimer */}
      <div className="text-[11px] text-text-muted flex items-center gap-1.5 pt-2 border-t border-border-subtle/50">
        <ShieldAlert size={12} className="text-amber-500/80 flex-shrink-0" />
        <span>{explanation.disclaimer}</span>
      </div>
    </div>
  );
};
