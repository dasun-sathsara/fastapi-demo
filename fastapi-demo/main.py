import psycopg2
from fastapi import FastAPI

from routers import auth, comment, post, user, vote


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(comment.router)
