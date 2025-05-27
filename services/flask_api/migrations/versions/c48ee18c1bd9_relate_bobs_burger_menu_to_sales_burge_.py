"""relate bobs burger menu to burger sales 4101

Revision ID: c48ee18c1bd9
Revises: 8fc8a8f6ab74
Create Date: 2025-05-08 19:47:19.042078

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c48ee18c1bd9'
down_revision: Union[str, None] = '8fc8a8f6ab74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE menus SET sales_account_id = 1 WHERE id = 1;

"""
    );


def downgrade() -> None:
    op.execute(
        """
        UPDATE menus SET sales_account__id = null WHERE id = 1;
"""
    )
