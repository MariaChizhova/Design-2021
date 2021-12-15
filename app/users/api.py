from fastapi import Depends, APIRouter, Request
from app.authorization.service import get_current_user, create_user
from app.users.models import User
from app.users.service import get_users, delete_user_by_id, get_user_by_id
from fastapi.responses import HTMLResponse
from dependency_injector.wiring import inject, Provide
from dependencies import Container, Service

router = APIRouter()


@router.get("/users/me/", response_class=HTMLResponse)
@inject
async def get_me(request: Request, current_user: User = Depends(get_current_user),
                 db: Service = Depends(Provide[Container.db])):
    return get_user_by_id(request=request, user_id=current_user.id, db=next(db.get_db()))


@router.get("/users/user_id/{user_id}", response_class=HTMLResponse)
@inject
async def get_user(request: Request, user_id: int, db: Service = Depends(Provide[Container.db])):
    return get_user_by_id(request=request, user_id=user_id, db=next(db.get_db()))


@router.get("/users/all/", response_class=HTMLResponse)
@inject
async def get_all(request: Request, db: Service = Depends(Provide[Container.db])):
    return get_users(request=request, db=next(db.get_db()))


@router.post("/users/add/")
@inject
def add_user(user: User, db: Service = Depends(Provide[Container.db])):
    return create_user(db=next(db.get_db()), user=user)


@router.post("/users/delete/{user_id}/")
@inject
def delete_task(user_id: int, db: Service = Depends(Provide[Container.db])):
    return delete_user_by_id(db=next(db.get_db()), user_id=user_id)
