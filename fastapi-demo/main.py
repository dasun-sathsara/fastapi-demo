import psycopg2
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

import models
from database import get_db


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


@app.get("/posts/")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")

    return {"data": post}


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
def add_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")

    post.delete()
    db.commit()

    return {"message": "Post deleted"}


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    old_post = post_query.first()

    if old_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {"data": post_query.first()}
