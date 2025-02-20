import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tailwindcss from '@tailwindcss/vite'
import { TanStackRouterVite } from '@tanstack/router-plugin/vite'

import path from 'path'

export default defineConfig({
  root: __dirname,
  cacheDir: "./node_modules/.vite/.",
  envDir: path.join(__dirname, "..", "..", ".."),
  plugins: [
    tailwindcss(),
    TanStackRouterVite(),
    react(),
  ],
  resolve: {
    alias: {
        "@core": path.resolve(__dirname, "src", "core"),
    },
  },
})
