"""add step end leg

Revision ID: 202605210003
Revises: 202605210002
Create Date: 2026-05-21 00:00:03

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "202605210003"
down_revision: Union[str, None] = "202605210002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("steps") as batch_op:
        batch_op.add_column(sa.Column("ends_with_left_free", sa.Boolean(), nullable=True))

    op.execute(
        sa.text("UPDATE steps SET ends_with_left_free = NOT starts_with_left_free")
    )

    with op.batch_alter_table("steps") as batch_op:
        batch_op.alter_column("ends_with_left_free", nullable=False)


def downgrade() -> None:
    with op.batch_alter_table("steps") as batch_op:
        batch_op.drop_column("ends_with_left_free")
