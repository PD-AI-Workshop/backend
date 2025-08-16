from auth.transport import bearer_transport
from auth.strategy import get_jwt_strategy
from fastapi_users.authentication import AuthenticationBackend

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
