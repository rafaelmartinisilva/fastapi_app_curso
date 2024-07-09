from http import HTTPStatus

from fast_api.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert


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


def test_read_users_without_users(client):
    response = client.get('/users/')

    # Validar o response code
    assert response.status_code == HTTPStatus.OK

    # Validar o UserPublic
    assert response.json() == {'users': []}


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


def test_update_user(client, user):
    response = client.put(
        '/users/1',
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
        'id': 1,
        'username': 'Rafael Martini',
        'email': 'rafaelmartinisilva@gmail.com',
    }


def test_update_user_not_found(client, user):
    response = client.put(
        '/users/2',
        json={
            'username': 'Rafael Martini Silva',
            'email': 'rafaelmartinisilva@gmail.com',
            'password': 'TestRafael',
        },
    )

    # Validar o response code
    assert response.status_code == HTTPStatus.NOT_FOUND

    # Validar o UserPublic
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client, user):
    response = client.delete(
        '/users/2',
    )

    # Validar o response code
    assert response.status_code == HTTPStatus.NOT_FOUND

    # Validar o UserPublic
    assert response.json() == {'detail': 'User not found'}


# Modificar esse endpoint mais tarde

# def test_read_user(client):
#     client.post(
#         '/users/',
#         json={
#             'username': 'Rafael Martini',
#             'email': 'rafaelmartinisilva@hotmail.com',
#             'password': 'Test123',
#         },
#     )

#     response = client.get('/users/1')

#     assert response.status_code == HTTPStatus.OK

#     assert response.json() == {
#         'id': 1,
#         'username': 'Rafael Martini',
#         'email': 'rafaelmartinisilva@hotmail.com',
#     }


# def test_read_user_not_found(client):
#     response = client.get('/users/2')

#     assert response.status_code == HTTPStatus.NOT_FOUND

#     assert response.json() == {'detail': 'User not found'}
