"""create bob's burger menu

Revision ID: f0a7e4c8835a
Revises: df22f6add2a2
Create Date: 2025-05-08 18:37:57.070925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0a7e4c8835a'
down_revision: Union[str, None] = 'df22f6add2a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO menus (name, description)
        VALUES ('BURGERS', 'All Bobs best burgers breakfast lunch and dinner')
"""
    );


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM menus WHERE name='BURGERS'
"""
    );
