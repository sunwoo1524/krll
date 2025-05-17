from pydantic import BaseModel


class Admin(BaseModel):
    username: str


class AdminInDB(Admin):
    id: str
    password: str


class AdminForSignUp(Admin):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None = None


class Filter(BaseModel):
    url_filter: str
