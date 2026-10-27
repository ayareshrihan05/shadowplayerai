import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import { MatchDetail, MatchInsights } from '../types';
import { LoadingSpinner } from '../components/shared/LoadingSpinner';
import { SyntheticLabel } from '../components/shared/SyntheticLabel';
import { ConfidenceBadge } from '../components/shared/ConfidenceBadge';
import { useAppStore } from '../store/appStore';
import { PlayCircle, GitCompare, Trophy, ArrowRight, Shield, Zap } from 'lucide-react';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const currentMatchId = useAppStore((s) => s.currentMatchId);
  const setCurrentMatchId = useAppStore((s) => s.setCurrentMatchId);
  const setSelectedPlayerId = useAppStore((s) => s.setSelectedPlayerId);
  const setSelectedSequenceId = useAppStore((s) => s.setSelectedSequenceId);

  const [matchDetail, setMatchDetail] = useState<MatchDetail | null>(null);
  const [insights, setInsights] = useState<MatchInsights | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const isWomenMatch = currentMatchId === 'match-women-001';

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [detailData, insightsData] = await Promise.all([
          api.getMatchDetail(currentMatchId),
          api.getMatchInsights(currentMatchId),
        ]);
        setMatchDetail(detailData);
        setInsights(insightsData);
      } catch (err: any) {
        setError(err.message || 'Failed to load match dashboard');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [currentMatchId]);

  if (loading) return <LoadingSpinner message="Calculating Shadow Impact Scores across 5,400 synthetic seconds..." />;
  if (error || !matchDetail) {
    return (
      <div className="p-8 text-center text-red-400">
        <p className="font-semibold">Error: {error || 'Match not found'}</p>
        <button
          onClick={() => window.location.reload()}
          className="mt-4 px-4 py-2 bg-surface-elevated border border-border-subtle rounded-lg text-text-primary"
        >
          Retry
        </button>
      </div>
    );
  }

  const handlePlayerClick = (playerId: string) => {
    setSelectedPlayerId(playerId);
    navigate('/profile');
  };

  const handleSequenceClick = (sequenceId: string) => {
    setSelectedSequenceId(sequenceId);
    navigate('/replay');
  };

  const scenarios = isWomenMatch
    ? [
        {
          id: 'SEQ-002',
          title: 'The Overlapping Override',
          player: 'Rosa Fernandez (w010)',
          role: 'LB • Northvale FC Women',
          metric: '+14.3 m² Space Created',
          desc: 'High overlap run forces defensive shift, unlocking flank crossing option and penalty box isolation.',
        },
        {
          id: 'SEQ-004',
          title: 'The Blindside Channel Run',
          player: 'Mara Okonkwo (w002)',
          role: 'LW • Northvale FC Women',
          metric: '+14.5 m² Space Created',
          desc: 'Blindside diagonal cut draws Eastmere centre-back away, opening a 27m passing channel.',
        },
      ]
    : [
        {
          id: 'SEQ-001',
          title: 'The Decoy Diagonal',
          player: 'James Holloway (p001)',
          role: 'ST • Northvale FC',
          metric: '+12.8 m² Space Created',
          desc: 'Diagonal run pulls opposition CB away, opening central corridor for CAM pass.',
        },
        {
          id: 'SEQ-003',
          title: 'The Press Cascade',
          player: 'Felix Ayo (p004)',
          role: 'CM • Northvale FC',
          metric: 'Turnover Forced',
          desc: 'Aggressive central pressing angle forces hurried backward pass and defensive recovery.',
        },
      ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 flex flex-col gap-8">
      {/* Hero Banner */}
      <div className="relative overflow-hidden bg-gradient-to-r from-surface via-surface-elevated to-surface border border-border-subtle rounded-2xl p-6 sm:p-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="flex flex-col gap-2 max-w-2xl">
            <SyntheticLabel className="w-fit" />
            <h1 className="text-3xl sm:text-4xl font-extrabold text-text-primary tracking-tight">
              Reveal the football <span className="text-accent-green">nobody sees</span>.
            </h1>
            <p className="text-text-secondary text-sm sm:text-base leading-relaxed">
              Traditional statistics record what happens on the ball. ShadowPlayer AI calculates,
              measures, and explains the 97% of match contributions made off the ball through
              synthetic tracking data and AI explainability.
            </p>
          </div>

          {/* Quick Match Card */}
          <div className="bg-surface/90 border border-border-subtle rounded-xl p-4 flex flex-col gap-3 min-w-[280px]">
            <div className="flex items-center justify-between text-xs text-text-muted font-mono">
              <span className="uppercase">{matchDetail.match_id}</span>
              <span className="text-accent-green">FT 90:00</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="text-left">
                <span className={`font-bold block ${isWomenMatch ? 'text-accent-magenta' : 'text-team-northvale'}`}>
                  {matchDetail.home_team.name.replace(" [FICTIONAL]", "")}
                </span>
                <span className="text-xs text-text-muted">4-3-3 • Home</span>
              </div>
              <div className="text-xl font-bold font-mono text-text-primary px-3 py-1 bg-surface-elevated rounded border border-border-subtle">
                {isWomenMatch ? '3 - 1' : '2 - 1'}
              </div>
              <div className="text-right">
                <span className="font-bold text-team-eastmere block">
                  {matchDetail.away_team.name.replace(" [FICTIONAL]", "")}
                </span>
                <span className="text-xs text-text-muted">4-4-2 • Away</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Match Selection Prompt Card */}
      <div className="bg-surface border border-border-subtle rounded-2xl p-6 flex flex-col gap-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <span className="text-xs font-mono uppercase tracking-wider text-accent-green">
              Match Environment Selector
            </span>
            <h2 className="text-xl font-bold text-text-primary">
              Which Match Do You Want To Analyze?
            </h2>
            <p className="text-xs text-text-secondary">
              Professional football maintains separate competitions. Choose between our gender-focused synthetic matches.
              All replays, tactical profiles, and AI reports will sync to your choice.
            </p>
          </div>
          <span className="text-xs font-mono text-text-muted bg-surface-elevated px-3 py-1 rounded-full border border-border-subtle w-fit">
            Active: {isWomenMatch ? "Women's Super League" : "Men's Premier League"}
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Men's Match Card */}
          <div
            onClick={() => setCurrentMatchId('match-men-001')}
            className={`cursor-pointer rounded-xl p-5 border transition-all flex flex-col justify-between ${
              !isWomenMatch
                ? 'bg-surface-elevated border-team-northvale shadow-lg shadow-team-northvale/10 ring-2 ring-team-northvale/30'
                : 'bg-surface border-border-subtle hover:border-border-focus'
            }`}
          >
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="px-2.5 py-0.5 rounded text-xs font-bold uppercase tracking-wider bg-team-northvale/10 text-team-northvale border border-team-northvale/30">
                  Men's Premier League
                </span>
                {!isWomenMatch ? (
                  <span className="text-xs font-bold text-team-northvale flex items-center gap-1">
                    ● Viewing Active Match
                  </span>
                ) : (
                  <span className="text-xs text-text-muted">Click to view</span>
                )}
              </div>
              <h3 className="text-lg font-bold text-text-primary">Northvale FC vs Eastmere City</h3>
              <p className="text-xs text-text-secondary mt-1">
                22 male players • Featuring James Holloway (ST), Felix Ayo (CM), Tom Reeves (CAM)
              </p>
              <div className="flex items-center gap-2 mt-3 text-xs font-mono text-text-muted">
                <span className="bg-surface px-2 py-1 rounded border border-border-subtle">Decoy Diagonal (SEQ-001)</span>
                <span className="bg-surface px-2 py-1 rounded border border-border-subtle">Press Cascade (SEQ-003)</span>
              </div>
            </div>
            <div className="mt-4 pt-3 border-t border-border-subtle/50 flex items-center justify-between text-xs">
              <span className="text-text-muted">Final Score: 2 - 1</span>
              <span className={`font-semibold ${!isWomenMatch ? 'text-team-northvale' : 'text-text-secondary'}`}>
                {!isWomenMatch ? 'Currently Selected' : 'Switch to Men\'s Match →'}
              </span>
            </div>
          </div>

          {/* Women's Match Card */}
          <div
            onClick={() => setCurrentMatchId('match-women-001')}
            className={`cursor-pointer rounded-xl p-5 border transition-all flex flex-col justify-between ${
              isWomenMatch
                ? 'bg-surface-elevated border-accent-magenta shadow-lg shadow-accent-magenta/10 ring-2 ring-accent-magenta/30'
                : 'bg-surface border-border-subtle hover:border-border-focus'
            }`}
          >
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="px-2.5 py-0.5 rounded text-xs font-bold uppercase tracking-wider bg-accent-magenta/10 text-accent-magenta border border-accent-magenta/30">
                  Women's Super League
                </span>
                {isWomenMatch ? (
                  <span className="text-xs font-bold text-accent-magenta flex items-center gap-1">
                    ● Viewing Active Match
                  </span>
                ) : (
                  <span className="text-xs text-text-muted">Click to view</span>
                )}
              </div>
              <h3 className="text-lg font-bold text-text-primary">Northvale FC Women vs Eastmere City Women</h3>
              <p className="text-xs text-text-secondary mt-1">
                22 female players • Featuring Mara Okonkwo (LW), Rosa Fernandez (LB), Maya Lindqvist (ST)
              </p>
              <div className="flex items-center gap-2 mt-3 text-xs font-mono text-text-muted">
                <span className="bg-surface px-2 py-1 rounded border border-border-subtle">Overlapping Run (SEQ-002)</span>
                <span className="bg-surface px-2 py-1 rounded border border-border-subtle">Blindside Channel (SEQ-004)</span>
              </div>
            </div>
            <div className="mt-4 pt-3 border-t border-border-subtle/50 flex items-center justify-between text-xs">
              <span className="text-text-muted">Final Score: 3 - 1</span>
              <span className={`font-semibold ${isWomenMatch ? 'text-accent-magenta' : 'text-text-secondary'}`}>
                {isWomenMatch ? 'Currently Selected' : 'Switch to Women\'s Match →'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Flagship Scenarios Showcase */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-xl font-bold text-text-primary flex items-center gap-2">
              <Zap className="text-accent-green" size={20} />
              Flagship Off-Ball Tactical Sequences
            </h2>
            <p className="text-xs text-text-secondary">
              Hand-crafted scenario benchmarks showcasing off-ball impact with synchronized replays.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {scenarios.map((sc) => (
            <div
              key={sc.id}
              className="bg-surface border border-border-subtle rounded-xl p-5 flex flex-col justify-between hover:border-border-focus transition-all group"
            >
              <div>
                <div className="flex items-center justify-between text-xs font-mono text-text-muted mb-2">
                  <span className="text-accent-green font-semibold">{sc.id}</span>
                  <span className="px-2 py-0.5 rounded bg-surface-elevated border border-border-subtle text-accent-green font-bold">
                    {sc.metric}
                  </span>
                </div>
                <h3 className="text-base font-bold text-text-primary group-hover:text-accent-green transition-colors">
                  {sc.title}
                </h3>
                <span className="text-xs text-text-muted block mt-0.5">{sc.player} • {sc.role}</span>
                <p className="text-xs text-text-secondary mt-3 leading-relaxed">{sc.desc}</p>
              </div>

              <div className="flex items-center gap-2 mt-5 pt-3 border-t border-border-subtle">
                <button
                  onClick={() => handleSequenceClick(sc.id)}
                  className="flex-1 flex items-center justify-center gap-1.5 py-2 px-3 rounded-lg bg-surface-elevated hover:bg-accent-green hover:text-white border border-border-subtle text-xs font-medium transition-colors"
                >
                  <PlayCircle size={15} />
                  <span>Inspect Replay</span>
                </button>
                <button
                  onClick={() => {
                    setSelectedSequenceId(sc.id);
                    navigate('/counterfactual');
                  }}
                  className="flex items-center justify-center p-2 rounded-lg bg-surface-elevated hover:bg-surface-hover border border-border-subtle text-text-secondary hover:text-text-primary transition-colors"
                  title="Compare Counterfactual"
                >
                  <GitCompare size={16} />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* SIS Leaderboard Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Full Roster Leaderboard (2 Cols) */}
        <div className="lg:col-span-2 bg-surface border border-border-subtle rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-lg font-bold text-text-primary flex items-center gap-2">
                <Trophy className="text-accent-amber" size={18} />
                Shadow Impact Score (SIS) Leaderboard
              </h2>
              <span className="text-xs text-text-muted">
                Experimental metric: SIS = 0.35S + 0.25P + 0.20D + 0.20C (0–100 normalized)
              </span>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-surface-elevated text-text-muted border-b border-border-subtle">
                <tr>
                  <th className="py-2.5 px-3 font-semibold">Rank</th>
                  <th className="py-2.5 px-3 font-semibold">Player</th>
                  <th className="py-2.5 px-3 font-semibold">Pos</th>
                  <th className="py-2.5 px-3 font-semibold text-right">SIS</th>
                  <th className="py-2.5 px-3 font-semibold text-center">Confidence</th>
                  <th className="py-2.5 px-3 font-semibold text-center">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-subtle/50 font-mono">
                {matchDetail.sis_leaderboard.map((entry, idx) => (
                  <tr
                    key={entry.player_id}
                    className="hover:bg-surface-elevated/50 transition-colors group"
                  >
                    <td className="py-2.5 px-3 text-text-muted">{idx + 1}</td>
                    <td className="py-2.5 px-3 font-sans font-medium text-text-primary group-hover:text-accent-green">
                      {entry.name}
                    </td>
                    <td className="py-2.5 px-3 text-text-secondary">{entry.position}</td>
                    <td className="py-2.5 px-3 text-right font-bold text-accent-green">
                      {entry.sis.toFixed(1)}
                    </td>
                    <td className="py-2.5 px-3 text-center">
                      <ConfidenceBadge confidence={entry.confidence} />
                    </td>
                    <td className="py-2.5 px-3 text-center">
                      <button
                        onClick={() => handlePlayerClick(entry.player_id)}
                        className="p-1 rounded hover:bg-surface-elevated text-text-muted hover:text-text-primary transition-colors"
                        title="View Shadow Profile"
                      >
                        <ArrowRight size={14} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Team SIS Comparison Sidebar */}
        <div className="flex flex-col gap-6">
          <div className="bg-surface border border-border-subtle rounded-xl p-5">
            <h3 className="text-sm font-bold text-text-primary mb-3 flex items-center gap-2">
              <Shield size={16} className="text-text-muted" />
              Team Off-Ball Aggregates
            </h3>

            {insights?.team_sis_summary && (
              <div className="flex flex-col gap-4">
                <div className="bg-surface-elevated border border-border-subtle rounded-lg p-3">
                  <div className="flex items-center justify-between text-xs mb-1">
                    <span className="font-bold text-team-northvale">Northvale FC</span>
                    <span className="font-mono font-bold text-accent-green">
                      {insights.team_sis_summary['team-northvale-fc']?.avg_sis} avg SIS
                    </span>
                  </div>
                  <span className="text-[11px] text-text-muted block">
                    Top contributor: {insights.team_sis_summary['team-northvale-fc']?.top_player}
                  </span>
                </div>

                <div className="bg-surface-elevated border border-border-subtle rounded-lg p-3">
                  <div className="flex items-center justify-between text-xs mb-1">
                    <span className="font-bold text-team-eastmere">Eastmere City</span>
                    <span className="font-mono font-bold text-accent-amber">
                      {insights.team_sis_summary['team-eastmere-city']?.avg_sis} avg SIS
                    </span>
                  </div>
                  <span className="text-[11px] text-text-muted block">
                    Top contributor: {insights.team_sis_summary['team-eastmere-city']?.top_player}
                  </span>
                </div>
              </div>
            )}
          </div>

          {/* Metric Guide Box */}
          <div className="bg-surface border border-border-subtle rounded-xl p-5">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-3">
              Understanding SIS Components
            </h3>
            <ul className="text-xs text-text-secondary flex flex-col gap-2.5">
              <li className="flex items-start gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-metric-space mt-1 flex-shrink-0" />
                <div>
                  <strong className="text-text-primary">Space Creation (35%):</strong> How movement creates viable territorial space for teammates.
                </div>
              </li>
              <li className="flex items-start gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-metric-lane mt-1 flex-shrink-0" />
                <div>
                  <strong className="text-text-primary">Passing Lanes (25%):</strong> Clear passing corridors opened or protected without interception.
                </div>
              </li>
              <li className="flex items-start gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-metric-defense mt-1 flex-shrink-0" />
                <div>
                  <strong className="text-text-primary">Defensive Support (20%):</strong> Tracking opponent runs and sealing central channels.
                </div>
              </li>
              <li className="flex items-start gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-metric-chain mt-1 flex-shrink-0" />
                <div>
                  <strong className="text-text-primary">Chain Reaction (20%):</strong> Downstream goals, shots, or turnovers generated within 10 seconds.
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
