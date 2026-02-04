---
description: Criar novo post para o blog usando o agente Content Creator
---

# Workflow: Criar Post para Blog

Este workflow guia a criação de um novo post otimizado para o blog **eltonjose.com.br**.

## Pré-requisitos

- Tema definido
- Público-alvo identificado (devs plenos/seniors, tech leads, heads)
- Palavras-chave pesquisadas (opcional, mas recomendado)

## Passos

### 1. Ativar o Agente Content Creator

```
@content-creator crie um post sobre [TEMA]
```

**Exemplo**:
```
@content-creator crie um post sobre "Como implementar CI/CD com GitHub Actions"
```

### 2. Fornecer Contexto (Opcional)

Se quiser direcionar o conteúdo, forneça:
- Ângulo específico do tema
- Exemplos que gostaria de ver
- Palavras-chave prioritárias
- Extensão desejada

**Exemplo**:
```
@content-creator crie um post sobre "Como implementar CI/CD com GitHub Actions"

Contexto adicional:
- Foco em projetos Node.js
- Incluir exemplo prático de deploy na AWS
- Palavras-chave: CI/CD, GitHub Actions, automação, DevOps
- Público: tech leads que querem implementar na equipe
```

### 3. Revisar o Conteúdo Gerado

O agente irá gerar:
- ✅ Arquivo `index.mdx` completo
- ✅ Estrutura de pasta com nomenclatura correta
- ✅ Sugestões de imagens
- ✅ Resumo com palavras-chave e estrutura

**Verifique**:
- [ ] Frontmatter completo
- [ ] Introdução (mín. 2 parágrafos)
- [ ] Tópicos principais (3-6, cada um com mín. 3 parágrafos)
- [ ] Conclusão (mín. 2 parágrafos)
- [ ] Imagens sugeridas
- [ ] Tom casual mas profissional

### 4. Solicitar Ajustes (Se Necessário)

```
Ajuste o post:
- Adicione mais exemplos práticos no tópico X
- Torne a conclusão mais inspiradora
- Inclua uma seção sobre [TEMA ESPECÍFICO]
```

### 5. Download do Arquivo

O agente disponibilizará o arquivo `index.mdx` para download.

**Salvar em**:
```
content/YYYYMMDD_titulo_do_post/index.mdx
```

### 6. Adicionar Imagens

1. Coloque as imagens sugeridas em `public/blogs/`
2. Verifique se os caminhos no MDX estão corretos
3. Confirme que todas as imagens têm alt text descritivo

### 7. Revisão Final

Antes de publicar:
- [ ] Testar localmente (`npm run dev`)
- [ ] Verificar renderização do MDX
- [ ] Validar links (internos e externos)
- [ ] Confirmar SEO (título, description, keywords)
- [ ] Revisar gramática e ortografia

### 8. Publicar

1. Commit das alterações
2. Push para repositório
3. Deploy (automático ou manual)
4. Compartilhar nas redes sociais

## Comandos Úteis

### Gerar Múltiplas Ideias
```
@content-creator sugira 5 ideias de posts sobre [TEMA AMPLO]
```

### Otimizar Post Existente
```
@content-creator revise e otimize o post em content/[PASTA]/index.mdx
```

### Expandir Tópico
```
@content-creator expanda o tópico [NOME DO TÓPICO] no post [CAMINHO]
```

## Dicas

- **Seja específico**: Quanto mais contexto, melhor o resultado
- **Itere**: Não hesite em pedir ajustes
- **Personalize**: Adicione suas experiências pessoais
- **SEO**: Sempre forneça palavras-chave se possível
- **Imagens**: Use imagens de qualidade e relevantes

## Exemplos de Temas

### Tecnologia
- "Arquitetura de Microserviços: Quando (Não) Usar"
- "Python vs Node.js para Backend: Escolhendo a Stack Certa"
- "Introdução ao Kubernetes para Desenvolvedores"

### Carreira
- "De Desenvolvedor a Tech Lead: Lições dos Primeiros 90 Dias"
- "Como Negociar Salário em Tech: Guia Prático"
- "Soft Skills que Todo Senior Dev Precisa Dominar"

### Tendências
- "IA Generativa no Desenvolvimento: Ferramentas que Uso Diariamente"
- "O Futuro do Frontend: Tendências para 2026"
- "Edge Computing: O Que Você Precisa Saber"

## Troubleshooting

### Post muito genérico
**Solução**: Forneça mais contexto e exemplos específicos

### Tom muito formal
**Solução**: Peça para tornar mais casual e conversacional

### Falta de exemplos práticos
**Solução**: Solicite explicitamente exemplos de código ou casos de uso

### SEO fraco
**Solução**: Forneça palavras-chave e peça otimização específica

---

**Pronto!** Agora você tem um workflow completo para criar posts de alta qualidade para o seu blog.
