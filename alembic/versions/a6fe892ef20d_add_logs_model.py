"""add logs model

Revision ID: a6fe892ef20d
Revises: 9f004b69d216
Create Date: 2025-04-12 21:03:20.195095

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6fe892ef20d'
down_revision: Union[str, None] = '9f004b69d216'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('action', sa.String(length=120), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('ip', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('log')
    # ### end Alembic commands ###
