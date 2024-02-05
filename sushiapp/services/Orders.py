from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import sushiapp.models.Orders as models_order
import sushiapp.tables as tables


async def get_orders(session: AsyncSession) -> list[models_order.Order]:
    query = select(tables.Orders).order_by(tables.Orders.id)
    result: Result = await session.execute(query)
    orders = result.scalars().all()
    return list(orders)


async def get_order(session: AsyncSession, order_id) -> models_order.Order | None:
    return await session.get(tables.Products, order_id)


async def create_order(session: AsyncSession, order_data: models_order.OrderCreate) -> models_order.Order:
    order = models_order.Order(**order_data.model_dump())
    session.add(order)
    await session.commit()
    # await session.refresh(order)
    return order

# async def main():
#     async with databaseworker.session_dependency() as session:
#         pass
#
# if __name__ == '__main__':
#     asyncio.run(main())
