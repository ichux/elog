/// <reference types="vite/client" />

import { resolve } from "path";
import { defineConfig } from "vite";
import eslintPlugin from "vite-plugin-eslint";

export default defineConfig({
  build: {
    sourcemap: false,
    outDir: "../static",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, "src/main"),
        elog: resolve(__dirname, "src/elog"),
        auth: resolve(__dirname, "src/auth"),
      },
      output: {
        format: "es",
        assetFileNames: "css/[name].css", // because we only have css files as assets
        entryFileNames: "js/[name].js",
      },
    },
  },
  plugins: [eslintPlugin()]
});
