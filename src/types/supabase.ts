export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string
          role: 'admin' | 'editor' | 'revisor' | 'assinante' | 'doador' | 'user'
          display_name: string | null
          avatar_url: string | null
          bio: string | null
          metadata: Json
          created_at: string
          updated_at: string
        }
        Insert: {
          id: string
          role?: 'admin' | 'editor' | 'revisor' | 'assinante' | 'doador' | 'user'
          display_name?: string | null
          avatar_url?: string | null
          bio?: string | null
          metadata?: Json
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          role?: 'admin' | 'editor' | 'revisor' | 'assinante' | 'doador' | 'user'
          display_name?: string | null
          avatar_url?: string | null
          bio?: string | null
          metadata?: Json
          created_at?: string
          updated_at?: string
        }
      }
      posts: {
        Row: {
          id: string
          author_id: string | null
          title: string
          slug: string
          content: string | null
          excerpt: string | null
          status: 'draft' | 'review' | 'published' | 'archived'
          is_premium: boolean
          published_at: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          author_id?: string | null
          title: string
          slug: string
          content?: string | null
          excerpt?: string | null
          status?: 'draft' | 'review' | 'published' | 'archived'
          is_premium?: boolean
          published_at?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          author_id?: string | null
          title?: string
          slug?: string
          content?: string | null
          excerpt?: string | null
          status?: 'draft' | 'review' | 'published' | 'archived'
          is_premium?: boolean
          published_at?: string | null
          created_at?: string
          updated_at?: string
        }
      }
      post_reviews: {
        Row: {
          id: string
          post_id: string
          reviewer_id: string
          status: 'approved' | 'rejected' | 'needs_changes'
          comments: string | null
          created_at: string
        }
        Insert: {
          id?: string
          post_id: string
          reviewer_id: string
          status: 'approved' | 'rejected' | 'needs_changes'
          comments?: string | null
          created_at?: string
        }
        Update: {
          id?: string
          post_id?: string
          reviewer_id?: string
          status?: 'approved' | 'rejected' | 'needs_changes'
          comments?: string | null
          created_at?: string
        }
      }
      donations: {
        Row: {
          id: string
          user_id: string | null
          amount: number
          currency: string
          status: 'pending' | 'completed' | 'failed' | 'refunded'
          payment_method: string | null
          transaction_id: string | null
          metadata: Json
          created_at: string
        }
        Insert: {
          id?: string
          user_id?: string | null
          amount: number
          currency?: string
          status: 'pending' | 'completed' | 'failed' | 'refunded'
          payment_method?: string | null
          transaction_id?: string | null
          metadata?: Json
          created_at?: string
        }
        Update: {
          id?: string
          user_id?: string | null
          amount?: number
          currency?: string
          status?: 'pending' | 'completed' | 'failed' | 'refunded'
          payment_method?: string | null
          transaction_id?: string | null
          metadata?: Json
          created_at?: string
        }
      }
      subscriptions: {
        Row: {
          id: string
          user_id: string
          plan: 'monthly' | 'yearly'
          status: 'active' | 'cancelled' | 'expired'
          started_at: string
          expires_at: string | null
          auto_renew: boolean
          created_at: string
        }
        Insert: {
          id?: string
          user_id: string
          plan: 'monthly' | 'yearly'
          status: 'active' | 'cancelled' | 'expired'
          started_at?: string
          expires_at?: string | null
          auto_renew?: boolean
          created_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          plan?: 'monthly' | 'yearly'
          status?: 'active' | 'cancelled' | 'expired'
          started_at?: string
          expires_at?: string | null
          auto_renew?: boolean
          created_at?: string
        }
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      has_role: {
        Args: {
          required_role: 'admin' | 'editor' | 'revisor' | 'assinante' | 'doador' | 'user'
        }
        Returns: boolean
      }
      has_premium_access: {
        Args: Record<PropertyKey, never>
        Returns: boolean
      }
    }
    Enums: {
      user_role: 'admin' | 'editor' | 'revisor' | 'assinante' | 'doador' | 'user'
      post_status: 'draft' | 'review' | 'published' | 'archived'
    }
  }
}
