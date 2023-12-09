"""create user table 

Revision ID: 4e078a026c50
Revises: c8b396fd92d1
Create Date: 2023-12-02 16:56:29.476395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e078a026c50'
down_revision: Union[str, None] = 'c8b396fd92d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('email', sa.String(), unique=True, nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()'))
        #  possiable to add such constraint as a functions instead of add theme from the table. 
        # sa.primaryKeyConstraint('id'),
        # sa.UniqueConstraint('email')
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
