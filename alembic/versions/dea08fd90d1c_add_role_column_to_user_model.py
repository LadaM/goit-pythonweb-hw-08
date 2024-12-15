"""Add role column to User model

Revision ID: dea08fd90d1c
Revises: e39a0497c7be
Create Date: 2024-12-15 17:50:32.326852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision: str = 'dea08fd90d1c'
down_revision: Union[str, None] = 'e39a0497c7be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define the enum type
user_role_enum = ENUM('USER', 'ADMIN', name='userrole', create_type=True)

def upgrade():
    # Create the ENUM type
    user_role_enum.create(op.get_bind(), checkfirst=True)

    # Add the role column with the ENUM type
    op.add_column('users', sa.Column('role', user_role_enum, nullable=False, server_default='USER'))

def downgrade():
    # Drop the role column
    op.drop_column('users', 'role')

    # Drop the ENUM type
    user_role_enum.drop(op.get_bind(), checkfirst=True)
