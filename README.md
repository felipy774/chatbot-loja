# Chatbot da Loja

Chatbot simples para atendimento de clientes, utilizando a API da OpenAI para gerar respostas sobre a disponibilidade de produtos em estoque.

## Tecnologias

- Python
- FastAPI
- OpenAI API
- HTML/CSS/JavaScript
- Pytest
- uv

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua_chave_aqui
```

## Execução

Instale as dependências:

```bash
uv pip install fastapi uvicorn openai python-dotenv pytest
```

Inicie o servidor:

```bash
uv run uvicorn backend.main:app --reload
```

Depois abra o arquivo:

```bash
frontend/index.html
```

## Testes

Execute:

```bash
uv run pytest
```