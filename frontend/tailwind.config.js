/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        orbitron: ['Orbitron', 'sans-serif'], // Add Orbitron to the font family list
      },
      fontWeight: {
        regular: 400, // Regular weight
        bold: 700,    // Bold weight
      },
    },
  },
  plugins: [],

}