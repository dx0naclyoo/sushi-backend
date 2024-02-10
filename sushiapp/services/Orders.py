from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import sushiapp.models.Orders as Models
import sushiapp.tables as tables


async def _get(user_id: int, session: AsyncSession, order_id: int) -> tables.Orders:
    order = await (session
                   .scalar(select(tables.Orders)
                           .where(tables.Orders.id == order_id and tables.Orders.user_id == user_id)))
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


async def get_orders(user_id: int, session: AsyncSession) -> list[tables.Orders]:
    stmt = select(tables.Orders).where(tables.Orders.user_id == user_id)
    result: Result = await session.execute(stmt)
    orders = result.scalars().all()
    return list(orders)


async def get_order(user_id: int, session: AsyncSession, order_id) -> tables.Orders:
    return await _get(user_id, session, order_id)


async def create_order(user_id: int, session: AsyncSession, order_data: Models.OrderCreate) -> tables.Orders:
    order = tables.Orders(**order_data.model_dump(), user_id=user_id)
    session.add(order)
    await session.commit()
    # await session.refresh(order)
    return order


async def update_order(
        user_id: int,
        session: AsyncSession,
        order_data: Models.OrderUpdate,
        order_id: int) -> tables.Orders:
    order = await _get(user_id, session, order_id)
    for field, value in order_data:
        setattr(order, field, value)
    await session.commit()
    return order


async def delete_order(
        user_id: int,
        session: AsyncSession,
        order_id: int
):
    order = await _get(user_id, session, order_id)
    await session.delete(order)
    await session.commit()
