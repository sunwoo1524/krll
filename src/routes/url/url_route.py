from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from urllib.parse import urlparse
import random, string, requests

from ...database import get_db
from .url_schemas import URLItem, ShortenRes
from .url_crud import storeKeyOfURL, getOriginalURL, getKeyOfURL, filter_url
from ...env import HOST, NTFY, secret_key, CAPTCHA_MODE, site_key, cap_instance


routes = APIRouter(
    tags=["url"]
)


@routes.post("/api/urls")
def shortenURL(item: URLItem, request: Request, db: Session = Depends(get_db)) -> ShortenRes:
    # check captcha
    if CAPTCHA_MODE:
        try:
            captcha_res = requests.post(
                "https://challenges.cloudflare.com/turnstile/v0/siteverify" if CAPTCHA_MODE == "turnstile" else f"{cap_instance}/{site_key}/siteverify",
                {
                    "secret": secret_key,
                    "response": item.token,
                    "remoteip": request.client.host if CAPTCHA_MODE == "turnstile" else None
                }
            )
            captcha_outcome = captcha_res.json()
            if not captcha_outcome["success"]:
                raise HTTPException(status_code=400, detail="FAILURE_CAPTCHA")
        except:
            raise HTTPException(status_code=400, detail="FAILURE_CAPTCHA")
    # elif CAPTCHA_MODE == "cap":
    #     try:
    #         captcha_res = requests.post(
    #             f"{CAP_INSTANCE}/{SITE_KEY}/siteverify",
    #             {
    #                 "secret": SECRET_KEY,
    #                 "response": item.token
    #             }
    #         )
    #         captcha_outcome = captcha_res.json()
    #         if not captcha_outcome["success"]:
    #             raise HTTPException(status_code=400, detail="FAILURE_CAPTCHA")
    #     except:
    #         raise HTTPException(status_code=400, detail="FAILURE_CAPTCHA")

    # check the URL is valid
    try:
        result = urlparse(item.url)
        if not all([result.scheme, result.netloc]):
            raise HTTPException(status_code=400, detail="INVALID_URL")
    except ValueError:
        raise HTTPException(status_code=400, detail="INVALID_URL")
    
    # check length of url
    if len(item.url) > 10000:
        raise HTTPException(status_code=400, detail="URL_MAX_LENGTH_EXCEEDED")

    # check if url matches filter
    filter_result = filter_url(db, item.url)
    if len(filter_result) > 0:
        raise HTTPException(status_code=400, detail="BLOCKED_URL")

    # get the URL of key from database
    # if it is not found, generate a new key
    # short url: https://host/key
    db_key = getKeyOfURL(db, url=item.url)
    key = None
    if db_key is None:
        letters = string.ascii_letters
        letters += "".join(str(i) for i in range(1, 10))
        key = "".join(random.choice(letters) for i in range(6))
        storeKeyOfURL(db, item.url, key)

        # send notification to ntfy
        if not NTFY is None: requests.post(NTFY, data=f"New short URL was created.\nWebsite: {result.netloc}".encode(encoding='utf-8'))
    else:
        key = db_key.key

    res = ShortenRes(
        key=key,
        original_url=item.url
    )
    return res


@routes.get("/{key}")
def redirect(key: str, db: Session = Depends(get_db)):
    # redirect to original URL if the key is exist
    original_url = getOriginalURL(db, key)
    if original_url is None:
        return HTTPException(status_code=404, detail="URL_NOT_FOUND")
    return RedirectResponse(original_url.original_url, status_code=301)
