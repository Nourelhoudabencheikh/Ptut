"""create table montres

Revision ID: a6886493b10d
Revises: 0255c1b0f2d4
Create Date: 2024-03-22 10:11:39.168069

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6886493b10d'
down_revision = '0255c1b0f2d4'
branch_labels = None
depends_on = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def upgrade_() -> None:
    op.create_table('montres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('montre', sa.String(length=64), nullable=False),
    sa.Column('debut', sa.DateTime, nullable=False),
    sa.Column('fin', sa.DateTime, nullable=False),
    sa.Column('etat', sa.String(length=10), nullable=False),
    sa.Column('marque', sa.String(length=100), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade_() -> None:
    op.drop_table('montres')
