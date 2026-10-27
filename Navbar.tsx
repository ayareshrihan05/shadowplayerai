import React from 'react';
import { NavLink, Link } from 'react-router-dom';
import { PlayCircle, Eye, GitCompare, UserCheck, FileText, Settings, Activity } from 'lucide-react';
import { SyntheticLabel } from '../shared/SyntheticLabel';
import { useAppStore } from '../../store/appStore';

export const Navbar: React.FC = () => {
  const currentMatchId = useAppStore((s) => s.currentMatchId);
  const setCurrentMatchId = useAppStore((s) => s.setCurrentMatchId);

  const navItems = [
    { to: '/', label: 'Dashboard', icon: Activity },
    { to: '/match', label: 'Match View', icon: Eye },
    { to: '/replay', label: 'Impact Replay', icon: PlayCircle },
    { to: '/counterfactual', label: 'Counterfactual', icon: GitCompare },
    { to: '/profile', label: 'Shadow Profile', icon: UserCheck },
    { to: '/report', label: 'Scouting Report', icon: FileText },
    { to: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <header className="bg-surface border-b border-border-subtle sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* Brand */}
        <Link to="/" className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-accent-green/10 border border-accent-green/40 flex items-center justify-center font-bold text-accent-green">
            SP
          </div>
          <div>
            <div className="font-bold text-white tracking-tight leading-none text-base">
              ShadowPlayer <span className="text-accent-green font-mono text-sm">AI</span>
            </div>
            <div className="text-[11px] text-slate-300 hidden sm:block">
              Reveal the football nobody sees
            </div>
          </div>
        </Link>

        {/* Navigation Links */}
        <nav className="hidden md:flex items-center gap-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                    isActive
                      ? 'bg-surface-elevated text-accent-green font-semibold border border-border-subtle'
                      : 'text-text-secondary hover:text-text-primary hover:bg-surface-elevated/50'
                  }`
                }
              >
                <Icon size={15} />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>

        {/* Right side: Match Switcher + Synthetic Label */}
        <div className="flex items-center gap-3">
          <div className="flex items-center bg-surface-elevated p-1 rounded-lg border border-border-subtle text-xs">
            <button
              onClick={() => setCurrentMatchId('match-men-001')}
              className={`px-2.5 py-1 rounded text-xs font-semibold transition-all ${
                currentMatchId !== 'match-women-001'
                  ? 'bg-team-northvale text-white shadow-sm'
                  : 'text-text-secondary hover:text-text-primary'
              }`}
            >
              Men's PL
            </button>
            <button
              onClick={() => setCurrentMatchId('match-women-001')}
              className={`px-2.5 py-1 rounded text-xs font-semibold transition-all ${
                currentMatchId === 'match-women-001'
                  ? 'bg-accent-magenta text-white shadow-sm'
                  : 'text-text-secondary hover:text-text-primary'
              }`}
            >
              Women's WSL
            </button>
          </div>
          <SyntheticLabel className="hidden sm:inline-flex" />
        </div>
      </div>
    </header>
  );
};
