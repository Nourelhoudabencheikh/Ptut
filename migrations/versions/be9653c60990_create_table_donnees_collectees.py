"""create table donnees Collectees

Revision ID: be9653c60990
Revises: be4c16c4897c
Create Date: 2024-03-22 10:11:40.830469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be9653c60990'
down_revision= 'be4c16c4897c'
branch_labels = None
depends_on = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def upgrade_() -> None:
    op.create_table('donnee_collectees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dateTime', sa.DateTime, nullable=False),
    sa.Column('accX', sa.Float(), nullable=False),
    sa.Column('accY', sa.Float(), nullable=False),
    sa.Column('accZ', sa.Float(), nullable=False),
    sa.Column('gyrX', sa.Float(), nullable=False),
    sa.Column('gyrY', sa.Float(), nullable=False),
    sa.Column('gyrZ', sa.Float(), nullable=False),
    sa.Column('bpm', sa.Float(), nullable=False),
    sa.Column('montre_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['montre_id'], ['montres.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade_() -> None:
    op.drop_table('donnee_collectees')