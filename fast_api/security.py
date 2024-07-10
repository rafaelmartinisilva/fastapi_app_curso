from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from fast_api.database import get_session
from fast_api.models import User

pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE = 30


def get_password_hash(password: str):
    return pwd_context.hash(password=password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(password=plain_password, hash=hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    # Adiciona um tempo de 30 minutos para expiração
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE
    )

    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM
    )

    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    # Cria a exceção personalizada
    credential_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if not username:
            raise credential_exception

    except PyJWTError:
        raise credential_exception

    user = session.scalar(select(User).where(User.email == username))

    if not user:
        raise credential_exception

    return user
