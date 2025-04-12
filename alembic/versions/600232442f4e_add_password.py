"""add password

Revision ID: 600232442f4e
Revises: e5220206aefc
Create Date: 2025-04-10 15:17:41.820175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '600232442f4e'
down_revision: Union[str, None] = 'e5220206aefc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
