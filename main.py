from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.authorization.models import Token
from app.authorization.service import get_db, create_access_token, authenticate_user, get_current_user, create_user
from app.users.data import Base, engine
from app.users.models import User, UserCreate

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
Base.metadata.create_all(bind=engine)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()


@app.post("/auth/token/", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
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


@app.get("/users/me/")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.post("/users/add/")
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)
