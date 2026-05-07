from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas
import models
import schemas
from database import get_db
from auth import get_current_user

router = APIRouter(prefix="/snippets", tags=["Snippets"])


@router.post("/snippets/", response_model=schemas.SnippetResponse, status_code=201)
def create_snippet(
    snippet: schemas.SnippetCreate,
    db: Session = Depends(get_db),
    current_user : models.User =  Depends(get_current_user)
):
    ## Authentication of user
    if snippet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to post on behalf of another user!"
        )

    ### create a new snippet
    new_snippet = models.Post(
        title=snippet.title, content=snippet.content, user_id=snippet.user_id
    )
    db.add(new_snippet)
    db.commit()
    db.refresh(new_snippet)

    return new_snippet
