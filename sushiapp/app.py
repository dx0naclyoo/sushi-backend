from fastapi import FastAPI

from api import router as api

app = FastAPI()
app.include_router(api, prefix="/api/v1")


@app.get("/")
def index():
    return {"message": "Страница index"}
