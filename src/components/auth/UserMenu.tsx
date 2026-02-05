'use client'

import { createClient } from '@/src/lib/supabase/client'
import { useRouter } from 'next/navigation'
import { Database } from '@/src/types/supabase'
import { useEffect, useState } from 'react'

type Profile = Database['public']['Tables']['profiles']['Row']

export function UserMenu() {
  const router = useRouter()
  const supabase = createClient()
  const [profile, setProfile] = useState<Profile | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const getProfile = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      if (user) {
        const { data } = await supabase
          .from('profiles')
          .select('*')
          .eq('id', user.id)
          .single()
        setProfile(data)
      }
      setLoading(false)
    }

    getProfile()
  }, [])

  const handleLogout = async () => {
    await supabase.auth.signOut()
    router.push('/login')
    router.refresh()
  }

  if (loading) return null
  if (!profile) return null

  const getRoleBadge = (role: string) => {
    const badges: Record<string, string> = {
      admin: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
      editor: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
      revisor: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
      assinante: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
      doador: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
      user: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200',
    }
    return badges[role] || badges.user
  }

  return (
    <div className="flex items-center gap-4 p-2 rounded-lg border dark:border-zinc-700 bg-white dark:bg-zinc-800">
      <div className="flex flex-col">
        <div className="flex items-center gap-2">
           <span className="text-sm font-medium dark:text-gray-200">{profile.display_name || 'Usuário'}</span>
           <span className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider ${getRoleBadge(profile.role)}`}>
            {profile.role}
          </span>
        </div>
      </div>
      <button
        onClick={handleLogout}
        className="text-sm text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 font-medium px-3 py-1 rounded hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
      >
        Sair
      </button>
    </div>
  )
}
