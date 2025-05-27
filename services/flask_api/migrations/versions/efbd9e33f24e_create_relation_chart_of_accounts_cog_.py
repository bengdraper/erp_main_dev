"""create relation chart of accounts cog account cat

Revision ID: efbd9e33f24e
Revises: adfe00c52139
Create Date: 2025-05-08 20:25:08.927563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'efbd9e33f24e'
down_revision: Union[str, None] = 'adfe00c52139'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO chart_of_accounts_cog_account_categories
        (chart_of_accounts_id, cog_account_categories_id)
        VALUES (1,1)
        """
    );


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM chart_of_accounts_cog_account_categories
        WHERE chart_of_accounts_id = 1 and cog_account_categories_id = 1
        """
    )
