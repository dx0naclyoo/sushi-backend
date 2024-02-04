from fastapi import FastAPI
from api import router as api

app = FastAPI()
app.include_router(api)


@app.get("/")
def index():
    return {"message": "Страница index"}
