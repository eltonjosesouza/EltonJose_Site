"use client";

import React, { createContext, useContext, useEffect, useState } from "react";

const MonetizationContext = createContext({
  isSupporter: false,
  becomeSupporter: () => {},
});

export const useMonetization = () => useContext(MonetizationContext);

export const MonetizationProvider = ({ children }) => {
  const [isSupporter, setIsSupporter] = useState(false);

  useEffect(() => {
    // Check local storage on mount
    const storedStatus = localStorage.getItem("isSupporter");
    if (storedStatus === "true") {
      setIsSupporter(true);
    }
  }, []);

  const becomeSupporter = () => {
    setIsSupporter(true);
    localStorage.setItem("isSupporter", "true");
  };

  return (
    <MonetizationContext.Provider value={{ isSupporter, becomeSupporter }}>
      {children}
    </MonetizationContext.Provider>
  );
};
