#
# as we say before, alembic is very similiar to handling the database, with versions.
# assume this is the first version, like for createing the Posts table, as a step/version
# with alembic.

# TODO question => is create the tables with columns using alembic replac the use of sqlAlchemy ?


"""create posts table

Revision ID: 8fac5c965277
Revises: 
Create Date: 2023-12-02 10:15:25.651915

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fac5c965277'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('content', sa.String, nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
