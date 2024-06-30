from fast_api.models import User


def test_create_user():
    user = User(
        username='Rafael Martini Silva',
        email='rafaelmartinisilva@hotmail.com',
        password='Test123',
    )

    assert user.username == 'Rafael Martini Silva'

    assert user.email == 'rafaelmartinisilva@hotmail.com'

    assert user.password == 'Test123'
