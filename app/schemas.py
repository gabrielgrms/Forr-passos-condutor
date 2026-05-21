from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StepBase(BaseModel):
    name: str
    starts_with_left_free: bool | None = None
    ends_with_left_free: bool | None = None
    is_composite: bool = False
    component_step_ids: list[int] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Nome do passo não pode ser vazio")
        return cleaned


class StepCreate(StepBase):
    @model_validator(mode="after")
    def validate_step_kind(self):
        if self.is_composite:
            if len(self.component_step_ids) < 2:
                raise ValueError("Passo composto deve ter pelo menos 2 componentes")
            if len(set(self.component_step_ids)) != len(self.component_step_ids):
                raise ValueError("Passo composto não pode repetir componentes")
        else:
            if self.starts_with_left_free is None:
                raise ValueError(
                    "Passo simples precisa informar se começa com a esquerda livre"
                )
            if self.ends_with_left_free is None:
                raise ValueError(
                    "Passo simples precisa informar se termina com a esquerda livre"
                )
            if self.component_step_ids:
                raise ValueError("Passo simples não pode ter componentes")
        return self


class StepComponentRead(BaseModel):
    step_id: int
    name: str
    starts_with_left_free: bool
    ends_with_left_free: bool
    position: int


class StepRead(BaseModel):
    id: int
    name: str
    starts_with_left_free: bool
    ends_with_left_free: bool
    is_composite: bool
    components: list[StepComponentRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class SequencePair(BaseModel):
    first: StepRead
    second: StepRead


class RandomizationResponse(BaseModel):
    pairs: list[SequencePair]
    leftovers: list[StepRead]
