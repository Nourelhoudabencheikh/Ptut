"""create table patient

Revision ID: 67b689fa4fe7
Revises: 8b2122f28c47
Create Date: 2024-03-06 17:29:42.621915

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67b689fa4fe7'
down_revision = '8b2122f28c47'
branch_labels = None
depends_on = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def upgrade_() -> None:
    op.create_table('patients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=64), nullable=False),
    sa.Column('prenom', sa.String(length=120), nullable=False),
    sa.Column('dateNaissance', sa.DateTime, nullable=False),
    sa.Column('etat', sa.String(length=120), nullable=False),
    sa.Column('statistiques', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    
    )


def downgrade_() -> None:
    op.drop_table('patients')