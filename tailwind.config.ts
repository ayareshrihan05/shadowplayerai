import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        page: '#0D1117',
        canvas: '#0D1117',
        surface: {
          DEFAULT: '#161B22',
          elevated: '#21262D',
          hover: '#282E37',
        },
        border: {
          subtle: '#30363D',
          focus: '#58A6FF',
        },
        pitch: {
          DEFAULT: '#1A3C2E',
          lines: '#2D6A4F',
          grass: '#143325',
          penalty: '#19392B',
        },
        team: {
          northvale: '#4299E1',
          eastmere: '#F0B429',
        },
        metric: {
          space: '#39D353',
          lane: '#38BDF8',
          defense: '#FB7185',
          chain: '#A78BFA',
        },
        accent: {
          green: '#39D353',
          amber: '#F59E0B',
          red: '#EF4444',
          blue: '#3B82F6',
          magenta: '#EC4899',
        },
        // Direct color shortcuts
        primary: '#FFFFFF',
        secondary: '#CBD5E1',
        muted: '#94A3B8',
        // Grouped text colors (enables text-text-primary, text-text-secondary, text-text-muted)
        text: {
          primary: '#FFFFFF',
          secondary: '#CBD5E1',
          muted: '#94A3B8',
        },
      },
      backgroundColor: {
        base: '#0D1117',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace'],
      },
    },
  },
  plugins: [],
} satisfies Config;
