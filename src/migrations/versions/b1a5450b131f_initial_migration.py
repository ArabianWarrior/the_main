"""initial migration

Revision ID: b1a5450b131f
Revises: c685f1e17239
Create Date: 2024-12-15 12:02:31.848824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = 'b1a5450b131f'
down_revision: Union[str, None] = 'c685f1e17239'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hotel_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('rooms')

