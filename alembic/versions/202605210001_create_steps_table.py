"""create steps table

Revision ID: 202605210001
Revises:
Create Date: 2026-05-21 00:00:01

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "202605210001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "steps",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("starts_with_left_free", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_steps_id"), "steps", ["id"], unique=False)
    op.create_index(op.f("ix_steps_name"), "steps", ["name"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_steps_name"), table_name="steps")
    op.drop_index(op.f("ix_steps_id"), table_name="steps")
    op.drop_table("steps")
