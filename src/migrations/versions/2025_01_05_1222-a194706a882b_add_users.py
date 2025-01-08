"""add users

Revision ID: a194706a882b
Revises: 282e93ca6c89
Create Date: 2025-01-05 12:22:54.015742

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "a194706a882b"
down_revision: Union[str, None] = "282e93ca6c89"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.create_unique_constraint("uq_email", "users", ["email"])
   op.create_unique_constraint("uq_nickname", "users", ["nickname"])
   


def downgrade() -> None:
   op.drop_constraint("uq_email", "users", type="unique")
   op.drop_constraint("uq_nickname", "users", type="unique")
    