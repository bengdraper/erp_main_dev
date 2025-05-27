"""create company

Revision ID: 49d5327fb5d1
Revises: 
Create Date: 2025-05-08 16:21:36.363662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49d5327fb5d1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO companies (name)
        VALUES ('Bobs Burgers default')
        ;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM companies
        WHERE name='Bobs Burgers default'
"""
    )
