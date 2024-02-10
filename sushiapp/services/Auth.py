import datetime
from datetime import timedelta

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import sushiapp.models.Auth as models_Auth
import sushiapp.tables as tables
from sushiapp.settings import settings
from sushiapp.tables import Users

oauth_schema = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/sign-in')


def get_current_user(token: str = Depends(oauth_schema)) -> models_Auth.User:
    return validate_token(token)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def validate_token(token: str) -> models_Auth.User:
    exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": 'Bearer'
        })

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError as e:
        raise exceptions from None

    user_data = payload.get('user')

    try:
        user = models_Auth.User.parse_obj(user_data)
    except ValidationError:
        raise exceptions from None

    return user


def create_token(user: tables.Users) -> models_Auth.Token:
    user_data = models_Auth.User.from_orm(user)

    now = datetime.datetime.utcnow()

    payload = {
        'iat': now,
        'nbf': now,
        'exp': now + timedelta(seconds=settings.jwt_expiration),
        'sub': str(user_data.id),
        'user': user_data.dict(),
    }
    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )

    return models_Auth.Token(access_token=token)


async def register_new_user(
        user_data: models_Auth.CreateUser,
        session: AsyncSession) -> models_Auth.Token:

    user = tables.Users(
        username=user_data.username,
        password=hash_password(user_data.password)
    )

    stmt = select(tables.Users).where(tables.Users.username == user_data.username)
    res = await session.execute(stmt)
    db_user = res.scalar()

    exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Users already exist",
        headers={
            "WWW-Authenticate": 'Bearer'
        })

    if db_user:
        raise exceptions

    session.add(user)
    await session.commit()

    return create_token(user)


async def authenticate_user(
        username: str,
        password: str,
        session: AsyncSession) -> models_Auth.Token:

    exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={
            "WWW-Authenticate": 'Bearer'})

    stmt = select(tables.Users).where(tables.Users.username == username)
    res = await session.execute(stmt)
    user = res.scalar()

    if not user:
        raise exceptions

    if not verify_password(password, user.password):
        raise exceptions

    return create_token(user)


async def change_role(
        user_id: int, new_role: tables.UserRole, user_role: tables.UserRole,
        session: AsyncSession
) -> tables.Users:

    stmt = select(tables.Users).where(tables.Users.id == user_id)
    res = await session.execute(stmt)
    new_user = res.scalar()

    if user_role == tables.UserRole.ADMIN:
        new_user.role = new_role
        await session.commit()
        await session.refresh(new_user)

        return new_user

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can update role"
        )




