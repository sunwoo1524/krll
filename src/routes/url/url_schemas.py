from pydantic import BaseModel


class URL(BaseModel):
    url: str


class ShortenURLRes(BaseModel):
    key: str
    original_url: str
