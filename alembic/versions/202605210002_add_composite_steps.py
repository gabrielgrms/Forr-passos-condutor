"""add composite steps support

Revision ID: 202605210002
Revises: 202605210001
Create Date: 2026-05-21 00:00:02

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "202605210002"
down_revision: Union[str, None] = "202605210001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "steps",
        sa.Column("is_composite", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    if op.get_bind().dialect.name != "sqlite":
        op.alter_column("steps", "is_composite", server_default=None)

    op.create_table(
        "step_components",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("compound_step_id", sa.Integer(), nullable=False),
        sa.Column("component_step_id", sa.Integer(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.CheckConstraint("position > 0", name="ck_step_components_position_positive"),
        sa.ForeignKeyConstraint(
            ["component_step_id"],
            ["steps.id"],
            name="fk_step_components_component_step_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["compound_step_id"],
            ["steps.id"],
            name="fk_step_components_compound_step_id",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("compound_step_id", "position", name="uq_step_components_position"),
    )
    op.create_index(
        op.f("ix_step_components_compound_step_id"),
        "step_components",
        ["compound_step_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_step_components_component_step_id"),
        "step_components",
        ["component_step_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_step_components_component_step_id"), table_name="step_components")
    op.drop_index(op.f("ix_step_components_compound_step_id"), table_name="step_components")
    op.drop_table("step_components")
    op.drop_column("steps", "is_composite")
