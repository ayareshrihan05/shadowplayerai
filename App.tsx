import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Navbar } from './components/layout/Navbar';
import { PersonalizationBanner } from './components/shared/PersonalizationBanner';
import { Dashboard } from './pages/Dashboard';
import { MatchView } from './pages/MatchView';
import { PlayerProfile } from './pages/PlayerProfile';
import { ReplayView } from './pages/ReplayView';
import { CounterfactualView } from './pages/CounterfactualView';
import { ScoutingReport } from './pages/ScoutingReport';
import { Settings } from './pages/Settings';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-base text-text-primary flex flex-col font-sans">
        <Navbar />
        <PersonalizationBanner />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/match" element={<MatchView />} />
            <Route path="/profile" element={<PlayerProfile />} />
            <Route path="/replay" element={<ReplayView />} />
            <Route path="/counterfactual" element={<CounterfactualView />} />
            <Route path="/report" element={<ScoutingReport />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <footer className="border-t border-border-subtle py-4 text-center text-xs text-text-muted bg-surface/50">
          ShadowPlayer AI • Premier League Hackathon Edition • All data is synthetic and fictional.
        </footer>
      </div>
    </BrowserRouter>
  );
};

export default App;
