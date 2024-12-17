from typing import Annotated
from datetime import datetime, timezone, timedelta

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session  # for typing
import jwt
from jwt.exceptions import InvalidTokenError

from .config import config_data
from . import models, schemas
from .database import get_db

AUTH_CONFIG = config_data["auth"]
SECRET_KEY = AUTH_CONFIG["secret_key"]
SIGNING_ALGORITHM = AUTH_CONFIG["signing_algorithm"]
ACCESS_TOKEN_TTL = timedelta(minutes=AUTH_CONFIG["access_token_ttl"])
ACCESS_TOKEN_NBF_LEEWAY = timedelta(seconds=AUTH_CONFIG["access_token_nbf_leeway"])
ACCESS_TOKEN_AUD = AUTH_CONFIG["access_token_aud"]


router = APIRouter(tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


# helper functions to handle authentication
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str, db: Session) -> schemas.UserSchema | None:
    query = select(models.User).where(models.User.user_name == username)

    user_orm = db.execute(query).unique().scalar_one_or_none()
    if user_orm is not None:
        return schemas.UserSchema(
            id=user_orm.id,
            user_name=user_orm.user_name,
            hashed_password=user_orm.password,
            role=user_orm.role,
            is_active=user_orm.is_active,
        )


def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def return_credentials_exception(detail="Could not validate credentials"):
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )
    return cred_exception


# token generator
def create_access_token(sub: str, role: str):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "iat": now,
        "exp": now + ACCESS_TOKEN_TTL,
        "nbf": now - ACCESS_TOKEN_NBF_LEEWAY,
        "aud": ACCESS_TOKEN_AUD,
        "role": role,
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=SIGNING_ALGORITHM)

    return encoded_jwt


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    # authenticate user
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise return_credentials_exception("Incorrect username or password")

    # generate token
    access_token = create_access_token(user.user_name, user.role)

    return {"access_token": access_token, "token_type": "bearer"}


# token validator
async def verify_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[SIGNING_ALGORITHM],
            audience=ACCESS_TOKEN_AUD,
        )
        username: str = payload.get("sub")
        if username is None:
            raise return_credentials_exception("Token has no 'sub' value")

    except jwt.exceptions.InvalidSignatureError as e:
        raise return_credentials_exception(
            f"Authorization token (JWT) signature is invalid: {e}"
        )
    except jwt.exceptions.ExpiredSignatureError as e:
        raise return_credentials_exception(f"Authorization token (JWT) is expired: {e}")
    except jwt.exceptions.InvalidAudienceError as e:
        raise return_credentials_exception(
            f"Authorization token (JWT) specifies the wrong audience: expected '{ACCESS_TOKEN_AUD}': {e}"
        )
    except jwt.exceptions.ImmatureSignatureError as e:
        raise return_credentials_exception(
            f"Authorization token (JWT) is not yet valid: {e}"
        )
    except jwt.exceptions.DecodeError as e:
        raise return_credentials_exception(
            f"Authorization token (JWT) could not be decoded: {e}"
        )
    except Exception as e:
        raise return_credentials_exception(f"Unexpected exception: {e}")

    user = get_user(username, db)
    if user is None:
        raise return_credentials_exception(
            f"User '{username}' is not in approved internal list"
        )

    return user


async def get_current_active_user(
    current_user: Annotated[schemas.UserSchema, Depends(verify_token)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[schemas.UserSchema, Depends(get_current_active_user)],
):
    return current_user
