""" create a phone number col on users table

Revision ID: 545de6788d0f
Revises: 220c149a0a4c
Create Date: 2024-05-24 15:26:12.668009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '545de6788d0f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String, nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
