module.exports = {
  mode: 'jit',
  important: true,
  content: [
    './index.html',
    './src/**/*.{js,ts}',
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
