"""user_id changed to id

Revision ID: 37acee8ce549
Revises: a5bdaea09c52
Create Date: 2025-02-23 17:42:05.702326

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37acee8ce549'
down_revision: Union[str, None] = 'a5bdaea09c52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('id', sa.UUID(), nullable=False))
    op.drop_index('ix_users_user_id', table_name='users')
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    op.drop_column('users', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.create_index('ix_users_user_id', 'users', ['user_id'], unique=True)
    op.drop_column('users', 'id')
    # ### end Alembic commands ###
