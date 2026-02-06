"use client";
import React from "react";

export default function ContactForm() {
  return (
    <ul>
      <li>
        <a href="mailto:contato@eltonjose.com.br" className="flex items-center mt-4 text-dark dark:text-light hover:text-accent dark:hover:text-accentDark transition-colors" target="_blank" rel="noopener noreferrer">
          Email: contato@eltonjose.com.br
        </a>
      </li>
      <li>
        <a href="https://www.linkedin.com/in/eltonjosesouza/" className="flex items-center mt-4 text-dark dark:text-light hover:text-accent dark:hover:text-accentDark transition-colors" target="_blank" rel="noopener noreferrer">
          LinkedIn: eltonjosesouza
        </a>
      </li>
      <li>
        <a href="https://www.instagram.com/eltonjose.tech" className="flex items-center mt-4 text-dark dark:text-light hover:text-accent dark:hover:text-accentDark transition-colors" target="_blank" rel="noopener noreferrer">
          Instagram: @eltonjose.tech
        </a>
      </li>
      <li>
        <a href="https://www.facebook.com/eltonjosesouza/" className="flex items-center mt-4 text-dark dark:text-light hover:text-accent dark:hover:text-accentDark transition-colors" target="_blank" rel="noopener noreferrer">
          Facebook: eltonjosesouza
        </a>
      </li>
      <li>
        <a href="https://github.com/eltonjosesouza" className="flex items-center mt-4 text-dark dark:text-light hover:text-accent dark:hover:text-accentDark transition-colors" target="_blank" rel="noopener noreferrer">
          Github: eltonjosesouza
        </a>
      </li>
      <li>
        <a href="https://www.eltonjose.com.br" className="flex items-center mt-4 text-dark dark:text-light hover:text-accent dark:hover:text-accentDark transition-colors" target="_blank" rel="noopener noreferrer">
          Website Pessoal: www.eltonjose.com.br
        </a>
      </li>
    </ul>



  );
}
