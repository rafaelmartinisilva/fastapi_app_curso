from http import HTTPStatus

from fastapi import FastAPI

from fast_api.schemas import Message, UserSchema, UserPublic

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/users/', response_model=UserPublic)
def create_user(user: UserSchema):
    return user
