from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from urllib.parse import urlparse
import random, string, requests

from ...database import get_db
from .url_schemas import URL, ShortenURLRes
from .url_crud import storeKeyOfURL, getOriginalURL, getKeyOfURL
from ...env import HOST, NTFY


routes = APIRouter(
    tags=["url"]
)


@routes.post("/api/urls")
def shortenURL(url: URL, db: Session = Depends(get_db)) -> ShortenURLRes:
    # check the URL is valid
    try:
        result = urlparse(url.url)
        if not all([result.scheme, result.netloc]):
            raise HTTPException(status_code=400, detail="INVALID_URL")
    except ValueError:
        raise HTTPException(status_code=400, detail="INVALID_URL")

    # get the URL of key from database
    # if it is not found, generate a new key
    # short url: https://host/key
    db_key = getKeyOfURL(db, url=url.url)
    key = None
    if db_key is None:
        letters = string.ascii_letters
        letters += "".join(str(i) for i in range(1, 10))
        key = "".join(random.choice(letters) for i in range(6))
        storeKeyOfURL(db, url.url, key)

        # send notification to ntfy
        requests.post(NTFY, data=f"New short URL was created.\nWebsite: {result.netloc}".encode(encoding='utf-8'))
    else:
        key = db_key.key

    res = ShortenURLRes(
        key=key,
        original_url=url.url
    )
    return res


@routes.get("/{key}")
def redirect(key: str, db: Session = Depends(get_db)):
    # redirect to original URL if the key is exist
    original_url = getOriginalURL(db, key)
    if original_url is None:
        return HTTPException(status_code=404, detail="URL_NOT_FOUND")
    return RedirectResponse(original_url.original_url, status_code=301)
