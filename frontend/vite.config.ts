import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import svgr from "vite-plugin-svgr";
import mkcert from "vite-plugin-mkcert";

export default defineConfig({
  plugins: [
    svgr({
      include: "**/*.svg?react",
    }),
    react(),
    mkcert(),
  ],
  base: "/",
  preview: {
    host: true,
    port: 5173,
  },
  server: {
    https: true,
    host: true,
  },
  resolve: {
    alias: {
      src: "/src",
    },
  },
});
