from db.session import async_session_maker
from pwdlib import PasswordHash
from model.user import User
from sqlalchemy import insert, select
from settings import settings


async def create_admin():
    async with async_session_maker() as session:
        select_query = select(User).where(User.email == settings.ADMIN_EMAIL)
        existing_admin = await session.execute(select_query)

        if existing_admin.scalar_one_or_none():
            return None

        email = settings.ADMIN_EMAIL
        username = settings.ADMIN_USERNAME
        password = settings.ADMIN_PASSWORD
        hashed_password = PasswordHash.recommended().hash(password)
        role = "ADMIN"
        is_active = True
        is_superuser = True
        is_verified = True

        admin_user = {
            "email": email,
            "username": username,
            "hashed_password": hashed_password,
            "role": role,
            "is_active": is_active,
            "is_superuser": is_superuser,
            "is_verified": is_verified,
        }

        insert_query = insert(User).values(**admin_user).returning(User)
        result = await session.execute(insert_query)
        await session.commit()
        return result.scalar_one_or_none()
