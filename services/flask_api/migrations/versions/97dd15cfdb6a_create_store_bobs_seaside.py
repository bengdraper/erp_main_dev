"""create store bobs_seaside

Revision ID: 97dd15cfdb6a
Revises: 7fd7e3c6d902
Create Date: 2025-05-08 18:25:50.532040

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97dd15cfdb6a'
down_revision: Union[str, None] = '7fd7e3c6d902'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO stores (name, company_id, chart_of_accounts_id)
        VALUES ('Bobs Seaside', 1, 1)
        """
    );


def downgrade() -> None:
    op.execute(
    """
        # DELETE FROM stores WHERE name='Bob's Seaside';
    """
    );
