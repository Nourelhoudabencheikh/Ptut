"""create table resultat journalier 

Revision ID: 93c5c02e2864
Revises: be9653c60990
Create Date: 2024-03-22 10:11:41.463471

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision='93c5c02e2864'
down_revision = 'be9653c60990'
branch_labels = None
depends_on = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def upgrade_() -> None:
    op.create_table('resultat journalier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nbAlerte', sa.Integer(), nullable=False),
    sa.Column('intensiteSed', sa.Float(), nullable=False),
    sa.Column('intensiteLeg', sa.Float(), nullable=False),
    sa.Column('intesiteMod', sa.Float(), nullable=False),
    sa.Column('intensiteVig', sa.Float(), nullable=False),
    sa.Column('dureeHorsLigne', sa.Float(), nullable=False),
    sa.Column('dureePort', sa.Float(), nullable=False),
    sa.Column('date', sa.DateTime, nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),  
    sa.PrimaryKeyConstraint('id')
    
    )


def downgrade_() -> None:
    op.drop_table('resultat journalier')
