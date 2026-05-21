from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Step
from app.schemas import RandomizationResponse, StepRead
from app.services.randomization import generate_sequences

router = APIRouter(prefix="/api/randomize", tags=["randomization"])


@router.post("", response_model=RandomizationResponse)
def randomize_steps(db: Session = Depends(get_db)):
    db_steps = db.query(Step).all()
    step_reads = [StepRead.model_validate(step) for step in db_steps]
    return generate_sequences(step_reads)
