from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import Step, StepComponent
from app.schemas import StepComponentRead, StepCreate, StepRead

router = APIRouter(prefix="/api/steps", tags=["steps"])


def _serialize_step(step: Step) -> StepRead:
    components = [
        StepComponentRead(
            step_id=item.component_step.id,
            name=item.component_step.name,
            starts_with_left_free=item.component_step.starts_with_left_free,
            ends_with_left_free=item.component_step.ends_with_left_free,
            position=item.position,
        )
        for item in sorted(step.components, key=lambda component: component.position)
    ]
    return StepRead(
        id=step.id,
        name=step.name,
        starts_with_left_free=step.starts_with_left_free,
        ends_with_left_free=step.ends_with_left_free,
        is_composite=step.is_composite,
        components=components,
    )


@router.post("", response_model=StepRead, status_code=status.HTTP_201_CREATED)
def create_step(step: StepCreate, db: Session = Depends(get_db)):
    starts_with_left_free = step.starts_with_left_free
    ends_with_left_free = step.ends_with_left_free
    component_steps_by_id: dict[int, Step] = {}

    if step.is_composite:
        component_steps = db.query(Step).filter(Step.id.in_(step.component_step_ids)).all()
        component_steps_by_id = {component.id: component for component in component_steps}
        if len(component_steps_by_id) != len(step.component_step_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Todos os componentes devem referenciar passos existentes",
            )
        starts_with_left_free = component_steps_by_id[
            step.component_step_ids[0]
        ].starts_with_left_free
        ends_with_left_free = component_steps_by_id[
            step.component_step_ids[-1]
        ].ends_with_left_free

    db_step = Step(
        name=step.name,
        starts_with_left_free=starts_with_left_free,
        ends_with_left_free=ends_with_left_free,
        is_composite=step.is_composite,
    )
    db.add(db_step)

    try:
        db.flush()
        if step.is_composite:
            if db_step.id in step.component_step_ids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Passo composto não pode referenciar a si mesmo",
                )
            db.add_all(
                [
                    StepComponent(
                        compound_step_id=db_step.id,
                        component_step_id=component_step_id,
                        position=index + 1,
                    )
                    for index, component_step_id in enumerate(step.component_step_ids)
                ]
            )
        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um passo com esse nome",
        ) from None
    db_step = (
        db.query(Step)
        .options(selectinload(Step.components).selectinload(StepComponent.component_step))
        .filter(Step.id == db_step.id)
        .one()
    )
    return _serialize_step(db_step)


@router.get("", response_model=list[StepRead])
def list_steps(db: Session = Depends(get_db)):
    steps = (
        db.query(Step)
        .options(selectinload(Step.components).selectinload(StepComponent.component_step))
        .order_by(Step.name.asc())
        .all()
    )
    return [_serialize_step(step) for step in steps]
