"""remove the extra column isPrivate column from posts table 

Revision ID: ca6eabacb80e
Revises: bd201149249f
Create Date: 2023-12-02 20:17:47.715218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca6eabacb80e'
down_revision: Union[str, None] = 'bd201149249f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


#  TODO note : never ever with alembic revision implement the upgrade without the downgrade . 


def upgrade() -> None:
    # op.drop_column(table_name='posts', column_name='isPrivate')
    pass


def downgrade() -> None:
    # op.add_column(
    #     table_name='posts',
    #     column=sa.Column('isPrivate', sa.Boolean())
    # )
    pass
