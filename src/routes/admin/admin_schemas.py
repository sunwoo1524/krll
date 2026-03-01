from pydantic import BaseModel


class Admin(BaseModel):
    username: str



class AdminForSignUp(Admin):
    password: str


class Filter(BaseModel):
    url_filter: str
