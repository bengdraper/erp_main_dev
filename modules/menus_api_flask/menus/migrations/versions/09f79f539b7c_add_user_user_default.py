"""add user user_default

Revision ID: 09f79f539b7c
Revises: 49d5327fb5d1
Create Date: 2025-05-08 16:37:37.798761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09f79f539b7c'
down_revision: Union[str, None] = '49d5327fb5d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute(
        """
        INSERT INTO users (email, password, permissions, name, company_id)
        VALUES ('user@bobs_burgers.com', 'great_password', '0', 'Burger Bob', '1')

"""
    );


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM users
        WHERE email='user@bobs_burgers.com'
"""
    );
