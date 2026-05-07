from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db


router = APIRouter(prefix = "/users", tags = ["Users"])

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate,
                db :Session= Depends(get_db) ):
    # get the user from the db
    db_user = db.query(models.User).filter( (models.User.username == user.username) |
                                  (models.User.email == user.email)).first()

    if db_user:# if the user already exists then raise error
        raise HTTPException(status_code=400,
                            detail="Username or Email already registered")
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

@router.get("/{user_id}", response_model =schemas.UserResponse )
def get_user_profile(user_id: int , db :Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    snippets = db.query(models.Post).filter(models.Post.user_id == user_id).all()
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "bio": user.bio,
        "created_at": user.created_at,
        "snippets": snippets
    }