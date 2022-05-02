# Elog
## Static Assets Generator

This directory represents a Vite project to generate assets for Elog UI.

### Setup
Assuming you have already cloned the repository and you're inside it.
```bash
cd elog/static-generator
pnpm install # Or npm or yarn
pnpm build
```

This will build and generate CSS, JS assets in `elog/static` directory (from project root).

If you're developing and want to watch for changes and rebuild while working, use `pnpm build:watch` instead.

`AlpineJs` is used for interactions and `TailwindCSS` for styling.