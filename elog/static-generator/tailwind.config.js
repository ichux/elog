module.exports = {
  mode: 'jit',
  important: true,
  content: [
    './index.html',
    './src/**/*.{js,ts,svg}',
    '../templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  safelist: [
    { pattern: /bg-(red|green|slate)-.*/ }
  ],
  plugins: [],
}
