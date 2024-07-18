from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


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

    updated_at: Mapped[datetime] = mapped_column(
        init=False, nullable=True, onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class Todo:
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TodoState]

    # Toda tarefa pertence a alguém
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        # nullable=True, default=0
    )
    # server_default -> o servidor do DB que define a data e hora

    updated_at: Mapped[datetime] = mapped_column(
        init=False, nullable=True, onupdate=func.now()
    )
