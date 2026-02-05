import { LoginForm } from '@/src/components/auth/LoginForm'
import { createClient } from '@/src/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function LoginPage() {
  const supabase = await createClient()

  const { data: { session } } = await supabase.auth.getSession()

  if (session) {
    redirect('/admin')
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 dark:bg-zinc-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold tracking-tight text-dark dark:text-light">
            Acesso Restrito
          </h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-300">
            Faça login para acessar o painel administrativo
          </p>
        </div>
        <LoginForm />
      </div>
    </div>
  )
}
