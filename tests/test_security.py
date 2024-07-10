from http import HTTPStatus

from jwt import decode

from fast_api.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
)


# ########################################################################### #
# --- Testa a criação de um token para o usuário, verificando se o usuário
# está correto e se existe uma informação de expiração de sessão.
# ########################################################################### #
def test_jwt():
    data = {'sub': 'test@test.com'}

    token = create_access_token(data=data)

    result = decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])

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
# def test_get_current_user_user_not_found(client, user2, session):
#     data = {'sub': 'rafae@test.com'}
#     token = create_access_token(data=data)
#     print(token)

#     user = get_current_user(session=session, token=token)

#     assert user.status_code == HTTPStatus.UNAUTHORIZED
#     assert user.json() == {'detail': 'Could not validate credentials'}
