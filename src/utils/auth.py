import bcrypt
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from ..env import JWT_SECRET_KEY

SESSION_COOKIE_NAME = "admin_session"
SESSION_MAX_AGE = 60 * 60 * 24 * 30  # 30 days in seconds
SESSION_RENEW_BEFORE = SESSION_MAX_AGE // 2  # renew when less than 15 days remain

_serializer = URLSafeTimedSerializer(JWT_SECRET_KEY, salt="admin-session")


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        bytes(plain_password, encoding="utf-8"),
        bytes(hashed_password, encoding="utf-8"),
    )


def get_password_hash(password):
    return bcrypt.hashpw(
        bytes(password, encoding="utf-8"),
        bcrypt.gensalt(),
    )


def create_session_token(admin_id: str) -> str:
    """Sign admin_id into a tamper-proof session token."""
    return _serializer.dumps(admin_id)


def verify_session_token(token: str) -> tuple[str, int] | None:
    """Return (admin_id, issued_at) if the token is valid and not expired, else None.

    issued_at is a Unix timestamp (seconds) indicating when the token was created.
    """
    try:
        # return_timestamp=True makes loads() return (payload, datetime) pair
        admin_id, issued_dt = _serializer.loads(
            token, max_age=SESSION_MAX_AGE, return_timestamp=True
        )
        return admin_id, int(issued_dt.timestamp())
    except (BadSignature, SignatureExpired):
        return None
