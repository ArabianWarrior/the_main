"""initial migration 

Revision ID: a6910c9744cd
Revises: b1a5450b131f
Create Date: 2024-12-15 15:27:14.290142

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a6910c9744cd"
down_revision: Union[str, None] = "b1a5450b131f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    pass
   

def downgrade() -> None:
   
    pass
  
