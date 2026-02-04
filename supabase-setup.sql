-- Criar tabela de visualizações
CREATE TABLE IF NOT EXISTS views (
  id SERIAL PRIMARY KEY,
  slug TEXT UNIQUE NOT NULL,
  count INTEGER DEFAULT 0 NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índice para melhorar performance
CREATE INDEX IF NOT EXISTS idx_views_slug ON views(slug);

-- Criar função para incrementar visualizações
CREATE OR REPLACE FUNCTION increment(slug_text TEXT)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO views (slug, count)
  VALUES (slug_text, 1)
  ON CONFLICT (slug)
  DO UPDATE SET
    count = views.count + 1,
    updated_at = NOW();
END;
$$;

-- Habilitar RLS (Row Level Security) - opcional mas recomendado
ALTER TABLE views ENABLE ROW LEVEL SECURITY;

-- Criar política para permitir leitura pública
CREATE POLICY "Allow public read access" ON views
  FOR SELECT
  USING (true);

-- Criar política para permitir incremento via função
CREATE POLICY "Allow increment via function" ON views
  FOR ALL
  USING (true);
