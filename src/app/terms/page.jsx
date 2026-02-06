import { Metadata } from 'next';

export const metadata = {
  title: 'Termos de Uso | Elton José',
  description: 'Termos de Uso do site eltonjose.com.br - Regras e condições para uso do site.',
  openGraph: {
    title: 'Termos de Uso | Elton José',
    description: 'Conheça os termos e condições de uso do site.',
    url: 'https://www.eltonjose.com.br/terms',
    type: 'website',
  },
};

export default function TermsPage() {
  return (
    <div className="w-full min-h-screen py-16 px-5 sm:px-10 md:px-24 lg:px-32">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl md:text-5xl font-bold text-dark dark:text-light mb-4">
          Termos de Uso
        </h1>
        <p className="text-dark/70 dark:text-light/70 mb-8">
          Última atualização: {new Date().toLocaleDateString('pt-BR')}
        </p>

        <div className="prose prose-lg dark:prose-invert max-w-none">
          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">1. Aceitação dos Termos</h2>
            <p className="text-dark/80 dark:text-light/80">
              Ao acessar e usar o site <strong>eltonjose.com.br</strong> ("Site"), você concorda em cumprir e estar
              vinculado a estes Termos de Uso. Se você não concordar com qualquer parte destes termos, não deve usar
              este Site.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">2. Descrição do Serviço</h2>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Este Site é um blog pessoal que fornece conteúdo educacional e informativo sobre:
            </p>
            <ul className="list-disc pl-6 mb-4 text-dark/80 dark:text-light/80">
              <li>Desenvolvimento de software</li>
              <li>Inteligência Artificial</li>
              <li>Tecnologia e inovação</li>
              <li>Carreira em tecnologia</li>
              <li>Tutoriais e guias técnicos</li>
            </ul>
            <p className="text-dark/80 dark:text-light/80">
              O conteúdo é fornecido "como está" para fins informativos e educacionais.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">3. Propriedade Intelectual</h2>

            <h3 className="text-xl font-semibold text-dark dark:text-light mb-3">3.1 Conteúdo do Site</h3>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Todo o conteúdo deste Site, incluindo mas não limitado a textos, gráficos, logos, imagens, vídeos,
              código-fonte e software, é propriedade de Elton José ou de seus licenciadores e está protegido por
              leis de direitos autorais brasileiras e internacionais.
            </p>

            <h3 className="text-xl font-semibold text-dark dark:text-light mb-3">3.2 Uso Permitido</h3>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Você pode:
            </p>
            <ul className="list-disc pl-6 mb-4 text-dark/80 dark:text-light/80">
              <li>Visualizar e ler o conteúdo para uso pessoal e não comercial</li>
              <li>Compartilhar links para artigos nas redes sociais</li>
              <li>Citar trechos do conteúdo com atribuição adequada</li>
            </ul>

            <h3 className="text-xl font-semibold text-dark dark:text-light mb-3">3.3 Uso Proibido</h3>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Você NÃO pode:
            </p>
            <ul className="list-disc pl-6 mb-4 text-dark/80 dark:text-light/80">
              <li>Copiar, reproduzir ou republicar conteúdo sem permissão expressa</li>
              <li>Usar conteúdo para fins comerciais sem autorização</li>
              <li>Modificar ou criar trabalhos derivados sem permissão</li>
              <li>Remover avisos de direitos autorais ou marcas registradas</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">4. Código de Conduta do Usuário</h2>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Ao usar este Site, você concorda em NÃO:
            </p>
            <ul className="list-disc pl-6 mb-4 text-dark/80 dark:text-light/80">
              <li>Violar qualquer lei ou regulamento aplicável</li>
              <li>Publicar conteúdo ofensivo, difamatório ou ilegal</li>
              <li>Tentar obter acesso não autorizado ao Site ou seus sistemas</li>
              <li>Interferir ou interromper o funcionamento do Site</li>
              <li>Usar bots, scrapers ou ferramentas automatizadas sem permissão</li>
              <li>Transmitir vírus, malware ou código malicioso</li>
              <li>Fazer engenharia reversa de qualquer parte do Site</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">5. Conteúdo de Terceiros e Links</h2>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Este Site pode conter links para sites de terceiros. Esses links são fornecidos apenas para sua
              conveniência. Não temos controle sobre o conteúdo desses sites e não nos responsabilizamos por eles.
            </p>
            <p className="text-dark/80 dark:text-light/80">
              A inclusão de qualquer link não implica endosso do site vinculado.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">6. Publicidade</h2>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Este Site exibe anúncios através do Google AdSense e possivelmente outras redes de publicidade.
              Não controlamos o conteúdo dos anúncios exibidos.
            </p>
            <p className="text-dark/80 dark:text-light/80">
              Você reconhece que clicar em anúncios pode levá-lo a sites de terceiros, pelos quais não somos responsáveis.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">7. Isenção de Garantias</h2>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              O Site e seu conteúdo são fornecidos "COMO ESTÃO" e "CONFORME DISPONÍVEIS", sem garantias de qualquer tipo,
              expressas ou implícitas, incluindo mas não limitado a:
            </p>
            <ul className="list-disc pl-6 mb-4 text-dark/80 dark:text-light/80">
              <li>Garantias de comercialização</li>
              <li>Adequação a um propósito específico</li>
              <li>Não violação de direitos de terceiros</li>
              <li>Precisão, confiabilidade ou completude do conteúdo</li>
            </ul>
            <p className="text-dark/80 dark:text-light/80">
              Não garantimos que o Site estará sempre disponível, livre de erros ou seguro.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">8. Limitação de Responsabilidade</h2>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Na extensão máxima permitida por lei, Elton José e seus afiliados não serão responsáveis por quaisquer
              danos diretos, indiretos, incidentais, especiais, consequenciais ou punitivos resultantes de:
            </p>
            <ul className="list-disc pl-6 mb-4 text-dark/80 dark:text-light/80">
              <li>Uso ou incapacidade de usar o Site</li>
              <li>Acesso não autorizado ou alteração de suas transmissões ou dados</li>
              <li>Declarações ou conduta de terceiros no Site</li>
              <li>Qualquer outro assunto relacionado ao Site</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">9. Indenização</h2>
            <p className="text-dark/80 dark:text-light/80">
              Você concorda em indenizar, defender e isentar Elton José de todas as reivindicações, responsabilidades,
              danos, perdas e despesas (incluindo honorários advocatícios) decorrentes de ou relacionados ao seu uso
              do Site ou violação destes Termos de Uso.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">10. Modificações dos Termos</h2>
            <p className="text-dark/80 dark:text-light/80">
              Reservamo-nos o direito de modificar estes Termos de Uso a qualquer momento. Mudanças significativas
              serão notificadas através de aviso no Site. O uso continuado do Site após tais modificações constitui
              sua aceitação dos novos termos.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">11. Rescisão</h2>
            <p className="text-dark/80 dark:text-light/80">
              Podemos rescindir ou suspender seu acesso ao Site imediatamente, sem aviso prévio ou responsabilidade,
              por qualquer motivo, incluindo violação destes Termos de Uso.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">12. Lei Aplicável e Jurisdição</h2>
            <p className="text-dark/80 dark:text-light/80">
              Estes Termos de Uso são regidos pelas leis do Brasil. Qualquer disputa relacionada a estes termos
              será resolvida nos tribunais competentes de São Paulo, Brasil.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">13. Disposições Gerais</h2>

            <h3 className="text-xl font-semibold text-dark dark:text-light mb-3">13.1 Acordo Completo</h3>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Estes Termos de Uso, juntamente com a Política de Privacidade, constituem o acordo completo entre
              você e Elton José em relação ao uso do Site.
            </p>

            <h3 className="text-xl font-semibold text-dark dark:text-light mb-3">13.2 Divisibilidade</h3>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Se qualquer disposição destes Termos for considerada inválida ou inexequível, as demais disposições
              permanecerão em pleno vigor e efeito.
            </p>

            <h3 className="text-xl font-semibold text-dark dark:text-light mb-3">13.3 Renúncia</h3>
            <p className="text-dark/80 dark:text-light/80">
              A falha em fazer cumprir qualquer direito ou disposição destes Termos não constituirá uma renúncia
              a tal direito ou disposição.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-dark dark:text-light mb-4">14. Contato</h2>
            <p className="text-dark/80 dark:text-light/80 mb-4">
              Se você tiver dúvidas sobre estes Termos de Uso, entre em contato:
            </p>
            <ul className="list-none mb-4 text-dark/80 dark:text-light/80">
              <li><strong>Email:</strong> contato@eltonjose.com.br</li>
              <li><strong>Site:</strong> <a href="/contact" className="text-accent dark:text-accentDark hover:underline">Formulário de Contato</a></li>
            </ul>
          </section>

          <div className="mt-12 p-6 bg-accent/10 dark:bg-accentDark/10 rounded-lg border-l-4 border-accent dark:border-accentDark">
            <p className="text-dark/80 dark:text-light/80 font-semibold mb-2">
              Ao usar este Site, você reconhece que leu, entendeu e concordou em estar vinculado a estes Termos de Uso.
            </p>
            <p className="text-dark/70 dark:text-light/70 text-sm">
              Última atualização: {new Date().toLocaleDateString('pt-BR')}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
