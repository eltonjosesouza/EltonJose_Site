# Social Media Post Models

> JSON schemas para integração com Postiz API - agendamento e publicação em redes sociais.

---

## Visão Geral

Estes modelos definem a estrutura de dados para criação de posts em diferentes plataformas via API do Postiz.

| Arquivo                | Plataforma | Tipo de Post                               |
| ---------------------- | ---------- | ------------------------------------------ |
| `linkedin-post.json`   | LinkedIn   | Post com carrossel de imagens              |
| `facebook-json.json`   | Facebook   | Post com imagem e link                     |
| `instagram-story.json` | Instagram  | Story (imagem vertical)                    |
| `instagram-post.json`  | Instagram  | Post de feed (imagem + legenda + hashtags) |

---

## Estrutura Base

Todos os modelos compartilham esta estrutura raiz:

```json
{
    "type": "schedule" | "now",
    "date": "ISO8601",
    "shortLink": boolean,
    "tags": string[],
    "posts": PostItem[]
}
```

| Campo       | Tipo    | Descrição                                                     |
| ----------- | ------- | ------------------------------------------------------------- |
| `type`      | string  | `schedule` (agendar) ou `now` (publicar imediatamente)        |
| `date`      | string  | Data/hora em formato ISO8601 (ex: `2024-12-14T10:00:00.000Z`) |
| `shortLink` | boolean | Se deve gerar link encurtado                                  |
| `tags`      | array   | Tags para organização interna                                 |
| `posts`     | array   | Lista de posts por integração                                 |

---

## PostItem Structure

```json
{
    "integration": {
        "id": "integration-id"
    },
    "value": ContentItem[],
    "settings": PlatformSettings
}
```

### ContentItem

```json
{
  "content": "Texto do post",
  "image": [
    {
      "id": "unique-image-id",
      "path": "https://uploads.postiz.com/imagem.jpg"
    }
  ]
}
```

---

## Configurações por Plataforma

### LinkedIn

**Arquivo:** `linkedin-post.json`

**Features suportadas:**

- Carrossel de múltiplas imagens (`post_as_images_carousel: true`)
- Texto formatado com links e hashtags no campo `content`

**Content:**

```json
{
  "content": "Texto do post com link https://exemplo.com e #hashtags #linkedin"
}
```

**Settings:**

```json
{
  "__type": "linkedin",
  "post_as_images_carousel": true
}
```

### Facebook

**Arquivo:** `facebook-json.json`

**Features suportadas:**

- Post com imagem
- Link externo anexado (no settings.url)
- Hashtags no campo `content`

**Content:**

```json
{
  "content": "Texto do post com #hashtags #facebook 🎉"
}
```

**Settings:**

```json
{
  "__type": "facebook",
  "url": "https://exemplo.com/link"
}
```

### Instagram Story

**Arquivo:** `instagram-story.json`

**Features suportadas:**

- Imagem em formato vertical (9:16)
- Publicação imediata (`type: "now"`)
- Content geralmente vazio para stories

**Settings:**

```json
{
  "__type": "instagram",
  "post_type": "story"
}
```

### Instagram Post (Feed)

**Arquivo:** `instagram-post.json`

**Features suportadas:**

- Imagem quadrada ou vertical para feed
- Legenda com texto formatado, emojis e hashtags no campo `content`
- Agendamento de publicação
- Colaboradores (opcional)

**Content:**

```json
{
  "content": "Legenda do post com emojis ✨ e #hashtags #instagram #post"
}
```

**Settings:**

```json
{
  "__type": "instagram",
  "post_type": "post",
  "collaborators": []
}
```

---

## Como Usar

1. Copie o template da plataforma desejada
2. Substitua os placeholders:
   - `your-[platform]-integration-id` → ID real da integração
   - URLs de imagem → URLs válidas
3. Ajuste `type` e `date` conforme necessidade
4. Envie via API do Postiz

---

## Placeholders Comuns

| Placeholder                      | Significado                          |
| -------------------------------- | ------------------------------------ |
| `your-linkedin-integration-id`   | ID da integração LinkedIn no Postiz  |
| `your-facebook-integration-id`   | ID da integração Facebook no Postiz  |
| `your-instagram-integration-id`  | ID da integração Instagram no Postiz |
| `https://uploads.postiz.com/...` | URL da imagem no Postiz              |

---

## Referência da API

- [Introdução](https://docs.postiz.com/public-api/introduction)
- [Listar Integrações](https://docs.postiz.com/public-api/integrations/list)
- [Verificar Conexão](https://docs.postiz.com/public-api/integrations/is-connected)
- [Buscar Slot](https://docs.postiz.com/public-api/integrations/find-slot)
- [Listar Posts](https://docs.postiz.com/public-api/posts/list)
- [Criar Post](https://docs.postiz.com/public-api/posts/create)
- [Deletar Post](https://docs.postiz.com/public-api/posts/delete)
- [Upload de Arquivo](https://docs.postiz.com/public-api/uploads/upload-file)
- [Upload de URL](https://docs.postiz.com/public-api/uploads/upload-from-url)
- [Provider LinkedIn](https://docs.postiz.com/public-api/providers/linkedin)
- [Provider Facebook](https://docs.postiz.com/public-api/providers/facebook)
- [Provider Instagram](https://docs.postiz.com/public-api/providers/instagram)
