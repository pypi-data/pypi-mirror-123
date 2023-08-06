from __future__ import annotations

import uuid
from typing import Union, Tuple, Optional

import pydantic
from classiq_interface.generator.custom_register_properties import (
    CustomRegisterProperties,
)


class CustomRegister(pydantic.BaseModel):
    """
    A user-defined custom quantum register.
    """

    class Config:
        # Validate field defaults.
        validate_all = True

    name: Optional[str] = pydantic.Field(
        default=None,
        description="The name of the custom register",
    )

    qubits: Tuple[pydantic.NonNegativeInt, ...] = pydantic.Field(
        description="A tuple of qubits as integers as indexed within a custom function code",
    )

    @property
    def width(self) -> pydantic.PositiveInt:
        """The number of qubits of the custom register"""
        return len(self.qubits)

    def is_compatible(
        self, register: Union[CustomRegisterProperties, CustomRegister]
    ) -> bool:
        if isinstance(register, CustomRegister):
            return register == self
        return register.name == self.name and register.width == self.width

    @pydantic.validator("name")
    def validate_name(cls, name: str):
        if name is None:
            return str(uuid.uuid4())
        return name

    @pydantic.validator("qubits")
    def validate_qubits(cls, qubits: Tuple[pydantic.NonNegativeInt, ...]):
        if len(qubits) == 0:
            raise ValueError(f"qubits field must be non-empty.")
        if len(set(qubits)) != len(qubits):
            raise ValueError(f"All qubits of a register must be distinct.")
        return qubits
