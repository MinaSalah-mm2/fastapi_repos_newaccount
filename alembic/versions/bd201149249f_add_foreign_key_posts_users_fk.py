"""add foreign key posts_users_fk

Revision ID: bd201149249f
Revises: 4e078a026c50
Create Date: 2023-12-02 17:36:50.377843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd201149249f'
down_revision: Union[str, None] = '4e078a026c50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# user_id = Column(Integer, ForeignKey(
#         'users.id', ondelete='CASCADE'), nullable=False)


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(constraint_name='posts_users_fk', source_table='posts', referent_table='users',
                          local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column(table_name='posts',column_name='user_id')
    pass
