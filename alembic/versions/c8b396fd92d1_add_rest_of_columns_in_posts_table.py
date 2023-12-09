"""add rest of columns in posts table 

Revision ID: c8b396fd92d1
Revises: 8fac5c965277
Create Date: 2023-12-02 16:25:03.028067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8b396fd92d1'
down_revision: Union[str, None] = '8fac5c965277'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('isPrivate', sa.Boolean,
                  nullable=False, server_default='False'))

    op.add_column("posts", sa.Column('published', sa.Boolean,
                  server_default='True', nullable=False),)

    op.add_column("posts", sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()')))

    pass


def downgrade() -> None:
    op.drop_column('posts', 'isPrivate')
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
