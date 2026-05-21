# Forró Passos Condutor

Aplicação para cadastrar passos de forró e gerar sequências aleatórias válidas sem repetição, respeitando perna livre inicial.

## Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Docker / Docker Compose
- Frontend simples em HTML/CSS/JS servido pelo backend

## Requisitos

- Python 3.12+
- PostgreSQL 16+

## Executar localmente

1. Crie e ative ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Exporte a variável `DATABASE_URL` (ou use o valor padrão abaixo, que também está em `.env.example`):

```bash
export DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/forro
```

4. Execute migrations:

```bash
alembic upgrade head
```

5. Suba a aplicação:

```bash
uvicorn app.main:app --reload
```

Acesse: `http://localhost:8000`

## Executar com Docker

```bash
docker compose up --build
```

Acesse: `http://localhost:8000`

## Endpoints

- `POST /api/steps` cria passo simples ou composto
- `GET /api/steps` lista passos (incluindo composição quando existir)
- `POST /api/randomize` gera sequências aleatórias sem repetição e sobras

### Passos compostos

- Um passo pode ser simples (`is_composite=false`) ou composto (`is_composite=true`).
- Passo composto deve informar `component_step_ids` com pelo menos 2 passos já existentes, em ordem.
- A ordem da composição é persistida na tabela relacional `step_components`.
- O campo `starts_with_left_free` do passo composto é derivado automaticamente do primeiro componente da sequência.
- O backend valida:
  - existência de todos os componentes;
  - mínimo de 2 componentes;
  - que um passo composto não referencie a si mesmo diretamente.
- Na listagem, cada passo composto retorna `components` na ordem cadastrada.

## Regras de randomização implementadas

- Cada passo possui `name` e `starts_with_left_free`.
- Passos compostos participam normalmente da randomização, usando `starts_with_left_free` final derivado.
- Todo passo termina com a perna oposta livre.
- As sequências são geradas em pares de 2 passos.
- O segundo passo do par sempre começa com a perna oposta ao primeiro.
- Um passo não é reutilizado na mesma randomização.
- O algoritmo consome passos até acabar um dos grupos.
- Passos sem par são retornados em `leftovers`.
