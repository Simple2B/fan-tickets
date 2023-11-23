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
        'categories-event': "url('/static/img/background_categories.png')",
        'categories-cinema': "url('/static/img/categories/cinema.png')",
        'categories-festival': "url('/static/img/categories/festival.png')",
        'categories-shows': "url('/static/img/categories/shows.png')",
        'categories-sport': "url('/static/img/categories/sport.png')",
        'categories-theatre': "url('/static/img/categories/theatre.png')",
        'review-people': "url('/static/img/reviews_people.png')",
        footer: "url('/static/img/background_footer.png')",
      },
      borderRadius: {
        '50%': '50%',
      },
      colors: ({colors}) => ({
        primary: '#fff',
        secondary: '#f2b705',
        black: '#1c1c1c',
        'ultra-black': '#151515',
        'light-grey': '#a9a9a9',
        grey: '#99a1a3',
        'middle-grey': '#5a5a5a',
        'dark-grey': '#2c2c2c',
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
