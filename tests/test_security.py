from http import HTTPStatus

from jwt import decode

from fast_api.security import (
    create_access_token,
    settings,
)


# ########################################################################### #
# --- Testa a criação de um token para o usuário, verificando se o usuário
# está correto e se existe uma informação de expiração de sessão.
# ########################################################################### #
def test_jwt():
    data = {'sub': 'test@test.com'}

    token = create_access_token(data=data)

    result = decode(
        jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert result['sub'] == data['sub']
    assert result['exp']


# ########################################################################### #
# --- Testa a validação de um token inválido gerado
# ########################################################################### #
def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


# ########################################################################### #
# ---
# ########################################################################### #
def test_get_current_user_user_not_found(client):
    data = {}
    token = create_access_token(data=data)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


# ########################################################################### #
# ---
# ########################################################################### #
def test_get_current_user_user_not_found_2(client):
    data = {'sub': 'email@test.com'}
    token = create_access_token(data=data)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
