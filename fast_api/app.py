from http import HTTPStatus

from fastapi import FastAPI

from fast_api.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []  # Criação do banco de dados temporário para testar o CRUD


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}
