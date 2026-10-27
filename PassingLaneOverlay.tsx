import React from 'react';
import { toSVGCoords } from './FootballPitch';
import { PassingLane, PlayerPosition } from '../../types';

interface PassingLaneOverlayProps {
  lanes: PassingLane[];
  players: PlayerPosition[];
}

export const PassingLaneOverlay: React.FC<PassingLaneOverlayProps> = ({ lanes, players }) => {
  const playerMap = new Map(players.map((p) => [p.player_id, p]));

  return (
    <g>
      {lanes.map((lane, i) => {
        const fromP = playerMap.get(lane.from_player);
        const toP = playerMap.get(lane.to_player);
        if (!fromP || !toP) return null;

        const p1 = toSVGCoords(fromP.x, fromP.y);
        const p2 = toSVGCoords(toP.x, toP.y);

        const isBlocked = lane.blocked;
        const color = isBlocked ? '#EF4444' : '#39D353';
        const strokeWidth = Math.max(2, Math.min(8, (lane.width || 1.5) * 3));

        return (
          <g key={i} opacity="0.75">
            {/* Outer corridor glow */}
            <line
              x1={p1.svgX}
              y1={p1.svgY}
              x2={p2.svgX}
              y2={p2.svgY}
              stroke={color}
              strokeWidth={strokeWidth * 2}
              strokeOpacity="0.2"
              strokeLinecap="round"
            />
            {/* Core passing line */}
            <line
              x1={p1.svgX}
              y1={p1.svgY}
              x2={p2.svgX}
              y2={p2.svgY}
              stroke={color}
              strokeWidth={strokeWidth}
              strokeDasharray={isBlocked ? '6 4' : 'none'}
              strokeLinecap="round"
            />
          </g>
        );
      })}
    </g>
  );
};
