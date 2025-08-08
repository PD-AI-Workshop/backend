"""Insert admin user

Revision ID: 4d17daf47b75
Revises: 71e44bc25879
Create Date: 2025-08-08 14:14:19.961115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d17daf47b75'
down_revision: Union[str, None] = '71e44bc25879'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        INSERT INTO "users" (email, username, hashed_password, role, is_active, is_superuser, is_verified)
        VALUES ('alext0408@yandex.ru', 'Topinambur02','$argon2id$v=19$m=65536,t=3,p=4$voV67kVg+gdH5M183E9X2A$AVpng1Cc9uPHxtCXRjSlu1jVt/xr5byCmtrBlafem+8', 'ADMIN', true, true, true);
    """)
    


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DELETE FROM "users"
        WHERE email = 'alext0408@yandex.ru';
    """)
