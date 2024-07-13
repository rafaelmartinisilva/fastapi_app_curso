from http import HTTPStatus

from freezegun import freeze_time


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


# ########################################################################### #
# --- Testa a validação do token expirado
# ########################################################################### #
def test_token_expired_after_time(client, user):
    # Modifica o tempo para que o datetime.now, por exemplo,
    # identifique a data como 14/07/2023 às 12h.
    with freeze_time('2023-07-14 12:00:00'):
        # Gera o token às 12h
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK

        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        # Verifica o token as 12h31
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'test',
                'email': 'test@test.com',
                'password': 'test',
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


# ########################################################################### #
# --- Testa a revalidação de um token
# ########################################################################### #
def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


# ########################################################################### #
# --- Testa a revalidação do token expirado
# ########################################################################### #
def test_token_expired_dont_refresh(client, user):
    # Modifica o tempo para que o datetime.now, por exemplo,
    # identifique a data como 14/07/2023 às 12h.
    with freeze_time('2023-07-14 12:00:00'):
        # Gera o token às 12h
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK

        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        # Verifica o token as 12h31
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
