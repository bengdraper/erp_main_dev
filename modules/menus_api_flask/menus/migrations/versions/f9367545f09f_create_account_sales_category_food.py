"""create account sales category food

Revision ID: f9367545f09f
Revises: f0a7e4c8835a
Create Date: 2025-05-08 19:20:36.286706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9367545f09f'
down_revision: Union[str, None] = 'f0a7e4c8835a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# food sales 4100


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO sales_account_categories (description, account_number)
        VALUES ('Food Sales', 4100)
"""
    );



def downgrade() -> None:
    op.execute(
        """
        DELETE FROM sales_account_categories WHERE account_number=4100
"""
    );
