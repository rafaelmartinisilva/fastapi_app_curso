from http import HTTPStatus

from fast_api.schemas import UserPublic


# ########################################################################### #
# --- Testa a criação de um novo usuário
# ########################################################################### #
def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Rafael Martini',
            'email': 'rafaelmartinisilva@hotmail.com',
            'password': 'Test123',
        },
    )

    # Validar o response code
    assert response.status_code == HTTPStatus.CREATED

    # Validar o UserPublic
    assert response.json() == {
        'id': 1,
        'username': 'Rafael Martini',
        'email': 'rafaelmartinisilva@hotmail.com',
    }


# ########################################################################### #
# --- Testa a criação de um novo usuário com um nome já existente
# ########################################################################### #
def test_create_user_user_already_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': user.email,
            'password': user.password,
        },
    )

    # print(user)

    # Validar o response code
    assert response.status_code == HTTPStatus.BAD_REQUEST

    # Validar o UserPublic
    assert response.json() == {
        'detail': 'Username already exist',
    }


# ########################################################################### #
# --- Testa a criação de um novo usuário com um e-mail já existente
# ########################################################################### #
def test_create_user_email_already_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': f'{user.username}1',
            'email': user.email,
            'password': 'test_1+senha',
        },
    )

    # Validar o response code
    assert response.status_code == HTTPStatus.BAD_REQUEST

    # Validar o UserPublic
    assert response.json() == {
        'detail': 'Email already exist',
    }


# ########################################################################### #
# --- Testa a listagem de todos os usuários com um banco de dados vazio
# ########################################################################### #
def test_read_users_without_users(client):
    response = client.get('/users/')

    # Validar o response code
    assert response.status_code == HTTPStatus.OK

    # Validar o UserPublic
    assert response.json() == {'users': []}


# ########################################################################### #
# --- Testa a listagem de todos os usuários
# ########################################################################### #
def test_read_users_with_users(client, user):
    # Converte o user do modelo do SQLAlchemy para o modelo do
    # UserPublic do Pydantic -> utilizar o ConfigDict no schema
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    # Validar o response code
    assert response.status_code == HTTPStatus.OK

    # Validar o UserPublic
    assert response.json() == {
        'users': [
            # Deve retornar o user no formato UserPublic do Pydantic
            user_schema
        ]
    }


# ########################################################################### #
# --- Testa a atualização de um usuário existente
# ########################################################################### #
def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Rafael Martini',
            'email': 'rafaelmartinisilva@gmail.com',
            'password': 'TestRafael',
        },
    )

    # Validar o response code
    assert response.status_code == HTTPStatus.OK

    # Validar o UserPublic
    assert response.json() == {
        'id': user.id,
        'username': 'Rafael Martini',
        'email': 'rafaelmartinisilva@gmail.com',
    }


# ########################################################################### #
# --- Testa a atualização de um usuário não autorizado
# ########################################################################### #
def test_update_user_not_found(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Rafael Martini',
            'email': 'rafaelmartinisilva@gmail.com',
            'password': 'TestRafael',
        },
    )

    # Validar o response code
    assert response.status_code == HTTPStatus.FORBIDDEN

    # Validar o UserPublic
    assert response.json() == {'detail': 'Not enough permissions'}


# ########################################################################### #
# --- Testa a exclusão de um usuário existente
# ########################################################################### #
def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'message': 'User deleted'}


# ########################################################################### #
# --- Testa a exclusão de um usuário não autorizado
# ########################################################################### #
def test_delete_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Validar o response code
    assert response.status_code == HTTPStatus.FORBIDDEN

    # Validar o UserPublic
    assert response.json() == {'detail': 'Not enough permissions'}


# ########################################################################### #
# --- Testa a listagem de um usuário por ID
# ########################################################################### #
def test_read_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'id': user.id,
        'username': f'{user.username}',
        'email': f'{user.email}',
    }


# ########################################################################### #
# --- Testa a listagem de um usuário não encontrado por ID
# ########################################################################### #
def test_read_user_not_found(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'User not found'}
