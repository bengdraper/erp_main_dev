"""add chart_of_accounts default

Revision ID: 7fd7e3c6d902
Revises: 09f79f539b7c
Create Date: 2025-05-08 17:56:31.609434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fd7e3c6d902'
down_revision: Union[str, None] = '09f79f539b7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO chart_of_accounts (description)
        VALUES ('default_chart_of_accounts')
        """
        );


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM chart_of_accounts WHERE description='default_chart_of_accounts'
        """
        );
