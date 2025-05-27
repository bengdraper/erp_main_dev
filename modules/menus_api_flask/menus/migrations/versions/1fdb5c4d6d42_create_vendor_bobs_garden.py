"""create vendor bobs garden

Revision ID: 1fdb5c4d6d42
Revises: efbd9e33f24e
Create Date: 2025-05-08 20:33:07.461693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fdb5c4d6d42'
down_revision: Union[str, None] = 'efbd9e33f24e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO vendors (name) VALUES ('Bobs Garden')
"""
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM vendors WHERE name = 'Bobs Garden'
"""
    )
