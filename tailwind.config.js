const colors = {
  mystic: "#e4e9ef",
  sail: "#b3d4fc",
  azure: "#0e7ee0",
  blueBayoux: "rgba(67,93,122,0.95)",

  // Monochrome
  mineShaft: "#222222",
  silver: "#cccccc",
  shuttleGray: "#5a6470",
};

module.exports = {
  theme: {
    fontFamily: {
      display: ["Helvetica", "Arial", "sans-serif"],
      body: ["Helvetica", "Arial", "sans-serif"],
    },
    extend: {
      colors: {
        body: colors.mineShaft,
        link: colors.azure,
        ...colors,
      },
      fontSize: {
        "3xl": "1.75rem",
      },
      maxWidth: {
        container: "1200px",
      },
    },
  },
  variants: {
    opacity: ["responsive", "hover", "focus", "group-hover"],
  },
  plugins: [],
};
