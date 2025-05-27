"""create relation burger_bob bobs_seaside


Revision ID: df22f6add2a2
Revises: 97dd15cfdb6a
Create Date: 2025-05-08 18:31:15.656508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df22f6add2a2'
down_revision: Union[str, None] = '97dd15cfdb6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO users_stores (user_id, store_id)
        VALUES (1,1)
"""
    );


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM users_stores
        WHERE user_id=1 and store_id=1
"""
    );
