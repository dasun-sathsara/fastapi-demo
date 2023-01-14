# FastAPI Demo

Simple blog API built with FastAPI and PostgreSQL. Users can create posts, comment on posts and like posts.

### Features

- Create, read, update and delete posts
- User signup and login with JWT
- Like and unlike posts
- Comment on posts

### Run

Create a database named fastapi in Postgres first. Then install dependencies with Poetry and start the server from the project folder.

```bash
cd fastapi-demo
poetry install
uvicorn main:app --reload
```
