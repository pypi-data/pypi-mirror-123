from typing import Union, Tuple

from classiq_interface.generator.custom_register import CustomRegister
from classiq_interface.generator.custom_register_properties import (
    CustomRegisterProperties,
)

CUSTOM_REGISTER_PROPERTIES_TYPE: type = Union[CustomRegister, CustomRegisterProperties]
CUSTOM_REGISTERS_STRICT_TYPE: type = Tuple[CustomRegister, ...]
CUSTOM_REGISTERS_PROPERTIES_STRICT_TYPE: type = Tuple[
    CUSTOM_REGISTER_PROPERTIES_TYPE, ...
]
CUSTOM_REGISTERS_PROPERTIES_TYPE: type = Union[
    Union[CUSTOM_REGISTER_PROPERTIES_TYPE, CUSTOM_REGISTERS_PROPERTIES_STRICT_TYPE]
]
CUSTOM_REGISTERS_TYPE: type = Union[CustomRegister, CUSTOM_REGISTERS_STRICT_TYPE]


def convert_single_register_to_iterable(
    registers: CUSTOM_REGISTERS_PROPERTIES_TYPE,
) -> CUSTOM_REGISTERS_PROPERTIES_STRICT_TYPE:
    if isinstance(registers, CustomRegister) or isinstance(
        registers, CustomRegisterProperties
    ):
        return (registers,)
    return registers
