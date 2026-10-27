import React from 'react';

export const toSVGCoords = (x: number, y: number) => ({
  svgX: x * 10,
  svgY: (68 - y) * 10,
});

interface FootballPitchProps {
  children?: React.ReactNode;
  width?: string | number;
  height?: string | number;
  className?: string;
}

export const FootballPitch: React.FC<FootballPitchProps> = ({
  children,
  width = '100%',
  height = '100%',
  className = '',
}) => {
  return (
    <div className={`relative w-full overflow-hidden rounded-xl border border-border-subtle bg-pitch ${className}`}>
      <svg
        viewBox="0 0 1050 680"
        className="w-full h-auto select-none block"
        style={{ width, height, aspectRatio: '1050 / 680' }}
      >
        <defs>
          {/* Subtle grass striping */}
          <pattern id="pitch-stripes" width="105" height="680" patternUnits="userSpaceOnUse">
            <rect x="0" y="0" width="52.5" height="680" fill="#143325" />
            <rect x="52.5" y="0" width="52.5" height="680" fill="#1A3C2E" />
          </pattern>
          {/* Arrowhead marker for defender arrows */}
          <marker
            id="arrowhead-red"
            markerWidth="8"
            markerHeight="8"
            refX="6"
            refY="3"
            orient="auto"
          >
            <polygon points="0 0, 8 3, 0 6" fill="#EF4444" />
          </marker>
          <marker
            id="arrowhead-blue"
            markerWidth="8"
            markerHeight="8"
            refX="6"
            refY="3"
            orient="auto"
          >
            <polygon points="0 0, 8 3, 0 6" fill="#38BDF8" />
          </marker>
          <marker
            id="arrowhead-green"
            markerWidth="8"
            markerHeight="8"
            refX="6"
            refY="3"
            orient="auto"
          >
            <polygon points="0 0, 8 3, 0 6" fill="#39D353" />
          </marker>
        </defs>

        {/* Pitch Background */}
        <rect width="1050" height="680" fill="url(#pitch-stripes)" />

        {/* Pitch Markings Group */}
        <g stroke="#2D6A4F" strokeWidth="2.5" fill="none" strokeOpacity="0.85">
          {/* Outer Boundary */}
          <rect x="15" y="15" width="1020" height="650" rx="4" />

          {/* Halfway Line */}
          <line x1="525" y1="15" x2="525" y2="665" />

          {/* Centre Circle (9.15m radius = 91.5px) */}
          <circle cx="525" cy="340" r="91.5" />
          {/* Centre Spot */}
          <circle cx="525" cy="340" r="3" fill="#2D6A4F" />

          {/* Left Penalty Area (16.5m depth = 165px, 40.3m height = 403px, centered at 340) */}
          <rect x="15" y="138.5" width="165" height="403" />
          {/* Left Goal Area (5.5m depth = 55px, 18.3m height = 183px) */}
          <rect x="15" y="248.5" width="55" height="183" />
          {/* Left Penalty Spot (11m = 110px from goal line) */}
          <circle cx="125" cy="340" r="3" fill="#2D6A4F" />
          {/* Left Penalty Arc */}
          <path d="M 180 285 A 91.5 91.5 0 0 1 180 395" />

          {/* Right Penalty Area */}
          <rect x="870" y="138.5" width="165" height="403" />
          {/* Right Goal Area */}
          <rect x="980" y="248.5" width="55" height="183" />
          {/* Right Penalty Spot */}
          <circle cx="925" cy="340" r="3" fill="#2D6A4F" />
          {/* Right Penalty Arc */}
          <path d="M 870 285 A 91.5 91.5 0 0 0 870 395" />

          {/* Corner Arcs (1m radius = 10px) */}
          <path d="M 15 25 A 10 10 0 0 0 25 15" />
          <path d="M 15 655 A 10 10 0 0 1 25 665" />
          <path d="M 1035 25 A 10 10 0 0 1 1025 15" />
          <path d="M 1035 655 A 10 10 0 0 0 1025 665" />
        </g>

        {/* Dynamic elements layer */}
        {children}
      </svg>
    </div>
  );
};
