/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        radar: {
          50: '#f0f4ff',
          100: '#e0eaff',
          500: '#3b82f6',
          600: '#2563eb',
          900: '#0f172a',
          950: '#030712',
        },
      },
    },
  },
  plugins: [],
};
