from http import HTTPStatus


# ########################################################################### #
# --- Testa a criação de um token para o usuário
# ########################################################################### #
def test_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token  # or assert token['access_token']


# ########################################################################### #
# --- Testa a criação de um token para o usuário com e-mail errado
# ########################################################################### #
def test_token_incorrect_user_or_email(client, user):
    response = client.post(
        '/auth/token',
        data={'username': 'raf@hot.com', 'password': user.clean_password},
    )

    # Validar o response code
    assert response.status_code == HTTPStatus.BAD_REQUEST

    # Validar o UserPublic
    assert response.json() == {'detail': 'Incorrect email or password'}


# ########################################################################### #
# --- Testa a criação de um token para o usuário com senha errada
# ########################################################################### #
def test_token_incorrect_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': '12'},
    )

    # Validar o response code
    assert response.status_code == HTTPStatus.BAD_REQUEST

    # Validar o UserPublic
    assert response.json() == {'detail': 'Incorrect email or password'}
