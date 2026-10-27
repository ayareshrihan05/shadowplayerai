import React from 'react';
import { toSVGCoords } from './FootballPitch';

interface BallMarkerProps {
  x: number;
  y: number;
  speed?: number;
}

export const BallMarker: React.FC<BallMarkerProps> = ({ x, y }) => {
  const { svgX, svgY } = toSVGCoords(x, y);

  return (
    <g aria-label="Football location">
      {/* Ball shadow */}
      <ellipse
        cx={svgX + 2}
        cy={svgY + 3}
        rx={7}
        ry={4}
        fill="#000000"
        opacity="0.4"
      />
      {/* Ball circle */}
      <circle
        cx={svgX}
        cy={svgY}
        r={7}
        fill="#FFFFFF"
        stroke="#161B22"
        strokeWidth="1.5"
      />
      {/* Pattern details */}
      <circle cx={svgX} cy={svgY} r={2.5} fill="#161B22" />
    </g>
  );
};
