'use client';

import { useState } from 'react';

export default function ContactForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  });
  const [status, setStatus] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setStatus('');

    try {
      // Aqui você pode integrar com um serviço de email (SendGrid, Resend, etc.)
      // Por enquanto, vamos simular o envio
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Exemplo de integração com API
      // const response = await fetch('/api/contact', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(formData),
      // });

      setStatus('success');
      setFormData({ name: '', email: '', subject: '', message: '' });
    } catch (error) {
      setStatus('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-dark dark:text-light mb-2">
          Nome *
        </label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
          className="w-full px-4 py-3 bg-light dark:bg-dark border-2 border-dark dark:border-light rounded-lg focus:outline-none focus:ring-2 focus:ring-accent dark:focus:ring-accentDark text-dark dark:text-light"
          placeholder="Seu nome completo"
        />
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-dark dark:text-light mb-2">
          Email *
        </label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
          className="w-full px-4 py-3 bg-light dark:bg-dark border-2 border-dark dark:border-light rounded-lg focus:outline-none focus:ring-2 focus:ring-accent dark:focus:ring-accentDark text-dark dark:text-light"
          placeholder="seu@email.com"
        />
      </div>

      <div>
        <label htmlFor="subject" className="block text-sm font-medium text-dark dark:text-light mb-2">
          Assunto *
        </label>
        <input
          type="text"
          id="subject"
          name="subject"
          value={formData.subject}
          onChange={handleChange}
          required
          className="w-full px-4 py-3 bg-light dark:bg-dark border-2 border-dark dark:border-light rounded-lg focus:outline-none focus:ring-2 focus:ring-accent dark:focus:ring-accentDark text-dark dark:text-light"
          placeholder="Sobre o que você quer falar?"
        />
      </div>

      <div>
        <label htmlFor="message" className="block text-sm font-medium text-dark dark:text-light mb-2">
          Mensagem *
        </label>
        <textarea
          id="message"
          name="message"
          value={formData.message}
          onChange={handleChange}
          required
          rows={6}
          className="w-full px-4 py-3 bg-light dark:bg-dark border-2 border-dark dark:border-light rounded-lg focus:outline-none focus:ring-2 focus:ring-accent dark:focus:ring-accentDark text-dark dark:text-light resize-none"
          placeholder="Escreva sua mensagem aqui..."
        />
      </div>

      {status === 'success' && (
        <div className="p-4 bg-green-100 dark:bg-green-900/30 border border-green-500 rounded-lg">
          <p className="text-green-700 dark:text-green-300 text-sm">
            ✓ Mensagem enviada com sucesso! Entrarei em contato em breve.
          </p>
        </div>
      )}

      {status === 'error' && (
        <div className="p-4 bg-red-100 dark:bg-red-900/30 border border-red-500 rounded-lg">
          <p className="text-red-700 dark:text-red-300 text-sm">
            ✗ Erro ao enviar mensagem. Por favor, tente novamente ou envie um email diretamente.
          </p>
        </div>
      )}

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full px-6 py-3 bg-accent dark:bg-accentDark text-light dark:text-dark font-semibold rounded-lg hover:bg-accent/90 dark:hover:bg-accentDark/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isSubmitting ? 'Enviando...' : 'Enviar Mensagem'}
      </button>

      <p className="text-xs text-dark/60 dark:text-light/60 text-center">
        * Campos obrigatórios
      </p>
    </form>
  );
}
