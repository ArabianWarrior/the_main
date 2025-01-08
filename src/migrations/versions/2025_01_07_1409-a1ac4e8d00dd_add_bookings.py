"""add bookings

Revision ID: a1ac4e8d00dd
Revises: 334c76fcfc9d
Create Date: 2025-01-07 14:09:37.539000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "a1ac4e8d00dd"
down_revision: Union[str, None] = "334c76fcfc9d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("data_from", sa.Date(), nullable=False),
        sa.Column("data_to", sa.Date(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("bookings")
    
