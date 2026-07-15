export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        pitch: "#0B2F24",
        fifa: "#0F766E",
        signal: "#F5C451",
        night: "#08111F"
      },
      boxShadow: { panel: "0 14px 40px rgba(0,0,0,.18)" }
    }
  },
  plugins: []
};
