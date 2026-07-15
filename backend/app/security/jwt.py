from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from pydantic import BaseModel
from app.core.config import get_settings


class TokenPayload(BaseModel):
    sub: str
    role: str
    exp: int


def create_access_token(subject: str, role: str) -> str:
    settings = get_settings()
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_minutes)
    payload = {"sub": subject, "role": role, "exp": expires}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> TokenPayload:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return TokenPayload(**payload)
    except JWTError as exc:
        raise ValueError("Invalid authentication token") from exc
