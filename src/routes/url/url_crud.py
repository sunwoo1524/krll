from sqlalchemy.orm import Session

from ...models import URL


def storeKeyOfURL(db: Session, url: str, key: str):
    url = URL(
        key=key,
        original_url=url
    )
    db.add(url)
    db.commit()

    return url


def getOriginalURL(db: Session, key: str):
    url = db.query(URL).filter(URL.key == key).first()
    return url


def getKeyOfURL(db: Session, url: str):
    key = db.query(URL).filter(URL.original_url == url).first()
    return key
