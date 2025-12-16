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
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6', // Matches favicon primary blue
          600: '#2563eb',
          700: '#1d4ed8', // Matches favicon gradient end
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554',
        },
      },
    },
  },
  plugins: [],
  safelist: [
    'bg-primary-500',
    'bg-primary-700',
    'text-primary-500',
    'text-primary-700',
    'hover:bg-primary-700',
    'hover:text-primary-500',
    'hover:text-primary-700',
    'focus:ring-primary-500',
    'border-primary-500',
  ],
}
