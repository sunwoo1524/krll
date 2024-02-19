from sqlalchemy import Column, String

from .database import Base


class URL(Base):
    __tablename__ = "url"

    key = Column(String, primary_key=True, nullable=False)
    original_url = Column(String, nullable=False)
