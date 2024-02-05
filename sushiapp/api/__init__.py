# Пакет исключитель для реализации api

from fastapi import APIRouter

from .Auth import router as auth_router
from .Orders import router as orders_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(orders_router)
