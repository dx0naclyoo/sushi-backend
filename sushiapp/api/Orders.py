from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import sushiapp.models.Orders as Orders_models
import sushiapp.services.Orders as Orders_services
from sushiapp.database import databaseworker

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=list[Orders_models.Order])
async def get_orders(
        session: AsyncSession = Depends(databaseworker.session_scoped_dependency),

):
    return await Orders_services.get_orders(session=session)


@router.get("/{order_id}", response_model=Orders_models.Order)
async def get_order(
        order_id: int,
        session: AsyncSession = Depends(databaseworker.session_scoped_dependency),

):
    order = await Orders_services.get_order(session=session, order_id=order_id)
    if order is not None:
        return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order {order_id} not found"
    )


@router.post("/", response_model=Orders_models.Order)
async def create_order(
        order_data: Orders_models.OrderCreate,
        session: AsyncSession = Depends(databaseworker.session_scoped_dependency),
):
    return await Orders_services.create_order(session=session, order_data=order_data)
