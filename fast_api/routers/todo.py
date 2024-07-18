from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import Todo, User
from fast_api.schemas import TodoPublic, TodoSchema
from fast_api.security import get_current_user

router = APIRouter(
    prefix='/todos',
    tags=['todos'],
)


SessionTunnel = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic)
def create_todo(todo: TodoSchema, session: SessionTunnel, user: CurrentUser):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
