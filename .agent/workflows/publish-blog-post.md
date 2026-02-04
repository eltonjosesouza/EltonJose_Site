---
description: Publicar post do blog em produção via Git e Vercel
---

# Workflow: Publicar Post do Blog

Este workflow automatiza a publicação de posts no blog **eltonjose.com.br** usando Git e deploy automático no Vercel.

## Pré-requisitos

- Post criado em `content/YYYYMMDD_titulo_post/index.mdx`
- Imagens adicionadas em `public/blogs/` (se houver novas)
- Post testado localmente (`npm run dev`)
- Git configurado no projeto

## Fluxo de Publicação

```mermaid
graph LR
    A[Post Criado] --> B[Verificar Mudanças]
    B --> C[Commit Seletivo]
    C --> D[Push para Main]
    D --> E[Vercel Deploy]
    E --> F[Post Publicado]
```

---

## Passos

### 1. Verificar Status do Git

// turbo
```bash
git status
```

**O que verificar**:
- Novos arquivos em `content/`
- Novas imagens em `public/blogs/`
- Arquivos não relacionados ao post (ignorar)

---

### 2. Adicionar Apenas Arquivos do Post

#### Adicionar pasta do post
// turbo
```bash
git add content/YYYYMMDD_titulo_post/
```

#### Adicionar imagens novas (se houver)
// turbo
```bash
git add public/blogs/nome-da-imagem.jpg
```

**Exemplo completo**:
```bash
# Adicionar post
git add content/20260204_implementando_observabilidade/

# Adicionar imagens novas
git add public/blogs/observabilidade-dashboard.png
git add public/blogs/prometheus-grafana.jpg
```

---

### 3. Verificar Arquivos Staged

// turbo
```bash
git status
```

**Confirme que apenas estão staged**:
- ✅ Pasta do post em `content/`
- ✅ Imagens novas em `public/blogs/` (se houver)
- ❌ Nenhum outro arquivo não relacionado

---

### 4. Criar Commit Descritivo

// turbo
```bash
git commit -m "feat: adiciona post sobre [TÍTULO DO POST]"
```

**Padrão de mensagem**:
```bash
# Para novo post
git commit -m "feat: adiciona post sobre [TÍTULO]"

# Para atualização de post
git commit -m "fix: atualiza post sobre [TÍTULO]"

# Para correção de imagens
git commit -m "fix: corrige imagens do post [TÍTULO]"
```

**Exemplos**:
```bash
git commit -m "feat: adiciona post sobre Implementando Observabilidade em Microserviços"
git commit -m "fix: atualiza post sobre CI/CD com GitHub Actions"
git commit -m "fix: corrige imagens do post sobre Kubernetes"
```

---

### 5. Push para Main (Deploy Automático)

// turbo
```bash
git push origin main
```

**O que acontece**:
1. ✅ Código é enviado para o GitHub
2. ✅ Vercel detecta mudanças na branch `main`
3. ✅ Vercel inicia build automático
4. ✅ Deploy em produção (2-5 minutos)

---

### 6. Verificar Deploy no Vercel

Aguarde alguns minutos e verifique:

**Opção 1: Via CLI do Vercel**
```bash
vercel ls
```

**Opção 2: Via Dashboard**
- Acesse: https://vercel.com/dashboard
- Verifique status do deploy
- Confirme que está "Ready"

**Opção 3: Testar URL de Produção**
```bash
curl -I https://www.eltonjose.com.br
```

---

### 7. Validar Post em Produção

Acesse o blog e verifique:
- [ ] Post aparece na listagem
- [ ] Título e descrição corretos
- [ ] Imagens carregando
- [ ] Links funcionando
- [ ] Formatação MDX correta
- [ ] SEO (meta tags, Open Graph)

---

## Comandos Completos (Copiar e Colar)

### Publicar Novo Post

```bash
# 1. Verificar status
git status

# 2. Adicionar post
git add content/YYYYMMDD_titulo_post/

# 3. Adicionar imagens novas (se houver)
git add public/blogs/imagem1.jpg public/blogs/imagem2.png

# 4. Verificar staged
git status

# 5. Commit
git commit -m "feat: adiciona post sobre [TÍTULO]"

# 6. Push (deploy automático)
git push origin main
```

### Atualizar Post Existente

```bash
# 1. Verificar mudanças
git status

# 2. Adicionar apenas o post modificado
git add content/YYYYMMDD_titulo_post/index.mdx

# 3. Commit
git commit -m "fix: atualiza post sobre [TÍTULO]"

# 4. Push
git push origin main
```

---

## Script de Automação

Para facilitar, você pode usar este script:

