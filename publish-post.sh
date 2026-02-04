#!/bin/bash
# publish-post.sh
# Script para publicar posts do blog automaticamente

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Uso: ./publish-post.sh "20260204_titulo_post" "Título do Post"

POST_DIR=$1
POST_TITLE=$2

# Função para exibir uso
show_usage() {
    echo -e "${YELLOW}Uso:${NC} ./publish-post.sh <pasta_do_post> <título_do_post>"
    echo -e "${YELLOW}Exemplo:${NC} ./publish-post.sh 20260204_observabilidade 'Implementando Observabilidade'"
    exit 1
}

# Validar argumentos
if [ -z "$POST_DIR" ] || [ -z "$POST_TITLE" ]; then
    show_usage
fi

echo -e "${BLUE}📝 Publicando post:${NC} $POST_TITLE"
echo ""

# Verificar se a pasta existe
if [ ! -d "content/$POST_DIR" ]; then
    echo -e "${RED}❌ Erro: Pasta content/$POST_DIR não encontrada${NC}"
    exit 1
fi

# Verificar se há mudanças não commitadas
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}⚠️  Há mudanças não commitadas no repositório${NC}"
fi

# Adicionar post
echo -e "${GREEN}➕ Adicionando post...${NC}"
git add "content/$POST_DIR/"

# Verificar se há imagens novas
echo -e "${BLUE}🖼️  Verificando imagens novas...${NC}"
NEW_IMAGES=$(git status --porcelain public/blogs/ 2>/dev/null | grep "^??" | awk '{print $2}')

if [ ! -z "$NEW_IMAGES" ]; then
    echo -e "${GREEN}➕ Adicionando imagens novas:${NC}"
    echo "$NEW_IMAGES" | sed 's/^/   /'
    git add public/blogs/
else
    echo -e "${YELLOW}   Nenhuma imagem nova detectada${NC}"
fi

# Mostrar status
echo ""
echo -e "${BLUE}📋 Arquivos a serem commitados:${NC}"
git status --short | grep "^[AM]" | sed 's/^/   /'

# Confirmar
echo ""
read -p "$(echo -e ${YELLOW}Continuar com o commit? \(s/n\)${NC} )" -n 1 -r
echo

if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo -e "${RED}❌ Publicação cancelada${NC}"
    git reset
    exit 1
fi

# Commit
echo -e "${GREEN}💾 Criando commit...${NC}"
git commit -m "feat: adiciona post sobre $POST_TITLE"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erro ao criar commit${NC}"
    exit 1
fi

# Push
echo -e "${BLUE}🚀 Enviando para produção...${NC}"
git push origin main

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erro ao fazer push${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Post publicado com sucesso!${NC}"
echo -e "${BLUE}🔗 Aguarde 2-5 minutos para o deploy no Vercel${NC}"
echo -e "${BLUE}🌐 URL:${NC} https://www.eltonjose.com.br"
echo ""
