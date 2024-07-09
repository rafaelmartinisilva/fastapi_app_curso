from datetime import datetime, timedelta

from jwt import encode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

pwd_context = PasswordHash.recommended()


SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE = 30


def get_password_hash(password: str):
    return pwd_context.hash(password=password)


def verify_password(plain_password: str, hashed_password: str):
    pwd_context.verify(password=plain_password, hash=hashed_password)


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
