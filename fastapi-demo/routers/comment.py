from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import oauth2
import schemas
from database import get_db


router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentResponse)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{comment.post_id} was not found")

    new_comment = models.Comment(user_id=current_user.id, **comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@router.get("/posts/{id}/comments", response_model=List[schemas.CommentResponse])
def get_comments(id: int, db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(models.Comment.post_id == id).all()

    return comments
