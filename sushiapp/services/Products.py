from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import sushiapp.models.Products as Models
import sushiapp.tables as tables


# [BLOCK] Main Page | Admin operations

async def _get(session: AsyncSession, product_id: int) -> tables.Products:
    product = await (
        session
        .scalar(select(tables.Products).where(tables.Products.id == product_id)))

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


async def get_all_products(session: AsyncSession, limit: int = 10, offset: int = 0) -> list[tables.Orders]:
    stmt = select(tables.Products).limit(limit).offset(offset)
    result: Result = await session.execute(stmt)
    orders = result.scalars().all()
    return list(orders)


async def get_product(session: AsyncSession, product_id) -> tables.Products:
    return await _get(session, product_id)


async def create_product(
        user_role: str, session: AsyncSession, product_data: Models.CreateProduct) -> tables.Products:

    product = tables.Products(**product_data.model_dump())
    if user_role == tables.UserRole.ADMIN:

        stmt = select(tables.Products).where(tables.Products.name == product.name)
        res = await session.execute(stmt)
        prod = res.scalar()

        if prod:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Product already exists"
            )

        session.add(product)
        await session.commit()
        # await session.refresh(order)
        return product

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can create products"
        )


async def update_product(
        product_id: int, user_role: str, session: AsyncSession, product_data: Models.CreateProduct,
) -> tables.Products:
    if user_role == tables.UserRole.ADMIN:
        product = await _get(session, product_id)
        for field, value in product_data:
            setattr(product, field, value)
        await session.commit()
        return product
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can update products"
        )


async def delete_product(
        session: AsyncSession, user_role: str, product_id: int
):
    if user_role == tables.UserRole.ADMIN:
        product = await _get(session, product_id)
        await session.delete(product)
        await session.commit()

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can delete products"
        )

# [BLOCK] Favorite product | User operations



