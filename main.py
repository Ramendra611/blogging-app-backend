from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
from pydantic import BaseModel
from datetime import datetime
from routers.users import router as users_router
# from routers.snippets import router as snippets_router
# from auth import hash_password, verify_password, create_access_token

app = FastAPI(title="Blogging Backend API",
              description="This is the backend for blogging website - Snippets",
              version='1.0.0')


app.include_router(users_router)
# app.include_router(snippets_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Snippets - Micro Blogging website!!"}


