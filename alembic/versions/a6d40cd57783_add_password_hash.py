"""add password_hash

Revision ID: a6d40cd57783
Revises: 600232442f4e
Create Date: 2025-04-10 15:21:30.479696

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6d40cd57783'
down_revision: Union[str, None] = '600232442f4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
