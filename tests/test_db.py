from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_api.models import User, table_registry


def test_create_user():
    engine = create_engine(  # Cria uma conexão com o DB em memória
        'sqlite:///:memory:'
    )

    table_registry.metadata.create_all(engine)  # Cria toda a estrtutura do DB

    # Session -> camada intermediário entre o código e o DB.
    with Session(engine) as session:
        user = User(
            username='Rafael Martini Silva',
            email='rafaelmartinisilva@hotmail.com',
            password='Test123',
        )

        session.add(user)  # adiciona o user na session
        session.commit()  # adiociona o user no DB
        session.refresh(user)  # atualiza o user criado com todos os dados

    assert user.id == 1
    assert user.username == 'Rafael Martini Silva'
    assert user.email == 'rafaelmartinisilva@hotmail.com'
    assert user.password == 'Test123'
