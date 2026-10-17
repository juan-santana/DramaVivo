import typography from '@tailwindcss/typography'

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#0a0a0f',
        surface: {
          DEFAULT: '#14141f',
          light: '#1e1e2d',
          lighter: '#28283d',
          border: 'rgba(255, 255, 255, 0.08)',
        },
        primary: {
          DEFAULT: '#e50914',
          hover: '#f40612',
          light: '#ff3344',
          dark: '#b20710',
        },
        secondary: {
          DEFAULT: '#f5c518',
          hover: '#e2b616',
          light: '#ffd700',
        },
        text: {
          main: '#ffffff',
          muted: '#a0a0b0',
          dim: '#6b6b7b',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      boxShadow: {
        'glow-primary': '0 0 20px -3px rgba(229, 9, 20, 0.4)',
        'glow-secondary': '0 0 20px -3px rgba(245, 197, 24, 0.35)',
        'glow-card': '0 8px 30px rgba(0, 0, 0, 0.8)',
      },
      backgroundImage: {
        'hero-gradient': 'linear-gradient(to top, #0a0a0f 10%, rgba(10, 10, 15, 0.8) 50%, rgba(10, 10, 15, 0.2) 100%)',
      },
      aspectRatio: {
        '9/16': '9 / 16',
        '2/3': '2 / 3',
      }
    },
  },
  plugins: [
    typography,
  ],
}
