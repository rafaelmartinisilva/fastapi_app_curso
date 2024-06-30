from http import HTTPStatus


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


def test_read_users(client):
    response = client.get('/users/')

    # Validar o response code
    assert response.status_code == HTTPStatus.OK

    # Validar o UserPublic
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'Rafael Martini',
                'email': 'rafaelmartinisilva@hotmail.com',
            }
        ]
    }
