import { ProtectedRoute } from '@/src/components/auth/ProtectedRoute'
import { UserMenu } from '@/src/components/auth/UserMenu'
import { createClient } from '@/src/lib/supabase/server'
import Link from 'next/link'

export default async function AdminDashboard() {
  const supabase = await createClient()

  const { data: { user } } = await supabase.auth.getUser()

  console.log('AdminDashboard: User from getUser()?', !!user);
  if (user) console.log('AdminDashboard: User ID:', user.id);
  const { data: profile } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', user?.id || '')
    .single() as any

  if (!profile) {
    // If no profile found (not logged in), let ProtectedRoute handle redirect or force it here
    // But since ProtectedRoute is inside the return, we can't reach it.
    // Better to just allow pass-through if we trust ProtectedRoute,
    // BUT we need 'profile' for the component body? No, we don't pass profile to ProtectedRoute.
    // We pass children.
    // Wait, if profile is null, we can't render the dashboard content.
    // We should redirect to login.
    // BUT, 'redirect' from next/navigation works here.
    const { redirect } = await import('next/navigation')
    redirect('/login')
  }

  // In a real app, you might want to fetch stats via an RPC call or aggregation
  // For now, we'll placeholder stats
  const stats = {
    total_users: 156,
    published_posts: 42,
    subscribers: 18,
    monthly_donations: 1250.00
  }

  return (
    <ProtectedRoute allowedRoles={['admin']}>
      <div className="min-h-screen bg-gray-100 dark:bg-zinc-900">
        <header className="bg-white dark:bg-zinc-800 shadow">
          <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
            <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
              Admin Dashboard
            </h1>
            <UserMenu />
          </div>
        </header>

        <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
            <div className="bg-white dark:bg-zinc-800 p-6 rounded-lg shadow-sm">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Usuários</h3>
              <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">{stats.total_users}</p>
            </div>

            <div className="bg-white dark:bg-zinc-800 p-6 rounded-lg shadow-sm">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Posts Publicados</h3>
              <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">{stats.published_posts}</p>
            </div>

            <div className="bg-white dark:bg-zinc-800 p-6 rounded-lg shadow-sm">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Assinantes Ativos</h3>
              <p className="mt-2 text-3xl font-bold text-blue-600 dark:text-blue-400">{stats.subscribers}</p>
            </div>

            <div className="bg-white dark:bg-zinc-800 p-6 rounded-lg shadow-sm">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Doações (Fev)</h3>
              <p className="mt-2 text-3xl font-bold text-green-600 dark:text-green-400">R$ {stats.monthly_donations.toFixed(2)}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <div className="bg-white dark:bg-zinc-800 rounded-lg shadow-sm p-6">
              <h2 className="text-lg font-medium mb-4 dark:text-white">Ações Rápidas</h2>
              <div className="grid grid-cols-2 gap-4">
                <Link href="/admin/users" className="p-4 border dark:border-zinc-700 rounded hover:bg-gray-50 dark:hover:bg-zinc-700 transition-colors text-center">
                  Gerenciar Usuários
                </Link>
                <Link href="/editor" className="p-4 border dark:border-zinc-700 rounded hover:bg-gray-50 dark:hover:bg-zinc-700 transition-colors text-center">
                  Painel de Editor
                </Link>
                <Link href="/revisor" className="p-4 border dark:border-zinc-700 rounded hover:bg-gray-50 dark:hover:bg-zinc-700 transition-colors text-center">
                  Painel de Revisor
                </Link>
                <Link href="/settings" className="p-4 border dark:border-zinc-700 rounded hover:bg-gray-50 dark:hover:bg-zinc-700 transition-colors text-center">
                  Configurações
                </Link>
              </div>
            </div>

            <div className="bg-white dark:bg-zinc-800 rounded-lg shadow-sm p-6">
              <h2 className="text-lg font-medium mb-4 dark:text-white">Logs Recentes</h2>
              <div className="space-y-3">
                <div className="flex justify-between text-sm py-2 border-b dark:border-zinc-700">
                  <span className="text-gray-600 dark:text-gray-400">Novo usuário registrado</span>
                  <span className="text-gray-400 text-xs">2 min atrás</span>
                </div>
                <div className="flex justify-between text-sm py-2 border-b dark:border-zinc-700">
                  <span className="text-gray-600 dark:text-gray-400">Post "Agentic AI" publicado</span>
                  <span className="text-gray-400 text-xs">1 hora atrás</span>
                </div>
                <div className="flex justify-between text-sm py-2">
                  <span className="text-gray-600 dark:text-gray-400">Doação recebida: R$ 50,00</span>
                  <span className="text-gray-400 text-xs">3 horas atrás</span>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  )
}
