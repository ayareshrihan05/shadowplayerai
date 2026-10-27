import React from 'react';
import { toSVGCoords } from './FootballPitch';

interface Point {
  x: number;
  y: number;
}

interface TrajectoryTrailProps {
  points: Point[];
  color?: string;
  strokeWidth?: number;
}

export const TrajectoryTrail: React.FC<TrajectoryTrailProps> = ({
  points,
  color = '#39D353',
  strokeWidth = 3,
}) => {
  if (points.length < 2) return null;

  return (
    <g opacity="0.85">
      {points.slice(1).map((pt, i) => {
        const prev = points[i];
        const p1 = toSVGCoords(prev.x, prev.y);
        const p2 = toSVGCoords(pt.x, pt.y);
        // Older segments have lower opacity
        const opacity = 0.2 + (i / points.length) * 0.8;

        return (
          <line
            key={i}
            x1={p1.svgX}
            y1={p1.svgY}
            x2={p2.svgX}
            y2={p2.svgY}
            stroke={color}
            strokeWidth={strokeWidth}
            strokeOpacity={opacity}
            strokeLinecap="round"
            strokeDasharray="4 2"
          />
        );
      })}
    </g>
  );
};
