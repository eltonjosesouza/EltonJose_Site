# Supabase Setup para Contador de Visualizações

Este projeto utiliza Supabase para armazenar e incrementar o número de visualizações dos posts do blog. Caso você troque de projeto Supabase, é necessário criar manualmente a tabela e a função (RPC) que o contador utiliza.

## 1. Tabela `views`

Crie a tabela `views` para armazenar o slug do post e o número de visualizações:

```sql
create table if not exists views (
  slug text primary key,
  count bigint default 0
);
```

## 2. Função RPC `increment`

Crie a função (RPC) `increment` para atualizar o contador de visualizações de um post:

```sql
create or replace function increment(slug_text text)
returns void as $$
begin
  insert into views (slug, count)
    values (slug_text, 1)
    on conflict (slug) do update
      set count = views.count + 1;
end;
$$ language plpgsql;
```

> **Importante:** O parâmetro da função deve ser `slug_text` para ser compatível com o código do projeto.

## 3. Passo a Passo para Configuração

1. Acesse o painel do Supabase do seu projeto.
2. Vá em **SQL Editor**.
3. Cole e execute o script da tabela `views`.
4. Se já existir uma função `increment`, rode antes:
   ```sql
   drop function if exists increment(text);
   ```
5. Cole e execute o script da função `increment` (veja exemplo abaixo).
6. Execute também os comandos de permissão e política de acesso (veja exemplos abaixo).
7. Pronto! O contador de views estará funcional.

## 4. Permissões e Políticas (Essencial!)

Execute também:

```sql
-- Permitir SELECT na tabela para todos
grant select on table views to anon, authenticated;

-- Ativar RLS e liberar leitura
alter table views enable row level security;
create policy "Allow public read" on views for select using (true);

-- Permitir execução da função
grant execute on function public.increment(text) to anon, authenticated;
```

## 5. Solução de Problemas

- **Erro 404 no endpoint `/rpc/increment`**: Verifique se a função existe, está no schema `public`, tem parâmetro `slug_text` e foi dada permissão de execução.
- **Erro 406 no endpoint `/views`**: Verifique se a tabela existe, se o RLS está ativo e se a política de leitura foi criada.
- **Erro ao criar função**: Se aparecer erro sobre nome de parâmetro, rode primeiro o `drop function`.

## 6. Recomendações

- Sempre execute esses scripts ao migrar para um novo projeto Supabase.
- Documente alterações futuras neste arquivo.
- Se alterar a estrutura do contador, atualize também este documento.

---

> **Referência:**
> O contador de visualizações depende dos endpoints `/rest/v1/views` e `/rest/v1/rpc/increment` do Supabase.
> Se receber erro 404 ou 406 nesses endpoints, revise esta documentação e os scripts acima.
