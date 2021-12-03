from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.authorization.models import Token
from app.authorization.service import get_db, create_access_token, authenticate_user, get_current_user, create_user, \
    get_users
from app.tasks.models import Task
from app.tasks.service import create_task, get_tasks_user, get_tasks
from app.users.data import Base, engine
from app.users.models import User

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


@app.get("/users/all/")
async def get_all(db: Session = Depends(get_db)):
    return get_users(db=db)


@app.post("/users/add/")
def add_user(user: User, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@app.post("/tasks/add/")
def add_task(task: Task, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)


@app.get("/tasks/all/")
def get_all_tasks(db: Session = Depends(get_db)):
    return get_tasks(db=db)


@app.get("/tasks/user_id/{user_id}/")
def get_task(user_id, db: Session = Depends(get_db)):
    return get_tasks_user(db=db, user_id=user_id)


@app.get("/tasks/me/")
async def get_tasks_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_tasks_user(db=db, user_id=current_user.id)
