from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Step
from app.schemas import StepCreate, StepRead

router = APIRouter(prefix="/api/steps", tags=["steps"])


@router.post("", response_model=StepRead, status_code=status.HTTP_201_CREATED)
def create_step(step: StepCreate, db: Session = Depends(get_db)):
    db_step = Step(name=step.name, starts_with_left_free=step.starts_with_left_free)
    db.add(db_step)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um passo com esse nome",
        ) from None
    db.refresh(db_step)
    return db_step


@router.get("", response_model=list[StepRead])
def list_steps(db: Session = Depends(get_db)):
    return db.query(Step).order_by(Step.name.asc()).all()
