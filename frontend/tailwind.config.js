/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'comedy-primary': '#6366f1',
        'comedy-secondary': '#ec4899',
        'comedy-accent': '#f59e0b',
        'comedy-dark': '#1f2937',
        'comedy-light': '#f8fafc',
        'ring': '#6366f1',
      },
      animation: {
        'bounce-subtle': 'bounce 2s infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [],
}