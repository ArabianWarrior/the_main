"""add users

Revision ID: deccbeb3652d
Revises: a6910c9744cd
Create Date: 2024-12-26 12:45:42.609904

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "deccbeb3652d"
down_revision: Union[str, None] = "a6910c9744cd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("nickname", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # Добавление уникальных ограничений для email и для nickname, чтобы они не повторялись
    op.create_unique_constraint("uq_email", "users", ["email"])
    op.create_unique_constraint("uq_nickname", "users", ["nickname"])


def downgrade() -> None:
    op.drop_table("users")
    #Удаляем уникальные ограничения для email и nickname
    op.drop_constraint("uq_email", "users", type="unique")
    op.drop_constraint("uq_nickname", "user", type="unique")