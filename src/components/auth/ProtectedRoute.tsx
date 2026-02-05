import { createClient } from '@/src/lib/supabase/server'
import { redirect } from 'next/navigation'
import { Database } from '@/src/types/supabase'

type UserRole = Database['public']['Enums']['user_role']

interface ProtectedRouteProps {
  children: React.ReactNode
  allowedRoles?: UserRole[]
}

export async function ProtectedRoute({ children, allowedRoles }: ProtectedRouteProps) {
  const supabase = await createClient()

  const {
    data: { session },
  } = await supabase.auth.getSession()

  if (!session) {
    redirect('/login')
  }

  if (allowedRoles && allowedRoles.length > 0) {
    const { data: profile } = await supabase
      .from('profiles')
      .select('role')
      .eq('id', session.user.id)
      .single() as any

    // Admin always has access
    if (profile?.role === 'admin') {
      return <>{children}</>
    }

    if (!profile || !allowedRoles.includes(profile.role)) {
      redirect('/unauthorized')
    }
  }

  return <>{children}</>
}
