import { ProtectedRoute } from '@/src/components/auth/ProtectedRoute'
import { UserMenu } from '@/src/components/auth/UserMenu'
import { createClient } from '@/src/lib/supabase/server'
import Link from 'next/link'

export default async function RevisorDashboard() {
  const supabase = await createClient()

  const { data: { user } } = await supabase.auth.getUser()
  const { data: profile } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', user?.id || '')
    .single() as any

  return (
    <ProtectedRoute allowedRoles={['revisor', 'editor', 'admin']}>
      <div className="min-h-screen bg-gray-50 dark:bg-zinc-900">
        <header className="bg-white dark:bg-zinc-800 shadow">
          <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
            <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
              Painel de Revisão
            </h1>
            {profile && <UserMenu />}
          </div>
        </header>

        <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <div className="mt-8">
            <h2 className="text-lg font-medium mb-4 dark:text-white">Fila de Revisão</h2>
            <div className="bg-white dark:bg-zinc-800 shadow overflow-hidden sm:rounded-md">
              <ul className="divide-y divide-gray-200 dark:divide-zinc-700">
                <li className="p-4 text-center text-gray-500 dark:text-gray-400 py-12">
                  Não há posts aguardando revisão no momento.
                </li>
              </ul>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  )
}
