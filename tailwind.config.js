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
        concert: "url('/static/img/backgrounds/concert.png')",
        'concert-mobile': "url('/static/img/backgrounds/concert_mobile.png')",
        'concert-blur': "url('/static/img/backgrounds/blur_trim_concert.png')",
        'ticket-outline': "url('/static/img/icons/ticket-outline.svg')",
        'dark-rectangle-line':
          "url('/static/img/background_dark_rectangle.png')",
        'categories-event': "url('/static/img/background_categories.png')",
        'categories-cinema': "url('/static/img/categories/cinema.png')",
        'categories-festival': "url('/static/img/categories/festival.png')",
        'categories-shows': "url('/static/img/categories/shows.png')",
        'categories-sport': "url('/static/img/categories/sport.png')",
        'categories-theatre': "url('/static/img/categories/theatre.png')",
        'review-people': "url('/static/img/reviews_people.png')",
        'slider-rio': "url('/static/img/slider/rio.png')",
        'slider-san-paulo': "url('/static/img/slider/san_paulo.png')",
        'slider-rio': "url('/static/img/slider/florianopolis.png')",
      },
      borderRadius: {
        '50%': '50%',
      },
      colors: ({colors}) => ({
        primary: '#fff',
        secondary: '#f2b705',
        black: '#1c1c1c',
        'ultra-black': '#151515',
        'light-grey-a9': '#a9a9a9',
        'light-grey-b0': '#b0b0b0',
        'light-grey-82': '#828282',
        'light-grey': '#cecece',
        grey: '#99a1a3',
        'grey-41': '#414141',
        'middle-grey': '#5a5a5a',
        'dark-grey': '#2c2c2c',
      }),
      fontFamily: {
        body: ['Space Grotesk', 'sans-serif'],
      },
      height: ({theme}) => ({
        264: '264px',
        448: '448px',
        475: '475px',
        517: '517px',
        600: '600px',
        650: '650px',
        700: '700px',
      }),
      lineHeight: {
        0.1: '0.1rem',
      },
      margin: ({theme}) => ({
        '50%': '50%',
      }),
      maxWidth: () => ({
        265: '265px',
      }),
      top: ({theme}) => ({
        '60%': '50%',
      }),
      width: ({theme}) => ({
        295: '295px',
        500: '500px',
        728: '728px',
      }),
      zIndex: {
        auto: 'auto',
        60: '60',
      },
    },
  },
  plugins: [require('flowbite/plugin')],
};
