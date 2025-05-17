from sqlalchemy.orm import Session
import uuid

from .admin_schemas import Admin, AdminInDB
from ...models import URL, Admin, URLFilter
from ...utils.auth import get_password_hash


def get_admin(db: Session, username: str):
    admin = db.query(Admin).filter(Admin.username == username).first()
    if admin: admin.id = str(admin.id)
    return admin


def get_admin_with_id(db: Session, id: str):
    admin = db.query(Admin).filter(Admin.id == uuid.UUID(id)).first()
    if admin: admin.id = str(admin.id)
    return admin


def create_admin_in_db(db: Session, username: str, password: str):
    admin = Admin(
        username = username,
        password = get_password_hash(password).decode("utf-8")
    )
    db.add(admin)
    db.commit()
    return admin


def get_url_list(db: Session, start: int, limit: int):
    urls = db.query(URL).order_by(URL.created_at.desc()).offset(start).limit(limit).all()
    return urls


def delete_url_db(db: Session, key: str):
    url = db.query(URL).where(key == URL.key).first()
    if url:
        db.delete(url)
        db.commit()
        return True
    return None
