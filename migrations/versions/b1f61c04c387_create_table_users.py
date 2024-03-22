"""create table users

Revision ID: b1f61c04c387
Revises: 
Create Date: 2024-03-22 10:11:35.913183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1f61c04c387'
down_revision = None
branch_labels = None
depends_on= None

def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def upgrade_() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=64), nullable=False),
    sa.Column('prenom', sa.String(length=64), nullable=False),
    sa.Column('dateNaissance', sa.DateTime, nullable=False),
    sa.Column('etat', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_nom'), 'users', ['nom'], unique=True)


def downgrade_() -> None:
    op.drop_index(op.f('ix_users_nom'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')