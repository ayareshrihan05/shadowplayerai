import React from 'react';
import { toSVGCoords } from './FootballPitch';

interface DefenderArrowProps {
  startX: number;
  startY: number;
  endX: number;
  endY: number;
  color?: string;
  label?: string;
}

export const DefenderArrow: React.FC<DefenderArrowProps> = ({
  startX,
  startY,
  endX,
  endY,
  color = '#EF4444',
  label,
}) => {
  const p1 = toSVGCoords(startX, startY);
  const p2 = toSVGCoords(endX, endY);

  const markerId = color === '#39D353' ? 'url(#arrowhead-green)' : color === '#38BDF8' ? 'url(#arrowhead-blue)' : 'url(#arrowhead-red)';

  return (
    <g opacity="0.9">
      <line
        x1={p1.svgX}
        y1={p1.svgY}
        x2={p2.svgX}
        y2={p2.svgY}
        stroke={color}
        strokeWidth="3"
        strokeLinecap="round"
        markerEnd={markerId}
      />
      {label && (
        <text
          x={(p1.svgX + p2.svgX) / 2}
          y={(p1.svgY + p2.svgY) / 2 - 8}
          fill={color}
          fontSize="10"
          fontWeight="bold"
          textAnchor="middle"
          className="select-none"
        >
          {label}
        </text>
      )}
    </g>
  );
};
