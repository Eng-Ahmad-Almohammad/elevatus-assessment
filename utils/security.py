"""This module provide function that we will use for Authentication."""

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

from core.settings import Settings
from users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

settings = Settings()


class TokenData(BaseModel):
    """Class to hold the username (user's email)."""

    email: str | None = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the user password.

    This function will call pwd_context.verify which is an instance
    of CryptContext to verify the password.

    Args:
        plain_password (str): User's plain password.
        hashed_password (str): User's hashed password.

    Returns:
        bool: True if the password matched the hash, else False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash the password.

    Use CryptContext to hash the password.

    Args:
        password (str): the password to hash.

    Returns:
        str: The secret as encoded by the specified algorithm.
    """
    return pwd_context.hash(password)


async def get_user(email: str) -> User | None:
    """Get user from db by email.

    Args:
        email (str): User's email.

    Returns:
        User or None: User if there is user with the provided email or None if not.
    """
    return await User.find_one({"email": email})


async def authenticate_user(email: str, password: str) -> User | bool:
    """Authenticate the user using the email and password.

    Args:
        email (str): User's email
        password (str): User's plain password

    Returns:
        User | bool: if the user is found then return User else False
    """
    user: User | None = await get_user(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Generate JWT access token.

    This function is responsible to generate the JWT token which will include user's email.

    Args:
        data (dict): key is sub and the value is the user's email
        expires_delta (timedelta | None, optional): toke expiration time Defaults to None.

    Returns:
        str: JWT token
    """
    to_encode: dict = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
