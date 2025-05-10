from sqlalchemy import Column, String, DateTime
import datetime

from .database import Base


class URL(Base):
    __tablename__ = "url"

    key = Column(String, primary_key=True, nullable=False)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now(datetime.timezone.utc))
