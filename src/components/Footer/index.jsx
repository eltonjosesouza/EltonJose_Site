import Link from 'next/link';
import siteMetadata from '@/src/utils/siteMetaData';
import { GithubIcon, LinkedinIcon, TwitterIcon, InstagramIcon } from '../Icons';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="w-full bg-light dark:bg-dark border-t-2 border-solid border-dark dark:border-light">
      <div className="max-w-7xl mx-auto px-5 sm:px-10 md:px-24 lg:px-32 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* About Section */}
          <div className="col-span-1 md:col-span-2">
            <h3 className="text-lg font-semibold text-dark dark:text-light mb-4">
              Elton José
            </h3>
            <p className="text-dark/70 dark:text-light/70 text-sm mb-4">
              Desenvolvedor experiente com mais de duas décadas de expertise em tecnologia,
              liderança e entrega de soluções inovadoras. Compartilhando conhecimento sobre
              IA, desenvolvimento de software e inovação.
            </p>
            <div className="flex gap-4">
              <a
                href={siteMetadata.linkedin}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block w-6 h-6 hover:scale-125 transition-all ease duration-200"
                aria-label="LinkedIn"
              >
                <LinkedinIcon className="fill-dark dark:fill-light" />
              </a>
              <a
                href={siteMetadata.twitter}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block w-6 h-6 hover:scale-125 transition-all ease duration-200"
                aria-label="Twitter"
              >
                <TwitterIcon className="fill-dark dark:fill-light" />
              </a>
              <a
                href={siteMetadata.github}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block w-6 h-6 hover:scale-125 transition-all ease duration-200"
                aria-label="GitHub"
              >
                <GithubIcon className="fill-dark dark:fill-light" />
              </a>
              <a
                href={siteMetadata.instagram}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block w-6 h-6 hover:scale-125 transition-all ease duration-200"
                aria-label="Instagram"
              >
                <InstagramIcon className="fill-dark dark:fill-light" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold text-dark dark:text-light mb-4">
              Links Rápidos
            </h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/"
                  className="text-dark/70 dark:text-light/70 hover:text-accent dark:hover:text-accentDark text-sm transition-colors"
                >
                  Home
                </Link>
              </li>
              <li>
                <Link
                  href="/about"
                  className="text-dark/70 dark:text-light/70 hover:text-accent dark:hover:text-accentDark text-sm transition-colors"
                >
                  Sobre
                </Link>
              </li>
              <li>
                <Link
                  href="/blogs"
                  className="text-dark/70 dark:text-light/70 hover:text-accent dark:hover:text-accentDark text-sm transition-colors"
                >
                  Blog
                </Link>
              </li>
              <li>
                <Link
                  href="/courses"
                  className="text-dark/70 dark:text-light/70 hover:text-accent dark:hover:text-accentDark text-sm transition-colors"
                >
                  Cursos
                </Link>
              </li>
              <li>
                <Link
                  href="/contact"
                  className="text-dark/70 dark:text-light/70 hover:text-accent dark:hover:text-accentDark text-sm transition-colors"
                >
                  Contato
                </Link>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="text-lg font-semibold text-dark dark:text-light mb-4">
              Legal
            </h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/privacy-policy"
                  className="text-dark/70 dark:text-light/70 hover:text-accent dark:hover:text-accentDark text-sm transition-colors"
                >
                  Política de Privacidade
                </Link>
              </li>
              <li>
                <Link
                  href="/terms"
                  className="text-dark/70 dark:text-light/70 hover:text-accent dark:hover:text-accentDark text-sm transition-colors"
                >
                  Termos de Uso
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-dark/20 dark:border-light/20">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-dark/60 dark:text-light/60 text-sm text-center md:text-left">
              © {currentYear} Elton José. Todos os direitos reservados.
            </p>
            <p className="text-dark/60 dark:text-light/60 text-sm text-center md:text-right">
              Feito com ❤️ usando{' '}
              <a
                href="https://nextjs.org"
                target="_blank"
                rel="noopener noreferrer"
                className="text-accent dark:text-accentDark hover:underline"
              >
                Next.js
              </a>
              {' '}e{' '}
              <a
                href="https://tailwindcss.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-accent dark:text-accentDark hover:underline"
              >
                Tailwind CSS
              </a>
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
