"""add wine_card and wine_id to scans

Revision ID: 97ac99ad6b61
Revises: 81dc0ac95a2e
Create Date: 2026-09-08 22:09:43.212494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97ac99ad6b61'
down_revision: Union[str, None] = '81dc0ac95a2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
