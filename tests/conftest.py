import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_api.app import app
from fast_api.database import get_session
from fast_api.models import table_registry


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app=app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    # Cria uma conexão com o DB em memória
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)  # Cria toda a estrtutura do DB

    with Session(engine) as session:
        # Transforma a session engine em um gerador e passa para a chamada da
        # função de test
        yield session

    # O test acontece entre a criação do DB e sua destruição

    table_registry.metadata.drop_all(engine)  # Destrói o DB após o test

    return engine
