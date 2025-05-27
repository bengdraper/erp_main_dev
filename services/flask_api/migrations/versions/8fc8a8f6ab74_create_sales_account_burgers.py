"""create sales account burgers

Revision ID: 8fc8a8f6ab74
Revises: f9367545f09f
Create Date: 2025-05-08 19:41:30.124246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fc8a8f6ab74'
down_revision: Union[str, None] = 'f9367545f09f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO sales_accounts (description, account_number)
        VALUES ('Burger Sales', 4101)
"""
    );


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM sales_accounts WHERE account_number = 4101
"""
    );
