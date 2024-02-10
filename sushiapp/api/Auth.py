from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import sushiapp.models.Auth as models_Auth
import sushiapp.services.Auth as Services
from sushiapp.database import databaseworker
from sushiapp.services.Auth import get_current_user
import sushiapp.tables as tables


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post('/sign-up')  # register
async def sign_up(
        user_data: models_Auth.CreateUser,
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await Services.register_new_user(session=session, user_data=user_data)


@router.post('/sign-in', response_model=models_Auth.Token)  # login
async def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(databaseworker.get_session)
):
    return await Services.authenticate_user(
        session=session,
        username=form_data.username,
        password=form_data.password)


@router.post("/user/{id}", response_model=models_Auth.User)
async def change_role(
        user_id: int,
        new_role: tables.UserRole = None,
        user: models_Auth.User = Depends(get_current_user),
        session: AsyncSession = Depends(databaseworker.get_session)
) -> tables.Users:
    return await Services.change_role(
        new_role=new_role, user_role=user.role, session=session, user_id=user_id)


@router.get('/user', response_model=models_Auth.User)
async def get_user(
        user: models_Auth.User = Depends(get_current_user)
):
    return user
