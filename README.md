# Pescador Vercel Flask

Aplicação Flask com login via Supabase, wizard multi-step e deploy compatível com Vercel.

## Instalação

```bash
pip install -r requirements.txt
```

## Ambiente virtual

Ative o ambiente antes de rodar localmente.

## Variáveis de ambiente

Copie o arquivo de exemplo e ajuste os valores:

```bash
cp .env.example .env
```

Variáveis usadas:
- `SECRET_KEY`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY` ou `publish`
- `SUPABASE_SERVICE_ROLE_KEY` quando necessário
- `SUPABASE_KEY` como fallback

## Rodar localmente

```bash
flask --app app:create_app run
```

## Deploy na Vercel

1. Instale a CLI da Vercel.
2. Faça login com `vercel`.
3. Publique o projeto com:

```bash
vercel
```

O deploy usa `api/index.py` como entrypoint serverless.

## Integração Supabase

A aplicação usa `python-dotenv` para carregar `.env` e inicializa o client do Supabase em `app/services/supabase_client.py`.

Observações:
- O login usa `sign_in_with_password`.
- A submissão do formulário envia os dados para a tabela `coletas`.
- Futuras validações e auditoria podem ser adicionadas sem mudar a estrutura do deploy.
