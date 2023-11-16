/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './app/templates/**/*.html',
    './src/js/**/*.js',
    './node_modules/flowbite/**/*.js',
  ],
  theme: {
    extend: {
      backgroundImage: {
        concert: "url('/static/img/concert.png')",
        'concert-blur': "url('/static/img/concert-blur.png')",
        'ticket-outline': "url('/static/img/ticket-outline.svg')",
        'dark-rectangle-line':
          "url('/static/img/background_dark_rectangle.png')",
      },
      colors: ({colors}) => ({
        primary: colors.blue,
        secondary: '#f2b705',
      }),
      height: ({theme}) => ({
        600: '600px',
        264: '264px',
      }),
      width: ({theme}) => ({
        728: '728px',
      }),
    },
  },
  plugins: [require('flowbite/plugin')],
};
