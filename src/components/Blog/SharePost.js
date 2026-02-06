"use client";
import React, { useState } from "react";
import { ShareFill, Check, Clipboard } from "react-bootstrap-icons";
import siteMetadata from "@/src/utils/siteMetaData";

const SharePost = ({ slug, title, description }) => {
  const [copied, setCopied] = useState(false);
  const url = `${siteMetadata.siteUrl}/blogs/${slug}`;

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: title,
          text: description,
          url: url,
        });
      } catch (error) {
        console.error("Error sharing:", error);
      }
    } else {
      try {
        await navigator.clipboard.writeText(url);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      } catch (err) {
        console.error("Failed to copy:", err);
      }
    }
  };

  return (
    <button
      onClick={handleShare}
      className="m-3 flex items-center gap-2 hover:scale-105 transition-all duration-200 cursor-pointer"
      aria-label="Compartilhar post"
      title="Compartilhar"
    >
      {copied ? (
        <>
          <Check className="w-5 h-5" />
          <span>Copiado!</span>
        </>
      ) : (
        <>
          <ShareFill className="w-4 h-4" />
          <span>Compartilhar</span>
        </>
      )}
    </button>
  );
};

export default SharePost;
