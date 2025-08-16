from fastapi import Depends, Request
from config.log_config import logger
from model.user import User, get_user_db
from fastapi_users import BaseUserManager, IntegerIDMixin


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def on_after_register(self, user: User, request: Request):
        logger.info(f"User {user.id} has registered.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
