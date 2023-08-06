from enum import Enum
from typing import List

import pydantic
from classiq_interface.generator import custom_register_utilities
from classiq_interface.generator.custom_function_data import CustomFunctionData
from classiq_interface.generator.custom_function_implementation import (
    CustomFunctionImplementation,
)
from classiq_interface.generator.function_params import FunctionParams

DEFAULT_CUSTOM_FUNCTION_INPUT = "DEFAULT_CUSTOM_FUNCTION_INPUT"
DEFAULT_CUSTOM_FUNCTION_OUTPUT = "DEFAULT_CUSTOM_FUNCTION_OUTPUT"


class CustomFunction(FunctionParams):
    """
    Facilitates the creation of a user-defined custom function
    """

    data: CustomFunctionData = pydantic.Field(
        description="IO data of the custom function",
    )

    implementations: List[CustomFunctionImplementation] = pydantic.Field(
        default_factory=list,
        description="The implementations of the custom function",
    )

    allow_synthesis_with_stub: bool = pydantic.Field(
        default=False,
        description="Authorize automatic generation of identity gates for stub functions",
    )

    def add_implementation(
        self,
        serialized_circuit: str,
        input_registers: custom_register_utilities.CUSTOM_REGISTERS_TYPE,
        output_registers: custom_register_utilities.CUSTOM_REGISTERS_TYPE,
        zero_input_registers: custom_register_utilities.CUSTOM_REGISTERS_TYPE = None,
        auxiliary_registers: custom_register_utilities.CUSTOM_REGISTERS_TYPE = None,
        implementation_name: str = None,
    ) -> CustomFunctionImplementation:
        """Adds an implementation to the custom function.

        Args:
            serialized_circuit (str): A QASM code of the custom implementation.
            input_registers (tuple): The inputs of the custom implementation as either a register or a tuple of registers.
            output_registers (tuple): The outputs of the custom implementation as either a register or a tuple of registers.
            zero_input_registers (:obj:`tuple`, optional): The zero inputs of the custom implementation as either a register or a tuple of registers.
            auxiliary_registers (:obj:`tuple`, optional): The auxiliary qubits of the custom implementation as either a register or a tuple of registers.
            implementation_name (:obj:`str`, optional): The name of the custom implementation.

        Returns:
            The custom function parameters.
        """

        custom_implementation = CustomFunctionImplementation(
            name=implementation_name,
            serialized_circuit=serialized_circuit,
            custom_function_data=self.data,
            input_registers=input_registers,
            output_registers=output_registers,
            zero_input_registers=zero_input_registers,
            auxiliary_registers=auxiliary_registers,
        )
        self.implementations.append(custom_implementation)
        return custom_implementation

    def create_io_enums(self):
        self._input_enum = Enum(
            f"_input_enum of {self.name}",
            {
                register.name: register.name
                for register in self.input_registers_properties
            },
        )
        self._output_enum = Enum(
            f"_output_enum of {self.name}",
            {
                register.name: register.name
                for register in self.output_registers_properties
            },
        )

    @property
    def name(self):
        """The name of the custom function"""
        return self.data.name

    @property
    def is_stub(self) -> bool:
        return not self.implementations

    @property
    def input_registers_properties(
        self,
    ) -> custom_register_utilities.CUSTOM_REGISTERS_PROPERTIES_STRICT_TYPE:
        """A tuple of output register properties to the custom function"""
        return self.data.input_registers_properties

    @property
    def output_registers_properties(
        self,
    ) -> custom_register_utilities.CUSTOM_REGISTERS_PROPERTIES_STRICT_TYPE:
        """A tuple of input register properties of the custom function"""
        return self.data.output_registers_properties
