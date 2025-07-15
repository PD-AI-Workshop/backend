from settings import settings
from fastapi_users.authentication import JWTStrategy


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600)
