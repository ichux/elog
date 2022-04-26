/// <reference types="vite/client" />

import path from "path";
import { defineConfig } from "vite";

export default defineConfig({
  build: {
    outDir: "../static",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, "src/main"),
        elog: path.resolve(__dirname, "src/elog"),
      },
      output: {
        format: "es",
        assetFileNames: "css/[name].css", // cause we only have css files as assets
        entryFileNames: "js/[name].js",
      },
    },
  
}});
