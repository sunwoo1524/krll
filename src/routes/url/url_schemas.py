from pydantic import BaseModel


class URLItem(BaseModel):
    url: str
    token: str | None


class ShortenRes(BaseModel):
    key: str
    original_url: str
