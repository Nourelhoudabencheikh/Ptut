"""add last seen to user table

Revision ID: 0f2ddfa2608f
Revises: 107dd48f78e8
Create Date: 2024-03-06 17:29:29.776209

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f2ddfa2608f'
down_revision = '107dd48f78e8'
branch_labels = None
depends_on = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def upgrade_() -> None:
    op.add_column('users', sa.Column('first_seen', sa.DateTime, nullable=True))
    op.add_column('users', sa.Column('last_seen', sa.DateTime, nullable=True))


def downgrade_() -> None:
    op.drop_column('users', 'first_seen')
    op.drop_column('users', 'last_seen')
