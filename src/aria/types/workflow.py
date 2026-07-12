from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class InputSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str = "string"
    required: bool = False
    default: Any = None

    @field_validator("type")
    @classmethod
    def valid_type(cls, value: str) -> str:
        if value not in {"string", "number", "boolean", "file"}:
            raise ValueError("type must be one of string, number, boolean, file")
        return value


class Step(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    uses: str
    for_each: Any | None = None
    with_: dict[str, Any] = Field(default_factory=dict, alias="with")


class ProviderSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str
    base_url: str | None = None
    api_key_env: str | None = None
    api_key_file: str | None = None

    @field_validator("type")
    @classmethod
    def valid_type(cls, value: str) -> str:
        if value not in {"openai", "ollama"}:
            raise ValueError("type must be one of openai, ollama")
        return value


class Workflow(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    version: str
    name: str
    inputs: dict[str, InputSpec] = Field(default_factory=dict)
    providers: dict[str, ProviderSpec] = Field(default_factory=dict)
    steps: list[Step]
    outputs: dict[str, Any] = Field(default_factory=dict)

    @field_validator("steps")
    @classmethod
    def has_steps(cls, value: list[Step]) -> list[Step]:
        if not value:
            raise ValueError("steps must not be empty")
        return value

    @model_validator(mode="after")
    def unique_step_ids(self) -> "Workflow":
        ids = [step.id for step in self.steps]
        if len(ids) != len(set(ids)):
            raise ValueError("step IDs must be unique")
        return self
