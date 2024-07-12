import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_api.app import app
from fast_api.database import get_session
from fast_api.models import User, table_registry
from fast_api.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:  # Determine o metadado da classe que o factory irá construir
        model = User

    # Cria o username de maneira sequencial
    username = factory.Sequence(lambda n: f'test_{n}')
    # obj = self e o self é o model
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}+senha')

    print(username)


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


@pytest.fixture()
def user(session):
    password = 'test_1+senha'

    # Reset the sequence to start from 1
    # UserFactory.reset_sequence(1)

    user_fake = UserFactory(password=get_password_hash(password=password))

    session.add(user_fake)
    session.commit()
    session.refresh(user_fake)

    # Monkey Patch (altera o objeto em tempo de execução)
    # Cria um atributo para manter o password sem hash
    user_fake.clean_password = password

    return user_fake


@pytest.fixture()
def other_user(session):
    password = 'test_2+senha'

    # Reset the sequence to start from 1
    # UserFactory.reset_sequence(1)

    user_fake = UserFactory(password=get_password_hash(password=password))

    session.add(user_fake)
    session.commit()
    session.refresh(user_fake)

    # Monkey Patch (altera o objeto em tempo de execução)
    # Cria um atributo para manter o password sem hash
    user_fake.clean_password = password

    return user_fake


@pytest.fixture()
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']
