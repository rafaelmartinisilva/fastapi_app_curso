#!/bin/sh

# Executa as migrações do bando de dados
poetry run alembic upgrade head

# Inicia a aplicação
poetry run fastapi run fast_api/app.py --host 0.0.0.0 --port 9500