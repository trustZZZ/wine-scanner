"""remove_tenant_id_from_all_tables

Revision ID: 51ec442bc2ad
Revises: 97ac99ad6b61
Create Date: 2026-09-09 06:59:44.710915

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51ec442bc2ad'
down_revision: Union[str, None] = '97ac99ad6b61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
