# Delete Posts via SQL (Docker PostgreSQL)

> Método alternativo para deletar posts quando a API retorna erro 500.
> O Postiz usa "soft delete" - marca o campo `deletedAt` ao invés de remover a linha.

## Pré-requisitos

- Acesso ao servidor Docker onde o Postiz está rodando
- Container PostgreSQL em execução
- Credenciais do banco (usuário: `eltonjose`, senha: `Pos@280885`)

## Comandos

### 1. Listar posts antes de deletar (segurança)

```bash
docker exec -e PGPASSWORD=Pos@280885 postgres psql -U eltonjose -d postiz -c "SELECT id, \"publishDate\", content FROM \"Post\" WHERE \"publishDate\" >= '2026-02-08 00:00:00' AND \"publishDate\" < '2026-02-09 00:00:00' AND \"deletedAt\" IS NULL;"
```

### 2. Deletar posts (Soft Delete)

```bash
docker exec -e PGPASSWORD=Pos@280885 postgres psql -U eltonjose -d postiz -c "UPDATE \"Post\" SET \"deletedAt\" = NOW() WHERE \"publishDate\" >= '2026-02-08 00:00:00' AND \"publishDate\" < '2026-02-09 00:00:00' AND \"deletedAt\" IS NULL;"
```

## Explicação

| Comando | Descrição |
|---------|-----------|
| `docker exec ... postgres psql ...` | Entra no container do PostgreSQL e executa o comando SQL |
| `UPDATE "Post" SET "deletedAt" = NOW()` | Soft delete - apenas marca a data de deleção ao invés de remover a linha |
| `WHERE ...` | Filtro por data e posts não deletados ainda (`deletedAt IS NULL`) |

## Por que Soft Delete?

- Evita erros de integridade referencial com outras tabelas (estatísticas, logs, etc)
- Permite recuperação de posts se necessário
- Mantém histórico completo para auditoria

## Ajustar por data

Para deletar posts de outra data, altere o `WHERE`:

```bash
# Dia 09/02/2026
WHERE "publishDate" >= '2026-02-09 00:00:00' AND "publishDate" < '2026-02-10 00:00:00'

# Dia específico 10/02/2026
WHERE "publishDate" >= '2026-02-10 00:00:00' AND "publishDate" < '2026-02-11 00:00:00'

# Todos posts futuros
WHERE "publishDate" > NOW() AND "deletedAt" IS NULL
```
