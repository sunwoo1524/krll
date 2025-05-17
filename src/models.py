from sqlalchemy import Column, String, DateTime, UUID
import datetime, uuid

from .database import Base


class URL(Base):
    __tablename__ = "url"

    key = Column(String, primary_key=True, nullable=False)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc))


class URLFilter(Base):
    __tablename__ = "url_filters"

    id = Column(UUID, nullable=False, default=uuid.uuid4, primary_key=True)
    filter = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc))


class Admin(Base):
    __tablename__ = "admins"

    id = Column(UUID, nullable=False, default=uuid.uuid4, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc))
