from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db


router = APIRouter(prefix = "/snippets", tags = ["Users"])

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate   , db :Session= Depends(get_db) ):
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