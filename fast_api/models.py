from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'  # Nome da tabela dentro do DB

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    # init -> Indica que está entrada não é necessária, visto que o DB vai
    #         gerenciar essa numeração
    # primary_key -> Indica que esta entrada é o indexador do BD

    username: Mapped[str] = mapped_column(unique=True)
    # unique -> restinge que o username tem que ser único no DB

    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    # server_default -> o servidor do DB que define a data e hora