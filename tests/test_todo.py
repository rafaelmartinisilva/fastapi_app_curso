from http import HTTPStatus

from fast_api.models import TodoState
from tests.conftest import TodoFactory


# ########################################################################### #
# --- Testa a criação de uma tarefa todo
# ########################################################################### #
def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'title': 'Test todo',
        'description': 'Test todo description',
        'state': 'draft',
    }


# ########################################################################### #
# --- Testa a listagem de 5 tarefas todo de um usuário específico
# ########################################################################### #
def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5

    session.bulk_save_objects(  # Cria 5 tarefas Todo paral inserir no DB
        TodoFactory.create_batch(5, user_id=user.id)
    )
    session.commit()

    response = client.get(
        '/todos/', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['todos']) == expected_todos


# ########################################################################### #
# --- Testa a paginação para listar 2 tarefas todo de um total de 5
# ########################################################################### #
def test_list_todos_pagination_should_return_2_todos(
    session, client, user, token
):
    expected_todos = 2

    session.bulk_save_objects(  # Cria 5 tarefas Todo paral inserir no DB
        TodoFactory.create_batch(5, user_id=user.id)
    )
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


# ########################################################################### #
# --- Testa o filtro de title para listar as tarefas com o título definido
# ########################################################################### #
def test_list_todos_filter_title_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5

    session.bulk_save_objects(  # Cria 5 tarefas Todo paral inserir no DB
        TodoFactory.create_batch(5, user_id=user.id, title='Test todo 1')
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


# ########################################################################### #
# --- Testa o filtro de desciption para listar as tarefas com a descrição
#     definida
# ########################################################################### #
def test_list_todos_filter_description_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5

    session.bulk_save_objects(  # Cria 5 tarefas Todo paral inserir no DB
        TodoFactory.create_batch(
            5, user_id=user.id, description='description 1'
        )
    )
    session.commit()

    response = client.get(
        '/todos/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


# ########################################################################### #
# --- Testa o filtro de state para listar as tarefas com a descrição definida
# ########################################################################### #
def test_list_todos_filter_state_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5

    session.bulk_save_objects(  # Cria 5 tarefas Todo paral inserir no DB
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft)
    )
    session.commit()

    response = client.get(
        '/todos/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


# ########################################################################### #
# --- Testa uma combinção de filtros para listar as tarefas
# ########################################################################### #
def test_list_todos_filter_combined_should_return_5_todos(
    session, user, client, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title='Test todo combined',
            description='combined description',
            state=TodoState.done,
        )
    )

    session.bulk_save_objects(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='other description',
            state=TodoState.todo,
        )
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test todo combined&description=combined&state=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


# ########################################################################### #
# --- Testa a remoção de uma tarefa todo do DB
# ########################################################################### #
def test_delete_todo(session, user, client, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'message': 'Task has been deleted successfully.'
    }


# ########################################################################### #
# --- Testa a remoção de uma tarefa todo não existente no DB
# ########################################################################### #
def test_delete_todo_error(session, user, client, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()
    # session.refresh(todo) # Não é necessário, mas por quê?

    response = client.delete(
        f'/todos/{3}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'Task not found.'}


# ########################################################################### #
# --- Testa a atualização de uma tarefa todo não existente no DB
# ########################################################################### #
def test_patch_todo_error(session, user, client, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()
    # session.refresh(todo) # Não é necessário, mas por quê?

    response = client.patch(
        f'/todos/{3}', headers={'Authorization': f'Bearer {token}'}, json={}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'Task not found.'}


# ########################################################################### #
# --- Testa a atualização vazia de uma tarefa todo existente no DB
# ########################################################################### #
def test_patch_todo_empty_update(session, user, client, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()
    # session.refresh(todo)  # Não é necessário, mas por quê?

    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={},
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'state': todo.state,
    }


# ########################################################################### #
# --- Testa a atualização vazia de uma tarefa todo existente no DB
# ########################################################################### #
def test_patch_todo(session, user, client, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Test de title update'},
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json()['title'] == 'Test de title update'
