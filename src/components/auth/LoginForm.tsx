'use client'

import { useState } from 'react'
import { createClient } from '@/src/lib/supabase/client'
import { useRouter } from 'next/navigation'

export function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()
  const supabase = createClient()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    console.log('LoginForm: Attempting login with', email);

    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })

    console.log('LoginForm: Supabase response', { data, error });

    if (error) {
      console.error('LoginForm: Login error', error.message);
      setError(error.message)
      setLoading(false)
    } else {
      console.log('LoginForm: Login success, redirecting to /admin');
      router.push('/admin') // Redirect to dashboard or respect 'redirect' param
      router.refresh()
    }
  }

  return (
    <form onSubmit={handleLogin} className="space-y-4 max-w-sm mx-auto p-6 bg-white dark:bg-zinc-800 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-center text-dark dark:text-light">Login</h2>
      {error && (
        <div className="bg-red-50 text-red-600 p-3 rounded text-sm">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="email" className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-200">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          autoComplete="email"
          className="w-full px-3 py-2 border rounded-md dark:bg-zinc-700 dark:border-zinc-600 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="seu@email.com"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-200">
          Senha
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          autoComplete="current-password"
          className="w-full px-3 py-2 border rounded-md dark:bg-zinc-700 dark:border-zinc-600 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="••••••••"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 transition-colors font-medium"
      >
        {loading ? 'Entrando...' : 'Entrar'}
      </button>
    </form>
  )
}
