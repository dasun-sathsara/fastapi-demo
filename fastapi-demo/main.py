import psycopg2
from fastapi import FastAPI

from routers import post


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(post.router)
