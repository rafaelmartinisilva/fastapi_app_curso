from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


def get_password_hash(password: str):
    return pwd_context.hash(password=password)


def verify_password(plain_password: str, hashed_password: str):
    pwd_context.verify(password=plain_password, hash=hashed_password)
