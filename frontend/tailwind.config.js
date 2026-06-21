/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        obsidian: '#0B0F17',
        slateBorder: '#1E293B',
        neonCyan: '#00F0FF',
        sunsetOrange: '#FF4500',
        glassBg: 'rgba(255, 255, 255, 0.03)',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      boxShadow: {
        glowCyan: '0 0 20px rgba(0, 240, 255, 0.2)',
      }
    },
  },
  plugins: [],
}
