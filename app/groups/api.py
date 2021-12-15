from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse

from app.authorization.service import get_current_user
from app.groups.models import Group
from app.groups.service import create_group, get_groups_user, get_groups, delete_group_by_id, get_group_info
from app.users.models import User
from dependency_injector.wiring import inject, Provide
from dependencies import Container, Service

router = APIRouter()


@router.post("/groups/add/")
@inject
def add_group(group: Group, db: Service = Depends(Provide[Container.db])):
    return create_group(db=next(db.get_db()), group=group)


@router.get("/groups/all/", response_class=HTMLResponse)
@inject
def get_all_groups(request: Request, db: Service = Depends(Provide[Container.db])):
    return get_groups(request=request, db=next(db.get_db()))


@router.get("/groups/user_id/{user_id}/", response_class=HTMLResponse)
@inject
def get_groups_by_user_id(request: Request, user_id, db: Service = Depends(Provide[Container.db])):
    return get_groups_user(request=request, db=next(db.get_db()), user_id=user_id)


@router.get("/groups/me/", response_class=HTMLResponse)
@inject
async def get_tasks_me(request: Request, db: Service = Depends(Provide[Container.db]),
                       current_user: User = Depends(get_current_user)):
    return get_groups_user(request=request, db=next(db.get_db()), user_id=current_user.id)


@router.post("/groups/delete/{group_id}/")
@inject
def delete_group(group_id: int, db: Service = Depends(Provide[Container.db])):
    return delete_group_by_id(db=next(db.get_db())(), group_id=group_id)


@router.get("/groups/group_id/{group_id}/", response_class=HTMLResponse)
@inject
def get_group(request: Request, group_id: int, db: Service = Depends(Provide[Container.db])):
    return get_group_info(request, db=next(db.get_db()), group_id=group_id)
