from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import sushiapp.models.Auth as models_Auth
from sushiapp.database import databaseworker
from sushiapp.services.Auth import get_current_user
import sushiapp.services.Auth as Services

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


@router.get('/user', response_model=models_Auth.User)
async def get_user(
        user: models_Auth.User = Depends(get_current_user)
):
    return user


