"""Update resource fields

Revision ID: 4a96a9dda632
Revises: bc19335e7b42
Create Date: 2024-06-02 22:26:07.959659

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4a96a9dda632"
down_revision: Union[str, None] = "bc19335e7b42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
