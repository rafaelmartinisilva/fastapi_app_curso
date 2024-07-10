from sqlalchemy import select

from fast_api.models import User


# ########################################################################### #
# --- Testa a adição de um usuário no banco de dados
# ########################################################################### #
# session proveniente do conftest que prepara o DB
def test_create_user(session):
    user = User(
        username='Rafael Martini Silva',
        email='rafaelmartinisilva@hotmail.com',
        password='Test123',
    )

    session.add(user)  # adiciona o user na session
    session.commit()  # adiociona o user no DB

    # Seleciona um usuário do DB para a validação
    result = session.scalar(
        select(User).where(User.email == 'rafaelmartinisilva@hotmail.com')
    )

    # Valida o usuário selecionado do DB
    assert result.id == 1
    assert result.username == 'Rafael Martini Silva'
    assert result.email == 'rafaelmartinisilva@hotmail.com'
    assert result.password == 'Test123'
