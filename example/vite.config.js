import { defineConfig } from "vite";

export default defineConfig({
  server: {
    port: 9999,
  },
  build: {
    manifest: true,
    outDir: "static/vite/dist",
    rollupOptions: {
      input: [
        // files imported via vite_import go here
        "static/main.ts",
        "static/styles.scss",
      ],
    },
  },
});
