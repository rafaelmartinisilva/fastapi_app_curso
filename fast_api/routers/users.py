from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import User
from fast_api.schemas import Message, UserList, UserPublic, UserSchema
from fast_api.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(
    # Defini o prefixo de todos os endpoints desse router
    prefix='/users',
    # Organizar as coisas na documentação que estão no mesmo domínio
    tags=['users'],
)


# ########################################################################### #
# ------------------- Endpoint para criar um novo usuário ------------------- #
# ########################################################################### #
@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exist',
            )

        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exist',
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


# ########################################################################### #
# ----------------- Endpoint para listar todos os usuários ------------------ #
# ########################################################################### #
@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 10,
    skip: int = 0,
    session: Session = Depends(get_session),
):
    users = session.scalars(
        select(User).limit(limit=limit).offset(offset=skip)
    )

    return {'users': users}


# ########################################################################### #
# -------------- Endpoint para atualizar um usuário existente --------------- #
# ########################################################################### #
@router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Not enough permission',
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user


# ########################################################################### #
# --------------- Endpoint para excluir um usuário existente ---------------- #
# ########################################################################### #
@router.delete('/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Not enough permission',
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}


# ########################################################################### #
# ----------------- Endpoint para listar um usuário pelo ID ----------------- #
# ########################################################################### #
@router.get('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user
