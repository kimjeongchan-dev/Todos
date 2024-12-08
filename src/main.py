from fastapi import FastAPI

from api import todo, user


app = FastAPI()
app.include_router(todo.router)
app.include_router(user.router)

@app.get("/healthcheck", status_code=200)
def healthcheck_handler() -> dict[str, str]:
    return {"status": "ok"}