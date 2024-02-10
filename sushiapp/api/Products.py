from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import sushiapp.services.Products as services
from sushiapp.database import databaseworker
from sushiapp.models.Products import Product, UpdateProduct, CreateProduct
import sushiapp.tables as tables
import sushiapp.models.Auth as models_Auth
from sushiapp.services.Auth import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/{id}", response_model=Product)
async def get_product(
        product_id: int,
        # user: models_Auth.User = Depends(get_current_user),
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await services.get_product(session=session, product_id=product_id)


@router.get("/", response_model=list[Product])
async def get_all_products(
        # user: models_Auth.User = Depends(get_current_user),
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await services.get_all_products(session=session)


@router.post("/", response_model=Product)
async def create_product(
        data: CreateProduct,
        user: models_Auth.User = Depends(get_current_user),
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await services.create_product(session=session, product_data=data, user_role=user.role)


@router.put("/{id}", response_model=Product)
async def update_product(
        product_id: int,
        data: CreateProduct,
        user: models_Auth.User = Depends(get_current_user),
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await services.update_product(
        session=session, product_data=data, product_id=product_id, user_role=user.role
    )


@router.delete("/{id}")
async def delete_product(
        product_id: int,
        user: models_Auth.User = Depends(get_current_user),
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await services.delete_product(session=session, product_id=product_id, user_role=user.role)








