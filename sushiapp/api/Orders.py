from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import sushiapp.services.Orders as services
from sushiapp.database import databaseworker
from sushiapp.models.Orders import OrderCreate, Order, OrderUpdate
import sushiapp.tables as tables
import sushiapp.models.Auth as models_Auth
from sushiapp.services.Auth import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/{id}", response_model=Order)
async def get_order(
        order_id: int,
        user: models_Auth.User = Depends(get_current_user),
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await services.get_order(session=session, order_id=order_id, user_id=user.id)


@router.get("/", response_model=list[Order])
async def get_all_order(
        user: models_Auth.User = Depends(get_current_user),
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await services.get_orders(session=session, user_id=user.id)


@router.post("/", response_model=Order)
async def create_order(
        data: OrderCreate,
        user: models_Auth.User = Depends(get_current_user),
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await services.create_order(session=session, order_data=data, user_id=user.id)


@router.put("/{id}", response_model=Order)
async def update_order(
        order_id: int,
        data: OrderUpdate,
        user: models_Auth.User = Depends(get_current_user),
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await services.update_order(session=session, order_data=data, order_id=order_id, user_id=user.id)


@router.delete("/{id}")
async def delete_order(
        order_ip: int,
        user: models_Auth.User = Depends(get_current_user),
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await services.delete_order(order_id=order_ip, session=session, user_id=user.id)








