
"use client";

import React from "react";
import { useMonetization } from "./MonetizationContext";

const SupporterCTA = () => {
  const { isSupporter } = useMonetization();

  if (isSupporter) {
    return (
      <div className="p-4 bg-green-100 dark:bg-green-900 rounded-lg text-center my-8">
        <p className="font-bold text-green-700 dark:text-green-300">
          🎉 Você é um apoiador! Obrigado por manter este site sem anúncios.
        </p>
      </div>
    );
  }

  return (
    <div className="p-6 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 my-8 text-center shadow-sm">
      <h3 className="text-xl font-bold mb-4 text-dark dark:text-light">Apoie meu trabalho com um Pix ⚡</h3>
      <p className="mb-6 text-gray-600 dark:text-white max-w-md mx-auto">
        Gostou do conteúdo? Mande um Pix para ajudar a manter o blog no ar e garantir novos artigos.
      </p>

      {/* LivePix Widget */}
      <div className="flex justify-center mb-6">
        <iframe
            src="https://widget.livepix.gg/embed/02c288d6-4dc3-42d8-8329-4b3c6914c596"
            width="300"
            height="320"
            className="border-none rounded-lg overflow-hidden"
            title="LivePix QR Code"
        ></iframe>
      </div>

      <div className="flex flex-col items-center gap-4">
        {/* Subscription & Profile Links */}
        <div className="flex flex-wrap justify-center gap-3 w-full">
            <a
                href="https://livepix.gg/eltonjose/assinatura"
                target="_blank"
                rel="noopener noreferrer"
                className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg transition-colors flex items-center gap-2"
            >
                ⭐ Seja Assinante
            </a>
            <a
                href="https://livepix.gg/eltonjose"
                target="_blank"
                rel="noopener noreferrer"
                className="px-5 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-600 dark:hover:bg-gray-500 text-dark dark:text-white font-bold rounded-lg transition-colors flex items-center gap-2"
            >
                🔗 Perfil LivePix
            </a>
        </div>


      </div>
    </div>
  );
};

export default SupporterCTA;
