import React, { useEffect, useState } from 'react';
import { useAppStore } from '../store/appStore';
import { api } from '../api/client';
import { PersonalizationTier } from '../types';
import { Check, ShieldCheck, Server, Sliders } from 'lucide-react';

export const Settings: React.FC = () => {
  const tier = useAppStore((s) => s.tier);
  const setTier = useAppStore((s) => s.setTier);

  const [health, setHealth] = useState<any>(null);
  const [checking, setChecking] = useState(false);

  useEffect(() => {
    async function checkHealth() {
      try {
        setChecking(true);
        const h = await api.getHealth();
        setHealth(h);
      } catch (e: any) {
        setHealth({ status: 'unreachable', error: e.message });
      } finally {
        setChecking(false);
      }
    }
    checkHealth();
  }, []);

  const tiers: Array<{
    id: PersonalizationTier;
    title: string;
    description: string;
    audience: string;
  }> = [
    {
      id: 'casual',
      title: 'Casual Fan Mode',
      description: 'Clear, approachable narratives focusing on the human impact of off-ball work. Metric jargon is translated into visual insights.',
      audience: 'Supporters who want to understand overlooked brilliance without technical overload.',
    },
    {
      id: 'analyst',
      title: 'Tactical Analyst Mode',
      description: 'Full numeric breakdowns including coordinates, corridor widths in meters, Voronoi control percentages, and confidence bands.',
      audience: 'Data scientists, tactical bloggers, and analytics enthusiasts.',
    },
    {
      id: 'coach',
      title: 'Coach & Scout Mode',
      description: 'Structured tactical summaries, training interventions, positional discipline audits, and comparable role profiles.',
      audience: 'Coaching staff and technical scouts evaluating off-ball work rate and tactical discipline.',
    },
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 flex flex-col gap-8">
      <div>
        <span className="text-xs font-mono uppercase tracking-wider text-accent-green">Configuration</span>
        <h1 className="text-2xl font-bold text-text-primary">Platform Settings</h1>
        <p className="text-xs text-text-secondary mt-1">
          Adjust viewing preferences and inspect backend status.
        </p>
      </div>

      {/* Personalization Tier Selection Cards */}
      <div className="flex flex-col gap-4">
        <h2 className="text-sm font-bold uppercase tracking-wider text-text-muted flex items-center gap-2">
          <Sliders size={16} />
          Choose Personalization Experience
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {tiers.map((t) => (
            <div
              key={t.id}
              onClick={() => setTier(t.id)}
              className={`p-5 rounded-xl border cursor-pointer transition-all flex flex-col justify-between ${
                tier === t.id
                  ? 'bg-surface-elevated border-accent-green shadow-lg shadow-accent-green/5'
                  : 'bg-surface border-border-subtle hover:border-border-focus'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-bold text-sm text-text-primary">{t.title}</h3>
                  {tier === t.id && (
                    <span className="w-5 h-5 rounded-full bg-accent-green text-white flex items-center justify-center">
                      <Check size={12} strokeWidth={3} />
                    </span>
                  )}
                </div>
                <p className="text-xs text-text-secondary leading-relaxed mb-3">{t.description}</p>
              </div>

              <div className="pt-3 border-t border-border-subtle/50 text-[11px] text-text-muted">
                Best for: {t.audience}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Backend Operational Status */}
      <div className="bg-surface border border-border-subtle rounded-xl p-6 flex flex-col gap-4">
        <h2 className="text-sm font-bold text-text-primary flex items-center gap-2">
          <Server size={16} className="text-accent-green" />
          Backend Diagnostics
        </h2>

        {checking ? (
          <span className="text-xs text-text-muted">Testing API connection...</span>
        ) : health ? (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
            <div className="bg-surface-elevated border border-border-subtle rounded-lg p-3">
              <span className="text-text-muted block">API Status</span>
              <span className="font-bold font-mono text-accent-green">
                {health.status?.toUpperCase() || 'OK'}
              </span>
            </div>
            <div className="bg-surface-elevated border border-border-subtle rounded-lg p-3">
              <span className="text-text-muted block">Database Cache</span>
              <span className="font-bold font-mono text-accent-green">
                {health.database_connected ? 'CONNECTED & SEEDED' : 'DISCONNECTED'}
              </span>
            </div>
            <div className="bg-surface-elevated border border-border-subtle rounded-lg p-3">
              <span className="text-text-muted block">AI Narrative Mode</span>
              <span className="font-bold font-mono text-accent-amber">
                {health.ai_fallback_mode ? 'DETERMINISTIC FALLBACK' : 'MICROSOFT FOUNDRY'}
              </span>
            </div>
          </div>
        ) : (
          <span className="text-xs text-red-400">Failed to connect to backend.</span>
        )}
      </div>

      {/* Hackathon Compliance & Synthetic Data Disclosures */}
      <div className="bg-surface border border-border-subtle rounded-xl p-6 flex flex-col gap-3">
        <h2 className="text-sm font-bold text-text-primary flex items-center gap-2">
          <ShieldCheck size={16} className="text-accent-green" />
          Hackathon Compliance & Synthetic Data Integrity
        </h2>
        <ul className="text-xs text-text-secondary flex flex-col gap-2 leading-relaxed">
          <li>
            • <strong>Synthetic Data Only:</strong> All coordinates, teams (Northvale FC, Eastmere City), and players (p001–p022) are fictional constructs designed specifically for demonstration.
          </li>
          <li>
            • <strong>Traceable Analytics:</strong> All metrics (Space Creation, Passing Lane, Defensive Support, Chain Reaction) are deterministically calculated using geometry algorithms rather than invented by an LLM.
          </li>
          <li>
            • <strong>Experimental Labeling:</strong> Shadow Impact Score (SIS) formula (0.35S + 0.25P + 0.20D + 0.20C) is a prototype proof-of-concept metric.
          </li>
        </ul>
      </div>
    </div>
  );
};
