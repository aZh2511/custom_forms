from dataclasses import dataclass, field
from uuid import uuid4, UUID


@dataclass(frozen=True)
class FieldUUID:
    value: UUID = field(default_factory=uuid4)


@dataclass(frozen=True)
class FormUUID:
    value: UUID = field(default_factory=uuid4)
