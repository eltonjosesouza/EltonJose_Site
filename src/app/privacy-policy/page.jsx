import { Metadata } from 'next';

export const metadata = {
  title: 'Política de Privacidade | Elton José',
  description: 'Política de Privacidade do site eltonjose.com.br - Como coletamos, usamos e protegemos seus dados pessoais.',
  openGraph: {
    title: 'Política de Privacidade | Elton José',
    description: 'Saiba como protegemos sua privacidade e tratamos seus dados.',
    url: 'https://www.eltonjose.com.br/privacy-policy',
    type: 'website',
  },
};

export default function PrivacyPolicyPage() {
  return (
    <div className="w-full min-h-screen py-16 px-5 sm:px-10 md:px-24 lg:px-32">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl md:text-5xl font-bold text-dark dark:text-light mb-4">
          Política de Privacidade
        </h1>
        <p className="text-dark/70 dark:text-light/70 mb-8">
          Última atualização: {new Date().toLocaleDateString('pt-BR')}
        </p>

        <div className="prose prose-lg dark:prose-invert max-w-none">
          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">1. Introdução</h2>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Esta Política de Privacidade descreve como o site <strong>eltonjose.com.br</strong> ("nós", "nosso" ou "site")
              coleta, usa, armazena e protege as informações pessoais dos visitantes e usuários.
            </p>
            <p className="text-dark/80 dark:text-light/80">
              Ao acessar e usar este site, você concorda com os termos desta Política de Privacidade.
              Se você não concordar com qualquer parte desta política, por favor, não use nosso site.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">2. Informações que Coletamos</h2>

            <h3 className="text-xl font-semibold text-dark dark:text-light mb-3">2.1 Informações Fornecidas Voluntariamente</h3>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Quando você entra em contato conosco através do formulário de contato, podemos coletar:
            </p>
            <ul className="list-disc pl-6 mb-4 text-dark/80 dark:text-light/80">
              <li>Nome</li>
              <li>Endereço de email</li>
              <li>Assunto e mensagem</li>
            </ul>

            <h3 className="text-xl font-semibold text-dark dark:text-light mb-3">2.2 Informações Coletadas Automaticamente</h3>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Quando você visita nosso site, podemos coletar automaticamente:
            </p>
            <ul className="list-disc pl-6 mb-4 text-dark/80 dark:text-light/80">
              <li>Endereço IP</li>
              <li>Tipo de navegador e sistema operacional</li>
              <li>Páginas visitadas e tempo de permanência</li>
              <li>Referências de origem (de onde você veio)</li>
              <li>Dados de cookies e tecnologias similares</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">3. Como Usamos Suas Informações</h2>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Usamos as informações coletadas para:
            </p>
            <ul className="list-disc pl-6 mb-4 text-dark/80 dark:text-light/80">
              <li>Responder a suas mensagens e solicitações</li>
              <li>Melhorar a experiência do usuário no site</li>
              <li>Analisar o uso do site e gerar estatísticas</li>
              <li>Exibir anúncios relevantes através do Google AdSense</li>
              <li>Cumprir obrigações legais</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">4. Cookies e Tecnologias Similares</h2>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Nosso site usa cookies e tecnologias similares para:
            </p>
            <ul className="list-disc pl-6 mb-4 text-dark/80 dark:text-light/80">
              <li><strong>Cookies Essenciais:</strong> Necessários para o funcionamento básico do site</li>
              <li><strong>Cookies Analíticos:</strong> Google Analytics para entender como os visitantes usam o site</li>
              <li><strong>Cookies de Publicidade:</strong> Google AdSense para exibir anúncios personalizados</li>
            </ul>
            <p className="text-dark/80 dark:text-light/80">
              Você pode configurar seu navegador para recusar cookies, mas isso pode afetar a funcionalidade do site.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">5. Google AdSense e Publicidade</h2>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Este site usa o Google AdSense para exibir anúncios. O Google pode usar cookies para exibir anúncios
              baseados em suas visitas anteriores a este site ou outros sites na internet.
            </p>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Você pode desativar anúncios personalizados visitando as{' '}
              <a
                href="https://www.google.com/settings/ads"
                target="_blank"
                rel="noopener noreferrer"
                className="text-accent dark:text-accentDark hover:underline"
              >
                Configurações de Anúncios do Google
              </a>.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">6. Compartilhamento de Informações</h2>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Não vendemos, alugamos ou compartilhamos suas informações pessoais com terceiros, exceto:
            </p>
            <ul className="list-disc pl-6 mb-4 text-dark/80 dark:text-light/80">
              <li>Com provedores de serviços (Google Analytics, Google AdSense) para operar o site</li>
              <li>Quando exigido por lei ou para proteger nossos direitos legais</li>
              <li>Com seu consentimento explícito</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">7. Segurança dos Dados</h2>
            <p className="text-dark/80 dark:text-light/80">
              Implementamos medidas de segurança técnicas e organizacionais para proteger suas informações pessoais
              contra acesso não autorizado, alteração, divulgação ou destruição. No entanto, nenhum método de
              transmissão pela internet é 100% seguro.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">8. Seus Direitos (LGPD/GDPR)</h2>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              De acordo com a Lei Geral de Proteção de Dados (LGPD) e o Regulamento Geral de Proteção de Dados (GDPR),
              você tem os seguintes direitos:
            </p>
            <ul className="list-disc pl-6 mb-4 text-dark/80 dark:text-light/80">
              <li><strong>Acesso:</strong> Solicitar acesso aos seus dados pessoais</li>
              <li><strong>Correção:</strong> Solicitar correção de dados incorretos ou incompletos</li>
              <li><strong>Exclusão:</strong> Solicitar a exclusão de seus dados pessoais</li>
              <li><strong>Portabilidade:</strong> Solicitar a transferência de seus dados</li>
              <li><strong>Oposição:</strong> Opor-se ao processamento de seus dados</li>
              <li><strong>Revogação de Consentimento:</strong> Retirar seu consentimento a qualquer momento</li>
            </ul>
            <p className="text-dark/80 dark:text-light/80">
              Para exercer esses direitos, entre em contato conosco através do email:{' '}
              <a
                href="mailto:contato@eltonjose.com.br"
                className="text-accent dark:text-accentDark hover:underline"
              >
                contato@eltonjose.com.br
              </a>
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">9. Links para Sites de Terceiros</h2>
            <p className="text-dark/80 dark:text-light/80">
              Nosso site pode conter links para sites de terceiros. Não somos responsáveis pelas práticas de
              privacidade desses sites. Recomendamos que você leia as políticas de privacidade de cada site que visitar.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">10. Menores de Idade</h2>
            <p className="text-dark/80 dark:text-light/80">
              Nosso site não é direcionado a menores de 18 anos. Não coletamos intencionalmente informações pessoais
              de menores. Se você é pai/mãe ou responsável e acredita que seu filho nos forneceu informações pessoais,
              entre em contato conosco.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">11. Alterações a Esta Política</h2>
            <p className="text-dark/80 dark:text-light/80">
              Podemos atualizar esta Política de Privacidade periodicamente. Notificaremos sobre mudanças significativas
              publicando a nova política nesta página com uma data de "última atualização" revisada.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">12. Contato</h2>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Se você tiver dúvidas sobre esta Política de Privacidade ou sobre como tratamos seus dados pessoais,
              entre em contato:
            </p>
            <ul className="list-none mb-4 text-dark/80 dark:text-light/80">
              <li><strong>Email:</strong> contato@eltonjose.com.br</li>
              <li><strong>Site:</strong> <a href="/contact" className="text-accent dark:text-accentDark hover:underline">Formulário de Contato</a></li>
            </ul>
          </section>
        </div>
      </div>
    </div>
  );
}
