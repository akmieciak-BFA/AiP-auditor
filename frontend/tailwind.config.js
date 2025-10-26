/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#e6ffe6',
          100: '#ccffcc',
          200: '#99ff99',
          300: '#66ff66',
          400: '#33ff33',
          500: '#00ff00',
          600: '#00cc00',
          700: '#009900',
          800: '#006600',
          900: '#003300',
        },
        dark: {
          50: '#f5f5f7',
          100: '#e8e9ed',
          200: '#d1d3db',
          300: '#9ea2b3',
          400: '#666d87',
          500: '#4a5166',
          600: '#383e54',
          700: '#2d3561',
          800: '#1a1d3a',
          900: '#0d0e1f',
        },
      },
    },
  },
  plugins: [],
}
