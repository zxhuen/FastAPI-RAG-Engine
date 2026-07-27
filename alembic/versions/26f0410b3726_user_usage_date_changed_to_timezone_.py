"""user usage date changed to timezone aware

Revision ID: 26f0410b3726
Revises: 6757fd53b569
Create Date: 2026-07-27 14:48:06.854657

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "26f0410b3726"
down_revision: Union[str, Sequence[str], None] = "6757fd53b569"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "user_usage",
        "last_reset_at",
        existing_type=sa.DateTime(),
        type_=sa.DateTime(timezone=True),
    )
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "user_usage",
        "last_reset_at",
        existing_type=sa.DateTime(timezone=True),
        type_=sa.DateTime(),
    )
    pass
    # ### end Alembic commands ###
