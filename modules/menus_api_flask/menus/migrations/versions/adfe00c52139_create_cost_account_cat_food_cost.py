"""create cost account cat food cost

Revision ID: adfe00c52139
Revises: c48ee18c1bd9
Create Date: 2025-05-08 20:19:42.059907

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adfe00c52139'
down_revision: Union[str, None] = 'c48ee18c1bd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO cog_account_categories (description, account_number)
        VALUES ('Food Cost', 5100)
"""
    );


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM cog_account_categories WHERE account_number = 5100
"""
    );
