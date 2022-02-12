import React, { createContext, useState } from "react";

const ColorContext = createContext(undefined);
const ColorDispatchContext = createContext(undefined);

function ColorProvider({ children }) {
  // create the state, which will be employed by the color context provider
  const [colorTheme, setColorTheme] = useState(colorThemes.main);

  return (
    <ColorContext.Provider value={colorTheme}>
      <ColorDispatchContext.Provider value={setColorTheme}>
        {/* This refers to all children. This will be wrapped around all pages in the app. */}
        {children}
      </ColorDispatchContext.Provider>
    </ColorContext.Provider>
  );
}

export { ColorContext, ColorDispatchContext, ColorProvider };

const colorThemes = {
  main: {
    primaryBackground: "#1a2f4b",
    primaryBackgroundTwo: "#122034",
    secondaryBackground: "#28475C",
    secondaryBackgroundShadow: "#08172c",
    primaryButton: "#2F8886",
    primaryButtonOutline: "#0F6866",
    primaryButtonHover: "#0F6866",
    primaryButtonAltHover: "#1d5a59",
    primaryButtonHoverOutline: "#094846",
    secondaryButton: "#84C69B",
    secondaryButtonHover: "#54966B",
    primaryHighlights: "#A4E6BB",
    primaryText: "#FFFFFF",
    primaryError: "#D72000",
    primaryErrorHover: "#972000",
    primaryInputOutline: "#68879c",
    primaryButtonHighlight: "#FFF",
  },
};
