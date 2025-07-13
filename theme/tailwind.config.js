module.exports = {
  content: [
    '../templates/**/*.html',
    './src/**/*.{js,css}',
  ],
  theme: {
    extend: {
      colors: {
        ozon: {
          DEFAULT: '#005BFF',
          dark: '#0041C4',
          light: '#F6F6F6',
        },
        osimi: {
          DEFAULT: '#FF6B35',
          dark: '#E85A2B', 
          light: '#FF8A5B',
          bright: '#FF4500',
        },
      },
      fontFamily: {
        sans: ['"Nunito Sans"', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
