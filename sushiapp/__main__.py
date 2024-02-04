import uvicorn
from settings import settings


# Запуск приложения

if __name__ == '__main__':
    uvicorn.run(
    "app:app",
    host=settings.host,
    port=settings.port,
    reload=True)

