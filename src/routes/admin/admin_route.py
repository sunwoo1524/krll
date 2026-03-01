from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from typing import Annotated
import re, uuid, time

from .admin_schemas import Admin, AdminForSignUp, Filter
from .admin_crud import get_admin, get_admin_with_id, create_admin_in_db, get_url_list, delete_url_db
from ...models import URLFilter
from ...database import get_db
from ...utils.auth import (
    SESSION_COOKIE_NAME, SESSION_MAX_AGE, SESSION_RENEW_BEFORE,
    create_session_token, verify_session_token, verify_password,
)

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


def get_current_admin(request: Request, response: Response, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        raise credentials_exception

    result = verify_session_token(token)
    if result is None:
        raise credentials_exception
    admin_id, issued_at = result

    admin = get_admin_with_id(db, id=admin_id)
    if admin is None:
        raise credentials_exception

    # Renew the cookie when less than half of its lifetime remains
    elapsed = int(time.time()) - issued_at
    if elapsed > SESSION_MAX_AGE - SESSION_RENEW_BEFORE:
        new_token = create_session_token(str(admin.id))
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=new_token,
            max_age=SESSION_MAX_AGE,
            httponly=True,
            secure=True,
            samesite="strict",
        )

    return admin


@routes.post("/login")
async def login(request: Request, response: Response, db: Session = Depends(get_db)):
    form = await request.form()
    username = form.get("username", "")
    password = form.get("password", "")

    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    admin = authenticate_admin(db, username, password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    session_token = create_session_token(str(admin.id))
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_token,
        max_age=SESSION_MAX_AGE,
        httponly=True,
        secure=True,
        samesite="strict",
    )
    return {"success": True}


@routes.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key=SESSION_COOKIE_NAME, secure=True, samesite="strict")
    return {"success": True}


@routes.post("/create_admin")
async def create_admin_account(
    item: AdminForSignUp,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    db: Session = Depends(get_db),
):
    if len(item.username) == 0 or re.fullmatch(r"[A-Za-z0-9_]+", item.username) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username",
        )

    if len(item.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password",
        )

    if get_admin(db, item.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exist username",
        )

    create_admin_in_db(db, item.username, item.password)
    return {"message": "Admin account is created successfully"}


@routes.get("/me")
async def get_admin_me(current_admin: Annotated[Admin, Depends(get_current_admin)]):
    return {"username": current_admin.username}


# get shorten url list
@routes.get("/urls")
async def get_urls(
    start: int,
    limit: int,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    db: Session = Depends(get_db),
):
    if start < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid parameters",
        )
    return get_url_list(db, start, limit)


# delete shorten url
@routes.delete("/urls")
async def delete_url(
    key: str,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    db: Session = Depends(get_db),
):
    if len(key) == 0 or delete_url_db(db, key) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Key not exist",
        )
    return {"success": True}


# get url filters list
@routes.get("/filters")
async def get_filters(
    start: int,
    limit: int,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    db: Session = Depends(get_db),
):
    if start < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid parameters",
        )
    filters = db.query(URLFilter).order_by(URLFilter.created_at.desc()).offset(start).limit(limit).all()
    return filters


# create new filter
@routes.post("/filters")
async def create_filter(
    item: Filter,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    db: Session = Depends(get_db),
):
    url_filter = URLFilter(filter=item.url_filter)
    db.add(url_filter)
    db.commit()
    return {"success": True}


# delete url filter
@routes.delete("/filters")
async def delete_filter(
    id: str,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    db: Session = Depends(get_db),
):
    try:
        uuid.UUID(id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID",
        )
    url_filter = db.query(URLFilter).filter(URLFilter.id == id).first()
    if url_filter:
        db.delete(url_filter)
        db.commit()
        return {"success": True}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="ID not exist",
    )
