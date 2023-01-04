import psycopg2
from psycopg2.extras import RealDictCursor
import time

from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


while True:
    try:
        conn = psycopg2.connect("dbname=fastapi user=postgres password=Ds20020618 host=localhost port=5432")
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        print("Database Connection Successfull")
        break
    except psycopg2.Error as e:
        print(e)
        print("Database Connection Unsuccessful")
        print("Retying...")
        time.sleep(3)


@app.get("/posts/")
def get_posts():
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    post = list(filter(lambda post: post["id"] == id, my_posts))
    cursor.execute("""SELECT * FROM post WHERE id=%s""", (id,))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")

    return {"data": post}


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
def add_post(post: Post):
    print(post)
    cursor.execute(
        """INSERT INTO post(title,content,published) VALUES(%s,%s,%s) RETURNING *""", (post.title, post.content, post.published)
    )
    conn.commit()
    new_post = cursor.fetchone()
    return {"date": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = list(filter(lambda post: post["id"] == id, my_posts))
    if len(post) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")

    my_posts.remove(post[0])


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    old_post = list(filter(lambda p: p["id"] == id, my_posts))
    if len(old_post) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")

    index = my_posts.index(old_post[0])
    my_posts[index] = post.dict()

    return {"data": post}
