from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.authorization.models import Token
from app.authorization.service import create_access_token, authenticate_user
from dependency_injector.wiring import inject, Provide
from dependencies import Container, Service

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


@router.post("/auth/token/", response_model=Token)
@inject
async def login_for_access_token(db: Service = Depends(Provide[Container.db]),
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
