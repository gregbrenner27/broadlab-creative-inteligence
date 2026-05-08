/** @type {import('tailwindcss').Config} */
// This file configures Tailwind CSS — the utility class system used for all styling.
// We extend the default Tailwind colours to include Broadlab's specific brand colours.
export default {
  // Tell Tailwind which files to scan for class names
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      // Broadlab brand colours — use these as: bg-broadlab-dark, text-broadlab-red, etc.
      colors: {
        broadlab: {
          dark: "#0d0d0d",        // primary background
          card: "#1a1a1a",        // card/panel background
          border: "#2a2a2a",      // subtle borders
          muted: "#333333",       // muted backgrounds
          grey: "#a0a0a0",        // secondary text
          white: "#ffffff",       // primary text
          red: "#e63946",         // accent colour — buttons, highlights
          "red-hover": "#c1121f", // darker red for hover states
          "red-muted": "#e6394620" // very faint red for backgrounds
        }
      },
      // Broadlab uses Inter font — clean and legible
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"]
      },
      // Custom animation for the progress steps lighting up
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "fade-in": "fadeIn 0.3s ease-in-out"
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" }
        }
      }
    }
  },
  plugins: []
}
