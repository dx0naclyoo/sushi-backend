from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import sushiapp.models.Categories as Models
import sushiapp.tables as tables


async def _get(session: AsyncSession, categories_id: int) -> tables.Categories:
    category = await (
        session
        .scalar(select(tables.Categories).where(tables.Categories.id == categories_id)))

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


async def get_all_categories(
        session: AsyncSession, limit: int = 10, offset: int = 0) -> list[tables.Categories]:

    stmt = select(tables.Categories).limit(limit).offset(offset)
    result: Result = await session.execute(stmt)
    category = result.scalars().all()
    return list(category)


async def get_category(session: AsyncSession, categories_id) -> tables.Categories:
    return await _get(session, categories_id)


async def create_category(
        user_role: str, session: AsyncSession, category_data: Models.CreateCategories) -> tables.Categories:

    category = tables.Categories(**category_data.model_dump())
    if user_role == tables.UserRole.ADMIN:

        stmt = select(tables.Categories).where(tables.Categories.name == category.name)
        res = await session.execute(stmt)
        cat = res.scalar()

        if cat:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Category already exists"
            )

        session.add(category)
        await session.commit()
        # await session.refresh(order)
        return category

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can create category"
        )


async def update_category(
        category_id: int, user_role: str, session: AsyncSession, category_data: Models.UpdateCategories,
) -> tables.Categories:

    if user_role == tables.UserRole.ADMIN:
        category = await _get(session, category_id)
        for field, value in category_data:
            setattr(category, field, value)
        await session.commit()
        return category
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can update products"
        )


async def delete_category(
        session: AsyncSession, user_role: str, category_id: int
):

    if user_role == tables.UserRole.ADMIN:
        category = await _get(session, category_id)
        await session.delete(category)
        await session.commit()

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can delete products"
        )
