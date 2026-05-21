from pydantic import BaseModel, ConfigDict, field_validator


class StepBase(BaseModel):
    name: str
    starts_with_left_free: bool

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Nome do passo não pode ser vazio")
        return cleaned


class StepCreate(StepBase):
    pass


class StepRead(StepBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SequencePair(BaseModel):
    first: StepRead
    second: StepRead


class RandomizationResponse(BaseModel):
    pairs: list[SequencePair]
    leftovers: list[StepRead]
