from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import timedelta
import re, uuid

from .admin_schemas import Admin, AdminForSignUp, TokenData, Token, Filter
from .admin_crud import get_admin, get_admin_with_id, create_admin_in_db, get_url_list, delete_url_db
from ...models import URLFilter
from ...database import get_db
from ...utils.auth import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, verify_password
from ...env import JWT_SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/token")

routes = APIRouter(
    tags=["admin"],
    prefix="/api/admin"
)


def authenticate_admin(db: Session, username: str, password: str):
    admin = get_admin(db, username)
    if not admin:
        return False
    if not verify_password(password, admin.password):
        return False
    return admin


async def get_current_admin(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception

    admin = get_admin_with_id(db, id=token_data.id)
    if admin is None:
        raise credentials_exception

    return admin


@routes.post("/token")
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    if len(form_data.username) == 0 or len(form_data.password) == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    admin = authenticate_admin(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(admin.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@routes.post("/create_admin")
async def create_admin_account(item: AdminForSignUp, token: Annotated[str, Depends(get_current_admin)], db: Session = Depends(get_db)):
    admin_exist = get_admin(db, item.username)
    if len(item.username) == 0 or re.fullmatch(r"[A-Za-z0-9_]+", item.username) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if len(item.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if admin_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exist username",
            headers={"WWW-Authenticate": "Bearer"}
        )
    else:
        admin = create_admin_in_db(db, item.username, item.password)
        return { "message": "Admin account is created successfully"}


@routes.get("/me")
async def get_admin_me(current_admin: Annotated[Admin, Depends(get_current_admin)]):
    return Admin(username=current_admin.username)


# get shorten url list
@routes.get("/urls")
async def get_urls(start: int, limit: int, token: Annotated[str, Depends(get_current_admin)], db: Session = Depends(get_db)):
    if start < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid parameters",
            headers={"WWW-Authenticate": "Bearer"}
        )

    url_list = get_url_list(db, start, limit)

    return url_list


# delete shorten url
@routes.delete("/urls")
async def delete_url(key: str, token: Annotated[str, Depends(get_current_admin)], db: Session = Depends(get_db)):
    if len(key) == 0 or delete_url_db(db, key) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Key not exist",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return {"success": True}


# get url filters list
@routes.get("/filters")
async def get_filters(start: int, limit: int, token: Annotated[str, Depends(get_current_admin)], db: Session = Depends(get_db)):
    if start < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid parameters",
            headers={"WWW-Authenticate": "Bearer"}
        )
    filters = db.query(URLFilter).order_by(URLFilter.created_at.desc()).offset(start).limit(limit).all()
    return filters


# create new filter
@routes.post("/filters")
async def create_filter(item: Filter, token: Annotated[str, Depends(get_current_admin)], db: Session = Depends(get_db)):
    url_filter = URLFilter(
        filter = item.url_filter
    )
    db.add(url_filter)
    db.commit()
    return {"success": True}


# delete url filter
@routes.delete("/filters")
async def delete_filter(id: str, token: Annotated[str, Depends(get_current_admin)], db: Session = Depends(get_db)):
    try:
        uuid.UUID(id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID",
            headers={"WWW-Authenticate": "Bearer"}
        )
    filter = db.query(URLFilter).filter(URLFilter.id == id).first()
    if filter:
        db.delete(filter)
        db.commit()
        return {"success": True}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="ID not exist",
        headers={"WWW-Authenticate": "Bearer"}
    )
