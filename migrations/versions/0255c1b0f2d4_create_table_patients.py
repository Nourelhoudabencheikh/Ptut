"""create table patients

Revision ID: 0255c1b0f2d4
Revises: 9fe082cb8ce3
Create Date: 2024-03-22 10:11:38.467609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0255c1b0f2d4'
down_revision= '9fe082cb8ce3'
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
    sa.Column('classe', sa.String(length=64), nullable=False),
    sa.Column('poids', sa.Float(), nullable=False),
    sa.Column('taille', sa.Float(), nullable=False),

    sa.PrimaryKeyConstraint('id')
    
    )


def downgrade_() -> None:
    op.drop_table('patients')