"""create users table

Revision ID: 1c9530f7df33
Revises: 57ca5c86170f
Create Date: 2024-12-13 17:55:14.377360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c9530f7df33'
down_revision: Union[str, None] = '57ca5c86170f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
