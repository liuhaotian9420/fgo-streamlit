"""Add atk to looper

Revision ID: fe3890ca251c
Revises: c300e962b967
Create Date: 2024-09-19 16:42:20.887361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe3890ca251c'
down_revision: Union[str, None] = 'c300e962b967'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('loopers', sa.Column('atk', sa.Integer(), nullable=False, comment='最大攻击力'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('loopers', 'atk')
    # ### end Alembic commands ###