```bash
#!/bin/bash
# publish-post.sh

# Uso: ./publish-post.sh "20260204_titulo_post" "Título do Post"

POST_DIR=$1
POST_TITLE=$2

if [ -z "$POST_DIR" ] || [ -z "$POST_TITLE" ]; then
    echo "Uso: ./publish-post.sh <pasta_do_post> <título_do_post>"
    echo "Exemplo: ./publish-post.sh 20260204_observabilidade 'Implementando Observabilidade'"
    exit 1
fi

echo "📝 Publicando post: $POST_TITLE"

# Verificar se a pasta existe
if [ ! -d "content/$POST_DIR" ]; then
    echo "❌ Erro: Pasta content/$POST_DIR não encontrada"
    exit 1
fi

# Adicionar post
echo "➕ Adicionando post..."
git add "content/$POST_DIR/"

# Verificar se há imagens novas
echo "🖼️  Verificando imagens novas..."
NEW_IMAGES=$(git status --porcelain public/blogs/ | grep "^??" | awk '{print $2}')

if [ ! -z "$NEW_IMAGES" ]; then
    echo "➕ Adicionando imagens novas:"
    echo "$NEW_IMAGES"
    git add public/blogs/
fi

# Mostrar status
echo ""
echo "📋 Arquivos a serem commitados:"
git status --short

# Confirmar
echo ""
read -p "Continuar com o commit? (s/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "❌ Publicação cancelada"
    git reset
    exit 1
fi

# Commit
echo "💾 Criando commit..."
git commit -m "feat: adiciona post sobre $POST_TITLE"

# Push
echo "🚀 Enviando para produção..."
git push origin main

echo ""
echo "✅ Post publicado com sucesso!"
echo "🔗 Aguarde 2-5 minutos para o deploy no Vercel"
echo "🌐 URL: https://www.eltonjose.com.br"
```

**Como usar o script**:

```bash
# 1. Tornar executável
chmod +x publish-post.sh

# 2. Executar
./publish-post.sh "20260204_observabilidade" "Implementando Observabilidade em Microserviços"
```

---

## Checklist de Publicação

Antes de fazer push:

### Pré-Deploy
- [ ] Post testado localmente
- [ ] Todas as imagens carregando
- [ ] Links verificados
- [ ] Gramática revisada
- [ ] SEO otimizado (título, description, keywords)
- [ ] Frontmatter completo

### Git
- [ ] Apenas arquivos do post staged
- [ ] Imagens novas adicionadas (se houver)
- [ ] Mensagem de commit descritiva
- [ ] Branch correta (main)

### Pós-Deploy
- [ ] Deploy concluído no Vercel
- [ ] Post visível em produção
- [ ] Imagens carregando corretamente
- [ ] Meta tags corretas (verificar com DevTools)
- [ ] Compartilhar nas redes sociais

---

## Troubleshooting

### Problema: Deploy falhou no Vercel

**Solução**:
1. Verificar logs no dashboard do Vercel
2. Testar build localmente: `npm run build`
3. Corrigir erros de build
4. Fazer novo commit e push

### Problema: Imagens não aparecem em produção

**Solução**:
1. Verificar se imagens foram commitadas:
   ```bash
   git ls-files public/blogs/
   ```
2. Verificar caminhos no MDX (devem ser `/blogs/nome.jpg`)
3. Adicionar imagens e fazer novo commit:
   ```bash
   git add public/blogs/
   git commit -m "fix: adiciona imagens do post"
   git push origin main
   ```

### Problema: Post não aparece na listagem

**Solução**:
1. Verificar `isPublished: true` no frontmatter
2. Verificar data `publishedAt` (não pode ser futura)
3. Limpar cache do Vercel e fazer redeploy

### Problema: Arquivos não relacionados foram staged

**Solução**:
```bash
# Resetar staging area
git reset

# Adicionar apenas o que precisa
git add content/YYYYMMDD_titulo_post/
git add public/blogs/imagem-nova.jpg
```

### Problema: Commit com mensagem errada

**Solução**:
```bash
# Se ainda não fez push
git commit --amend -m "feat: mensagem correta"

# Se já fez push (evitar se possível)
git commit --amend -m "feat: mensagem correta"
git push --force origin main
```

---

## Comandos Úteis

### Verificar últimos commits
```bash
git log --oneline -5
```

### Ver diferenças antes de commitar
```bash
git diff content/
```

### Desfazer último commit (antes do push)
```bash
git reset --soft HEAD~1
```

### Ver arquivos que serão commitados
```bash
git diff --cached --name-only
```

### Adicionar apenas imagens novas
```bash
git add public/blogs/*.jpg
git add public/blogs/*.png
```

---

## Fluxo Completo (Exemplo Real)

```bash
# 1. Post criado em: content/20260204_observabilidade_microservicos/
# 2. Imagens em: public/blogs/observabilidade-*.jpg

# Verificar status
git status

# Adicionar post
git add content/20260204_observabilidade_microservicos/

# Adicionar imagens novas
git add public/blogs/observabilidade-dashboard.jpg
git add public/blogs/observabilidade-metrics.jpg

# Verificar staged
git status

# Commit
git commit -m "feat: adiciona post sobre Implementando Observabilidade em Microserviços"

# Push (deploy automático)
git push origin main

# Aguardar deploy (2-5 min)
# Verificar: https://www.eltonjose.com.br
```

---

## Integração com Content Creator

Após criar post com `@content-creator`:

```bash
# 1. Salvar arquivo MDX em content/YYYYMMDD_titulo/index.mdx
# 2. Adicionar imagens em public/blogs/
# 3. Testar localmente: npm run dev
# 4. Usar este workflow para publicar
```

---

## Boas Práticas

✅ **Sempre testar localmente antes de publicar**
✅ **Commitar apenas arquivos relacionados ao post**
✅ **Usar mensagens de commit descritivas**
✅ **Verificar deploy no Vercel antes de compartilhar**
✅ **Fazer backup de imagens importantes**

❌ **Não commitar arquivos de configuração não relacionados**
❌ **Não fazer push direto sem testar**
❌ **Não usar `git add .` (adiciona tudo)**
❌ **Não fazer force push sem necessidade**

---

**Pronto!** Agora você tem um workflow completo e automatizado para publicar posts no blog. 🚀
