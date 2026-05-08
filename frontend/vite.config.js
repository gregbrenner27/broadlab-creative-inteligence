import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite is the build tool that compiles and serves the React frontend.
// This config sets up the development server and tells it where the backend API is.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Proxy: any request from the frontend starting with /api gets forwarded
    // to the backend server at port 8000. This prevents CORS issues in development.
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
