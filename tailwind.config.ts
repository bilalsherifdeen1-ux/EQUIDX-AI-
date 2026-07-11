import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#070B0A",
          900: "#0B1210",
          800: "#101A17",
          700: "#182622",
          600: "#22332E",
        },
        signal: {
          400: "#5EF0B8",
          500: "#3DDC97",
          600: "#28B57C",
        },
        amber: {
          400: "#F2B84B",
          500: "#DE9C2C",
        },
        mist: {
          100: "#EAF2EF",
          300: "#B9C9C3",
          500: "#7E9691",
        },
      },
      fontFamily: {
        display: ["var(--font-display)", "sans-serif"],
        body: ["var(--font-body)", "sans-serif"],
        mono: ["var(--font-mono)", "monospace"],
      },
      backgroundImage: {
        "trace-grid":
          "linear-gradient(to right, rgba(61,220,151,0.06) 1px, transparent 1px), linear-gradient(to bottom, rgba(61,220,151,0.06) 1px, transparent 1px)",
      },
    },
  },
  plugins: [],
};
export default config;
