from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models
# import schemas
from database import get_db
from pydantic import BaseModel
from datetime import datetime
# from auth import hash_password, verify_password, create_access_token

app = FastAPI(title="Blogging Backend API",
              description="This is the backend for blogging website - Snippets",
              version='1.0.0')


class SnippetBase(BaseModel):
    title: str
    content: str

class SnippetCreate(SnippetBase):
    user_id: int

class SnippetResponse(SnippetBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email : str # todo: we can add a EmailStr
    bio : str

class UserCreate(UserBase):
    # password: str
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime
    snippets: list[SnippetResponse] = []

    class Config:
        from_attributes = True


@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate   , db :Session= Depends(get_db) ):
    # get the user from the db
    db_user = db.query(models.User).filter( (models.User.username == user.username) |
                                  (models.User.email == user.email)).first()

    if db_user:# if the user already exists then raise error
        raise HTTPException(status_code=400, detail="Username or Email already registered")
    # otherwise we will add the user to db
    new_user = models.User(
        username=user.username,
        email=user.email,
        bio=user.bio,
        # hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # return the added user details
    return new_user

# @app.post("/snippets/", response_model=SnippetResponse, status_code=201)
# def create_snippet(
#     snippet: SnippetCreate,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user)
# ):


