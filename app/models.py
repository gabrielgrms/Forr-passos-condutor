from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Step(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    starts_with_left_free = Column(Boolean, nullable=False)
    is_composite = Column(Boolean, nullable=False, default=False)

    components = relationship(
        "StepComponent",
        back_populates="compound_step",
        cascade="all, delete-orphan",
        foreign_keys="StepComponent.compound_step_id",
        order_by="StepComponent.position",
    )


class StepComponent(Base):
    __tablename__ = "step_components"
    __table_args__ = (
        UniqueConstraint("compound_step_id", "position", name="uq_step_components_position"),
        CheckConstraint("position > 0", name="ck_step_components_position_positive"),
    )

    id = Column(Integer, primary_key=True)
    compound_step_id = Column(
        Integer, ForeignKey("steps.id", ondelete="CASCADE"), nullable=False, index=True
    )
    component_step_id = Column(
        Integer, ForeignKey("steps.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    position = Column(Integer, nullable=False)

    compound_step = relationship(
        "Step", foreign_keys=[compound_step_id], back_populates="components"
    )
    component_step = relationship("Step", foreign_keys=[component_step_id])
