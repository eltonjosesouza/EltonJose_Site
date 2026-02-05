import { ProtectedRoute } from '@/src/components/auth/ProtectedRoute'
import { UserMenu } from '@/src/components/auth/UserMenu'
import { createClient } from '@/src/lib/supabase/server'
import Link from 'next/link'

export default async function EditorDashboard() {
  const supabase = await createClient()

  const { data: { user } } = await supabase.auth.getUser()
  const { data: profile } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', user?.id || '')
    .single() as any

  return (
    <ProtectedRoute allowedRoles={['editor', 'admin']}>
      <div className="min-h-screen bg-gray-50 dark:bg-zinc-900">
        <header className="bg-white dark:bg-zinc-800 shadow">
          <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
            <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
              Painel do Editor
            </h1>
            {profile && <UserMenu />}
          </div>
        </header>

        <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <div className="mt-8">
            <h2 className="text-lg font-medium mb-4 dark:text-white">Gerenciar Conteúdo</h2>
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
              <Link href="/posts/new" className="block p-6 bg-white dark:bg-zinc-800 rounded-lg shadow hover:shadow-md transition-shadow border-l-4 border-blue-500">
                <h3 className="text-lg font-bold text-gray-900 dark:text-white">Novo Post</h3>
                <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">Criar um novo artigo para o blog</p>
              </Link>

              <Link href="/posts?status=draft" className="block p-6 bg-white dark:bg-zinc-800 rounded-lg shadow hover:shadow-md transition-shadow border-l-4 border-yellow-500">
                <h3 className="text-lg font-bold text-gray-900 dark:text-white">Rascunhos</h3>
                <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">Ver e editar posts em andamento</p>
              </Link>

              <Link href="/posts?status=published" className="block p-6 bg-white dark:bg-zinc-800 rounded-lg shadow hover:shadow-md transition-shadow border-l-4 border-green-500">
                <h3 className="text-lg font-bold text-gray-900 dark:text-white">Publicados</h3>
                <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">Gerenciar posts já publicados</p>
              </Link>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  )
}
