from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_api.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


# Para códigos que não podem ser coberto pelos testes, deve-se informar
# ao pytest que ele não deve analisar o código. Isso é indicado com a
# descrição abaixo.
def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
