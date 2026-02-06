#!/bin/bash
# Script para atualizar variáveis de ambiente no Vercel
# Remove as existentes e adiciona as novas

set -e

echo "🚀 Atualizando variáveis de ambiente no Vercel..."
echo ""

# Função para atualizar uma variável
update_env() {
  local name=$1
  local value=$2

  echo "📝 Atualizando $name..."

  # Remove das 3 ambientes (ignora erros se não existir)
  vercel env rm "$name" production -y 2>/dev/null || true
  vercel env rm "$name" preview -y 2>/dev/null || true
  vercel env rm "$name" development -y 2>/dev/null || true

  # Adiciona nas 3 ambientes
  echo "$value" | vercel env add "$name" production
  echo "$value" | vercel env add "$name" preview
  echo "$value" | vercel env add "$name" development
}

# PostgreSQL
update_env "POSTGRES_URL" "postgres://postgres.ibtazavzmuwgznjabtnf:PM22OPUDsNPxVLFa@aws-0-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require&supa=base-pooler.x"
update_env "POSTGRES_USER" "postgres"
update_env "POSTGRES_HOST" "db.ibtazavzmuwgznjabtnf.supabase.co"
update_env "POSTGRES_PRISMA_URL" "postgres://postgres.ibtazavzmuwgznjabtnf:PM22OPUDsNPxVLFa@aws-0-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require&pgbouncer=true"
update_env "POSTGRES_PASSWORD" "PM22OPUDsNPxVLFa"
update_env "POSTGRES_DATABASE" "postgres"
update_env "POSTGRES_URL_NON_POOLING" "postgres://postgres.ibtazavzmuwgznjabtnf:PM22OPUDsNPxVLFa@aws-0-sa-east-1.pooler.supabase.com:5432/postgres?sslmode=require"

# Supabase
update_env "SUPABASE_JWT_SECRET" "4OC69RvLQmJMAp17OEcLGrf4AlAzgAYgCcL3ZnonH75srnxplq5UyzUyclIOHuiRy9C6omILBKEQnpJN6YEyZA=="
update_env "NEXT_PUBLIC_SUPABASE_ANON_KEY" "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlidGF6YXZ6bXV3Z3puamFidG5mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk5NjExMDYsImV4cCI6MjA4NTUzNzEwNn0.jgkdEnk9mJXg4ZKkSY3miQrqnWimOg2UMDz6wJMUhvY"
update_env "SUPABASE_URL" "https://ibtazavzmuwgznjabtnf.supabase.co"
update_env "SUPABASE_ANON_KEY" "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlidGF6YXZ6bXV3Z3puamFidG5mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk5NjExMDYsImV4cCI6MjA4NTUzNzEwNn0.jgkdEnk9mJXg4ZKkSY3miQrqnWimOg2UMDz6wJMUhvY"
update_env "NEXT_PUBLIC_SUPABASE_URL" "https://ibtazavzmuwgznjabtnf.supabase.co"
update_env "SUPABASE_SERVICE_ROLE_KEY" "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlidGF6YXZ6bXV3Z3puamFidG5mIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTk2MTEwNiwiZXhwIjoyMDg1NTM3MTA2fQ.XPP9zB1fgQo0w_UcbXQiaEppFgIITLVii1nCloDSp9w"

echo ""
echo "✅ Todas as variáveis foram atualizadas com sucesso!"
echo ""
echo "⚠️  Próximos passos:"
echo "   1. Verifique as variáveis: vercel env ls"
echo "   2. Faça redeploy para aplicar: vercel --prod"
echo ""
