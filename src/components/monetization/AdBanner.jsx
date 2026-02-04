"use client";

import React from "react";
import { useMonetization } from "./MonetizationContext";
import Link from "next/link";

const AdBanner = ({ placement = "header" }) => {
  const { isSupporter } = useMonetization();

  const adPushed = React.useRef(false);

  React.useEffect(() => {
    if (!isSupporter && !adPushed.current) {
      try {
        const ads = document.getElementsByClassName("adsbygoogle");
        // Check if the last ad slot is already filled (has children) to avoid "already has ads" error
        if (ads.length > 0) {
             const lastAd = ads[ads.length - 1];
             if (lastAd.innerHTML.trim() === "") {
                 (window.adsbygoogle = window.adsbygoogle || []).push({});
                 adPushed.current = true;
             }
        }
      } catch (err) {
        console.error("AdSense error:", err);
      }
    }
  }, [isSupporter]);

  // If user is a supporter, do not show ads
  if (isSupporter) {
    return null;
  }

  // Styles based on placement
  const styles = {
    header: "w-full h-24 bg-gray-100 dark:bg-gray-800 flex items-center justify-center my-4 rounded-md border border-gray-200 dark:border-gray-700",
    sidebar: "w-full h-64 bg-gray-100 dark:bg-gray-800 flex items-center justify-center my-4 rounded-md border border-gray-200 dark:border-gray-700",
    "article-bottom": "w-full h-32 bg-gray-100 dark:bg-gray-800 flex items-center justify-center my-8 rounded-md border border-gray-200 dark:border-gray-700",
    content: "w-full h-auto min-h-[250px] bg-gray-50 dark:bg-gray-900 flex items-center justify-center my-8 rounded-md border border-gray-200 dark:border-gray-700",
  };



  return (
    <div className={styles[placement]}>
      <div className="text-center w-full">
         <ins className="adsbygoogle"
             style={{ display: 'block' }}
             data-ad-client="ca-pub-5240361910984411"
             data-ad-slot="7697822611"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
      </div>
    </div>
  );
};

export default AdBanner;
