"""add hotels

Revision ID: 282e93ca6c89
Revises: 0d4f88350b24
Create Date: 2025-01-05 12:22:00.087388

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "282e93ca6c89"
down_revision: Union[str, None] = "0d4f88350b24"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
   
