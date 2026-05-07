from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas

snippets = APIRouter(prefix = "/snippets", tags = ["Snippets"])



# @app.post("/snippets/", response_model=SnippetResponse, status_code=201)
# def create_snippet(
#     snippet: SnippetCreate,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user)
# ):