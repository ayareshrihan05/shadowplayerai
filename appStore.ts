import { create } from 'zustand';
import { PersonalizationTier } from '../types';

export interface ReplayState {
  isPlaying: boolean;
  currentFrameIndex: number;
  playbackSpeed: number;
  showTrails: boolean;
  showDefenders: boolean;
  showPassingLanes: boolean;
  showSpaceZones: boolean;
  showCounterfactual: boolean;
}

interface AppStore {
  currentMatchId: string;
  selectedPlayerId: string;
  selectedSequenceId: string;
  tier: PersonalizationTier;
  replay: ReplayState;
  
  setCurrentMatchId: (id: string) => void;
  setSelectedPlayerId: (id: string) => void;
  setSelectedSequenceId: (id: string) => void;
  setTier: (tier: PersonalizationTier) => void;
  
  // Replay actions
  setIsPlaying: (playing: boolean) => void;
  togglePlay: () => void;
  setCurrentFrameIndex: (idx: number) => void;
  setPlaybackSpeed: (speed: number) => void;
  toggleTrails: () => void;
  toggleDefenders: () => void;
  togglePassingLanes: () => void;
  toggleSpaceZones: () => void;
  toggleCounterfactual: () => void;
  resetReplay: () => void;
}

export const useAppStore = create<AppStore>((set) => ({
  currentMatchId: 'match-men-001',
  selectedPlayerId: 'p001',
  selectedSequenceId: 'SEQ-001',
  tier: 'analyst',
  
  replay: {
    isPlaying: false,
    currentFrameIndex: 0,
    playbackSpeed: 1,
    showTrails: true,
    showDefenders: true,
    showPassingLanes: true,
    showSpaceZones: true,
    showCounterfactual: false,
  },

  setCurrentMatchId: (id) => {
    const isWomen = id === 'match-women-001';
    set({
      currentMatchId: id,
      selectedPlayerId: isWomen ? 'w002' : 'p001',
      selectedSequenceId: isWomen ? 'SEQ-002' : 'SEQ-001',
    });
  },
  setSelectedPlayerId: (id) => set({ selectedPlayerId: id }),
  setSelectedSequenceId: (id) => set({ selectedSequenceId: id }),
  setTier: (tier) => set({ tier }),

  setIsPlaying: (playing) => set((s) => ({ replay: { ...s.replay, isPlaying: playing } })),
  togglePlay: () => set((s) => ({ replay: { ...s.replay, isPlaying: !s.replay.isPlaying } })),
  setCurrentFrameIndex: (idx) => set((s) => ({ replay: { ...s.replay, currentFrameIndex: idx } })),
  setPlaybackSpeed: (speed) => set((s) => ({ replay: { ...s.replay, playbackSpeed: speed } })),
  toggleTrails: () => set((s) => ({ replay: { ...s.replay, showTrails: !s.replay.showTrails } })),
  toggleDefenders: () => set((s) => ({ replay: { ...s.replay, showDefenders: !s.replay.showDefenders } })),
  togglePassingLanes: () => set((s) => ({ replay: { ...s.replay, showPassingLanes: !s.replay.showPassingLanes } })),
  toggleSpaceZones: () => set((s) => ({ replay: { ...s.replay, showSpaceZones: !s.replay.showSpaceZones } })),
  toggleCounterfactual: () => set((s) => ({ replay: { ...s.replay, showCounterfactual: !s.replay.showCounterfactual } })),
  resetReplay: () => set((s) => ({ replay: { ...s.replay, currentFrameIndex: 0, isPlaying: false } })),
}));
