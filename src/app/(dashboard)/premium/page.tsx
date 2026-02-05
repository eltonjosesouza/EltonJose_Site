import { ProtectedRoute } from '@/src/components/auth/ProtectedRoute'
import { UserMenu } from '@/src/components/auth/UserMenu'
import { createClient } from '@/src/lib/supabase/server'

export default async function PremiumDashboard() {
  const supabase = await createClient()

  const { data: { user } } = await supabase.auth.getUser()
  const { data: profile } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', user?.id || '')
    .single() as any

  if (!profile) return null

  return (
    <ProtectedRoute allowedRoles={['assinante', 'doador', 'admin']}>
      <div className="min-h-screen bg-gray-50 dark:bg-zinc-900">
        <header className="bg-white dark:bg-zinc-800 shadow">
          <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
            <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
              Área Premium
            </h1>
            {profile && <UserMenu />}
          </div>
        </header>

        <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-lg shadow-lg p-8 text-white mb-8">
            <h2 className="text-3xl font-bold mb-4">Bem-vindo, {profile?.role === 'doador' ? 'Doador' : 'Assinante'}!</h2>
            <p className="text-lg opacity-90">
              Obrigado pelo seu apoio. Aqui você tem acesso a conteúdos exclusivos e recursos antecipados.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div className="bg-white dark:bg-zinc-800 p-6 rounded-lg shadow">
              <h3 className="text-xl font-bold mb-2 dark:text-white">Conteúdos Exclusivos</h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">Acesse artigos técnicos aprofundados apenas para apoiadores.</p>
              <button className="text-blue-600 font-medium hover:underline">Ver artigos premium &rarr;</button>
            </div>

            <div className="bg-white dark:bg-zinc-800 p-6 rounded-lg shadow">
              <h3 className="text-xl font-bold mb-2 dark:text-white">Sem Anúncios</h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">Navegue pelo blog sem interrupções publicitárias.</p>
              <span className="text-green-600 font-medium text-sm bg-green-50 px-2 py-1 rounded">Ativo</span>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  )
}
