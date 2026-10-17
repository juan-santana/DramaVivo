import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
      '/cdn-proxy': {
        target: 'https://cdn.dramashorts.io',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/cdn-proxy/, ''),
        headers: {
          Referer: 'https://dramashorts.io/',
          Origin: 'https://dramashorts.io',
        },
      },
    },
  },
})
