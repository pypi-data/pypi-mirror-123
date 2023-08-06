from typing import Optional

import pydantic
from classiq_interface.generator import custom_register_utilities
from classiq_interface.generator.custom_function_data import CustomFunctionData
from classiq_interface.generator.custom_register import CustomRegister
from qiskit import circuit as qiskit_circuit
from qiskit import qasm as qiskit_qasm

DEFAULT_CUSTOM_IMPLEMENTATION_ZERO_INPUT = "DEFAULT_CUSTOM_IMPLEMENTATION_ZERO_INPUT"


class CustomFunctionImplementation(pydantic.BaseModel):
    """
    A user-defined custom implementation.
    """

    class Config:
        validate_all = True

    name: Optional[str] = pydantic.Field(
        default=None,
        description="The name of the custom implementation",
    )

    num_qubits_in_serialized_circuit: Optional[pydantic.PositiveInt] = pydantic.Field(
        default=None,
        alias="_num_qubits_in_serialized_circuit",
        description="This is a private attribute",
    )

    serialized_circuit: pydantic.constr(min_length=1) = pydantic.Field(
        description="The QASM code of the custom implementation",
    )

    input_registers: custom_register_utilities.CUSTOM_REGISTERS_TYPE = pydantic.Field(
        description="A tuple of input registers to the custom implementation",
    )

    output_registers: custom_register_utilities.CUSTOM_REGISTERS_TYPE = pydantic.Field(
        description="A tuple of output registers of the custom implementation",
    )

    custom_function_data: CustomFunctionData = pydantic.Field(
        description="The custom function IO parmeters required for validation",
    )

    zero_input_registers: Optional[
        custom_register_utilities.CUSTOM_REGISTERS_TYPE
    ] = pydantic.Field(
        default=None,
        description="A tuple of zero input registers to the custom implementation",
    )

    auxiliary_registers: Optional[
        custom_register_utilities.CUSTOM_REGISTERS_TYPE
    ] = pydantic.Field(
        default=None,
        description="A tuple of auxiliary registers to the custom implementation",
    )

    @staticmethod
    def get_num_qubits_in_qasm(qasm_string: str) -> int:
        try:
            qc = qiskit_circuit.QuantumCircuit.from_qasm_str(qasm_string)
        except qiskit_qasm.exceptions.QasmError:  # The qiskit error is often extremely uninformative
            raise ValueError("The QASM string is not a valid quantum circuit.")
        return qc.num_qubits

    @pydantic.validator(
        "input_registers",
        "output_registers",
        "zero_input_registers",
        "auxiliary_registers",
        pre=True,
    )
    def validate_all_registers_are_iterable(
        cls,
        registers: custom_register_utilities.CUSTOM_REGISTERS_TYPE,
    ):
        return custom_register_utilities.convert_single_register_to_iterable(
            registers=registers
        )

    @pydantic.validator("serialized_circuit")
    def validate_serialized_circuit_and_num_qubits_in_serialized_circuit(
        cls, serialized_circuit, values
    ):
        if serialized_circuit is None:
            raise ValueError("Not enough input to define a custom implementation.")
        values["num_qubits_in_serialized_circuit"] = cls.get_num_qubits_in_qasm(
            qasm_string=serialized_circuit
        )
        return serialized_circuit

    @pydantic.root_validator(skip_on_failure=True)
    def validate_all_registers(cls, values):
        input_registers: custom_register_utilities.CUSTOM_REGISTERS_STRICT_TYPE = (
            values.get("input_registers")
        )
        output_registers: custom_register_utilities.CUSTOM_REGISTERS_STRICT_TYPE = (
            values.get("output_registers")
        )
        zero_input_registers: custom_register_utilities.CUSTOM_REGISTERS_STRICT_TYPE = (
            values.get("zero_input_registers")
        )
        auxiliary_registers: custom_register_utilities.CUSTOM_REGISTERS_STRICT_TYPE = (
            values.get("auxiliary_registers")
        )

        all_output_registers = output_registers + auxiliary_registers
        output_qubits = set().union(
            *[set(register.qubits) for register in all_output_registers]
        )
        if len(output_qubits) != sum(
            register.width for register in all_output_registers
        ):
            raise ValueError(
                f"The output registers of a custom function must not overlap."
            )

        all_input_registers = (
            input_registers + zero_input_registers + auxiliary_registers
        )
        input_qubits = set().union(
            *[set(register.qubits) for register in all_input_registers]
        )
        if len(input_qubits) != sum(register.width for register in all_input_registers):
            raise ValueError(
                f"The input registers of a custom function must not overlap."
            )
        if input_qubits != set(range(values.get("num_qubits_in_serialized_circuit"))):
            raise ValueError(
                f"The number of qubits in the quantum circuit of the implementation must match its input registers."
            )

        return values

    @pydantic.validator("zero_input_registers")
    def validate_zero_input_registers(
        cls,
        zero_input_registers: custom_register_utilities.CUSTOM_REGISTERS_STRICT_TYPE,
        values,
    ):
        output_qubits = set().union(
            *[set(register.qubits) for register in values.get("output_registers")]
        )
        input_qubits = set().union(
            *[set(register.qubits) for register in values.get("input_registers")]
        )
        zero_input_qubits = tuple(output_qubits.difference(input_qubits))
        if zero_input_registers is None:
            if len(zero_input_qubits) == 0:
                return ()
            return (
                CustomRegister(
                    name=DEFAULT_CUSTOM_IMPLEMENTATION_ZERO_INPUT,
                    qubits=zero_input_qubits,
                ),
            )
        return zero_input_registers

    @pydantic.validator("auxiliary_registers")
    def validate_auxiliary_registers(
        cls,
        auxiliary_registers: custom_register_utilities.CUSTOM_REGISTERS_STRICT_TYPE,
    ):
        if auxiliary_registers is None:
            return ()
        return auxiliary_registers

    @classmethod
    def _validate_io_registers_properties(
        cls,
        io_registers_properties: custom_register_utilities.CUSTOM_REGISTERS_PROPERTIES_STRICT_TYPE,
        io_registers: custom_register_utilities.CUSTOM_REGISTERS_STRICT_TYPE,
    ):
        error_message = "The IO registers of the implementation must match the IO register properties of the custom function."
        if len(io_registers) != len(io_registers_properties):
            raise ValueError(error_message)
        sorted_io_registers = sorted(io_registers, key=lambda register: register.name)
        sorted_io_registers_properties = sorted(
            io_registers_properties, key=lambda register: register.name
        )
        for register, register_properties in zip(
            sorted_io_registers, sorted_io_registers_properties
        ):
            if not register.is_compatible(register=register_properties):
                raise ValueError(error_message)

    @pydantic.validator("custom_function_data")
    def validate_custom_function_data(
        cls, custom_function_data: CustomFunctionData, values
    ):
        cls._validate_io_registers_properties(
            io_registers=values.get("input_registers"),
            io_registers_properties=custom_function_data.input_registers_properties,
        )
        cls._validate_io_registers_properties(
            io_registers=values.get("output_registers"),
            io_registers_properties=custom_function_data.output_registers_properties,
        )
        return custom_function_data
