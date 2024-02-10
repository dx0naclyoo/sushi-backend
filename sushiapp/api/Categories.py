from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import sushiapp.models.Auth as models_Auth
import sushiapp.services.Categories as Services
from sushiapp.database import databaseworker
from sushiapp.models.Categories import CreateCategories, Categories, UpdateCategories
from sushiapp.services.Auth import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/{id}", response_model=Categories)
async def get_categories(
        categories_id: int,
        # user: models_Auth.User = Depends(get_current_user),
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await Services.get_category(session=session, categories_id=categories_id)


@router.get("/", response_model=list[Categories])
async def get_all_categories(
        # user: models_Auth.User = Depends(get_current_user),
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await Services.get_all_categories(session=session)


@router.post("/", response_model=Categories)
async def create_categories(
        data: CreateCategories,
        user: models_Auth.User = Depends(get_current_user),
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await Services.create_category(session=session, category_data=data, user_role=user.role)


@router.put("/{id}", response_model=Categories)
async def update_categories(
        product_id: int,
        data: UpdateCategories,
        user: models_Auth.User = Depends(get_current_user),
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await Services.update_category(
        session=session, category_data=data, category_id=product_id, user_role=user.role
    )


@router.delete("/{id}")
async def delete_categories(
        category_id: int,
        user: models_Auth.User = Depends(get_current_user),
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await Services.delete_category(session=session, category_id=category_id, user_role=user.role)
