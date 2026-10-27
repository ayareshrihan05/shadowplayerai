import React from 'react';
import { toSVGCoords } from './FootballPitch';

interface PlayerMarkerProps {
  x: number;
  y: number;
  playerId: string;
  name?: string;
  jerseyNumber?: number;
  position?: string;
  teamId?: string;
  isInPossession?: boolean;
  isFocusPlayer?: boolean;
  speed?: number;
  onClick?: () => void;
}

export const PlayerMarker: React.FC<PlayerMarkerProps> = ({
  x,
  y,
  playerId,
  name,
  jerseyNumber,
  position,
  teamId = '',
  isInPossession = false,
  isFocusPlayer = false,
  onClick,
}) => {
  const { svgX, svgY } = toSVGCoords(x, y);

  const isNorthvale = teamId.includes('northvale') || parseInt(playerId.replace('p', '')) <= 11;
  const fillColor = isNorthvale ? '#4299E1' : '#F0B429';
  const label = jerseyNumber !== undefined ? jerseyNumber.toString() : (position || playerId);

  return (
    <g
      className="cursor-pointer transition-transform duration-100 ease-out"
      onClick={onClick}
      aria-label={`Player ${name || playerId}, position ${position || ''}, team ${isNorthvale ? 'Northvale FC' : 'Eastmere City'}`}
    >
      {/* Focus player pulse ring */}
      {isFocusPlayer && (
        <circle
          cx={svgX}
          cy={svgY}
          r={26}
          fill="none"
          stroke="#39D353"
          strokeWidth="2.5"
          strokeDasharray="4 2"
          opacity="0.8"
        >
          <animate
            attributeName="r"
            values="22;30;22"
            dur="2s"
            repeatCount="indefinite"
          />
          <animate
            attributeName="opacity"
            values="0.9;0.3;0.9"
            dur="2s"
            repeatCount="indefinite"
          />
        </circle>
      )}

      {/* Possession halo */}
      {isInPossession && (
        <circle
          cx={svgX}
          cy={svgY}
          r={20}
          fill="none"
          stroke="#FFFFFF"
          strokeWidth="3"
          opacity="0.95"
        />
      )}

      {/* Main player circle */}
      <circle
        cx={svgX}
        cy={svgY}
        r={14}
        fill={fillColor}
        stroke="#0D1117"
        strokeWidth="2"
      />

      {/* Number/position text */}
      <text
        x={svgX}
        y={svgY + 4}
        textAnchor="middle"
        fontSize="10"
        fontWeight="bold"
        fill="#FFFFFF"
        fontFamily="JetBrains Mono, monospace"
        pointerEvents="none"
      >
        {label}
      </text>

      {/* Focus label tag above player */}
      {isFocusPlayer && (
        <g>
          <rect
            x={svgX - 35}
            y={svgY - 30}
            width={70}
            height={16}
            rx={3}
            fill="#161B22"
            stroke="#39D353"
            strokeWidth="1"
            opacity="0.9"
          />
          <text
            x={svgX}
            y={svgY - 18}
            textAnchor="middle"
            fontSize="9"
            fontWeight="bold"
            fill="#39D353"
          >
            FOCUS
          </text>
        </g>
      )}
    </g>
  );
};
