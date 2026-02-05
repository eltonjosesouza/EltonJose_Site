"use client";

import React from "react";
import { useMonetization } from "./MonetizationContext";
import { usePathname } from "next/navigation";

const AdBanner = ({ placement = "header" }) => {
  const { isSupporter } = useMonetization();
  const pathname = usePathname();

  const adPushed = React.useRef(false);

  React.useEffect(() => {
    if (!isSupporter && !adPushed.current) {
// ... existing logic ...
    }
  }, [isSupporter]);

  // If user is a supporter OR on excluded routes, do not show ads
  const excludedRoutes = ['/login', '/signup'];
  const isExcluded = excludedRoutes.includes(pathname) || pathname?.startsWith('/admin');

  if (isSupporter || isExcluded) {
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
