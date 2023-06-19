/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {
      boxShadow:{
        'full': '0 0 5px rgba(0,0,0,0.5)'
      }
    },
  },
  plugins: [],
}

