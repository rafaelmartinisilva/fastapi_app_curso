from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import User
from fast_api.schemas import Token
from fast_api.security import (
    create_access_token,
    verify_password,
)

router = APIRouter(
    # Defini o prefixo de todos os endpoints desse router
    prefix='/auth',
    # Organizar as coisas na documentação que estão no mesmo domínio
    tags=['auth'],
)


# ########################################################################### #
# ------------------ Endpoint para criar o token de acesso ------------------ #
# ########################################################################### #
@router.post('/token', response_model=Token)
def login_for_access_token(
    # Formulário para gerar e autorizar o token
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
