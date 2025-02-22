"""UUID4 id format was aplied

Revision ID: a5bdaea09c52
Revises: f636f1bef07f
Create Date: 2025-02-22 14:37:47.429986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5bdaea09c52'
down_revision: Union[str, None] = 'f636f1bef07f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_id', sa.UUID(), nullable=False))
    op.drop_index('ix_users_id', table_name='users')
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=True)
    op.drop_column('users', 'id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.drop_column('users', 'user_id')
    # ### end Alembic commands ###
