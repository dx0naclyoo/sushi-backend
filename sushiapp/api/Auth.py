from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from sushiapp.models.Auth import User, CreateUser, Token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get('/sign-up', response_model=Token)  # register
def sign_up():
    return


@router.post('/sign-in', response_model=Token)  # login
def sign_in():
    return
