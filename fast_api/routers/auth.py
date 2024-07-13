from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import User
from fast_api.schemas import Token
from fast_api.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(
    # Defini o prefixo de todos os endpoints desse router
    prefix='/auth',
    # Organizar as coisas na documentação que estão no mesmo domínio
    tags=['auth'],
)


# ########################################################################### #
# ---------------------- Criando as variáveis Annotated --------------------- #
# ########################################################################### #
# Ao definir tipos em Python, a nova padronização da PEP8 orienta a inserir um
# "T_" antes da variável tipo.
T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


# ########################################################################### #
# ------------------ Endpoint para criar o token de acesso ------------------ #
# ########################################################################### #
@router.post('/token', response_model=Token)
def login_for_access_token(
    # Formulário para gerar e autorizar o token
    session: T_Session,
    form_data: T_OAuth2Form,
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}


# ########################################################################### #
# ---------------- Endpoint para revalidar o token do usuário --------------- #
# ########################################################################### #
@router.post('/refresh_token', response_model=Token)
def refresh_access_token(user: User = Depends(get_current_user)):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
