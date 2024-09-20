"""update supports

Revision ID: 58e1a9927420
Revises: 8c9fa7164aa4
Create Date: 2024-09-20 14:41:11.098964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58e1a9927420'
down_revision: Union[str, None] = '8c9fa7164aa4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('supports', 'rarity')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('supports', sa.Column('rarity', sa.INTEGER(), nullable=False))
    # ### end Alembic commands ###
