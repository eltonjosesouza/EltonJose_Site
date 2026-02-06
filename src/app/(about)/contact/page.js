import { Metadata } from 'next';
import ContactForm from '@/src/components/Contact/ContactForm';
import { Mail, MapPin } from 'lucide-react';

export const metadata = {
    title: 'Contato | Elton José',
    description: 'Entre em contato comigo para discutir projetos, colaborações ou apenas para trocar ideias sobre tecnologia e desenvolvimento.',
    openGraph: {
        title: 'Contato | Elton José',
        description: 'Entre em contato para discutir projetos e colaborações.',
        url: 'https://www.eltonjose.com.br/contact',
        type: 'website',
    },
};

export default function ContactPage() {
    return (
        <div className="w-full min-h-screen py-16 px-5 sm:px-10 md:px-24 lg:px-32">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="text-center mb-16">
                    <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-dark dark:text-light mb-4">
                        Entre em Contato
                    </h1>
                    <p className="text-lg md:text-xl text-dark/70 dark:text-light/70 max-w-2xl mx-auto">
                        Tem um projeto em mente? Quer discutir sobre tecnologia ou colaborar em algo interessante?
                        Adoraria ouvir de você!
                    </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                    {/* Contact Information */}
                    <div className="space-y-8">
                        <div>
                            <h2 className="text-2xl md:text-3xl font-semibold text-dark dark:text-light mb-6">
                                Informações de Contato
                            </h2>
                            <p className="text-dark/70 dark:text-light/70 mb-8">
                                Estou sempre aberto a novas oportunidades, colaborações e conversas interessantes sobre tecnologia,
                                desenvolvimento de software e inovação.
                            </p>
                        </div>

                        {/* Contact Details */}
                        <div className="space-y-6">
                            <div className="flex items-start gap-4">
                                <div className="p-3 bg-accent/10 dark:bg-accentDark/10 rounded-lg">
                                    <Mail className="w-6 h-6 text-accent dark:text-accentDark" />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-dark dark:text-light mb-1">Email</h3>
                                    <a
                                        href="mailto:contato@eltonjose.com.br"
                                        className="text-accent dark:text-accentDark hover:underline"
                                    >
                                        contato@eltonjose.com.br
                                    </a>
                                    <p className="text-sm text-dark/60 dark:text-light/60 mt-1">
                                        Respondo geralmente em até 24-48 horas
                                    </p>
                                </div>
                            </div>

                            <div className="flex items-start gap-4">
                                <div className="p-3 bg-accent/10 dark:bg-accentDark/10 rounded-lg">
                                    <MapPin className="w-6 h-6 text-accent dark:text-accentDark" />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-dark dark:text-light mb-1">Localização</h3>
                                    <p className="text-dark/70 dark:text-light/70">
                                        Goiânia/GO, Brasil
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Contact Form */}
                    <div className="bg-light dark:bg-dark border-2 border-solid border-dark dark:border-light rounded-lg p-8">
                        <h2 className="text-2xl md:text-3xl font-semibold text-dark dark:text-light mb-6">
                            Envie uma Mensagem
                        </h2>
                        <ContactForm />
                    </div>
                </div>


            </div>
        </div>
  );
}
