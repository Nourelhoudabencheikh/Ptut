"""create table capteurs

Revision ID: be4c16c4897c
Revises: a6886493b10d
Create Date: 2024-03-22 10:11:39.927040

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be4c16c4897c'
down_revision = 'a6886493b10d'
branch_labels = None
depends_on = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def upgrade_() -> None:
    op.create_table('capteurs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('typeCapteur', sa.String(length=64), nullable=False),
    sa.Column('freqEchantillon', sa.Integer(), nullable=False),
    sa.Column('montre_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['montre_id'], ['montres.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade_() -> None:
    op.drop_table('capteurs')