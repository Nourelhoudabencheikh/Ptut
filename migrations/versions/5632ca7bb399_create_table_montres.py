"""create table montres

Revision ID: 5632ca7bb399
Revises: 67b689fa4fe7
Create Date: 2024-03-20 13:35:07.574446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5632ca7bb399'
down_revision= '67b689fa4fe7'
branch_labels = None
depends_on = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def upgrade_() -> None:
    op.create_table('montres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('etat', sa.String(length=64), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade_() -> None:
    op.drop_table('montres')
