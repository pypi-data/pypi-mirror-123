from enum import Enum
from typing import Type, Optional, Any, Union, List

import numpy as np
import numpy.typing
import pydantic

from classiq_interface.generator import function_params, complex_type

DataNumber = Union[complex_type.Complex, float, int]
DataArray = List[List[DataNumber]]


class UnitaryGateInputs(Enum):
    TARGET_QUBIT_IN = "TARGET_QUBIT_IN"


class UnitaryGateOutputs(Enum):
    TARGET_QUBIT_OUT = "TARGET_QUBIT_OUT"


class UnitaryGateControlledInputs(Enum):
    CTRL_IN = "CTRL_IN"
    TARGET_QUBIT_IN = "TARGET_QUBIT_IN"


class UnitaryGateControlledOutputs(Enum):
    CTRL_OUT = "CTRL_OUT"
    TARGET_QUBIT_OUT = "TARGET_QUBIT_OUT"


class UnitaryGate(function_params.FunctionParams):
    """
    Creates a circuit implementing a specified 2**n * 2**n unitary transformation.
    Use the num_ctrl_qubits to create a controlled unitary transformation, and the ctrl_state field to customize the
    control state.
    """

    # TODO - add support to numpy array-like (requires custom pydantic type definition)
    data: DataArray = pydantic.Field(
        description="A 2**n * 2**n (n positive integer) unitary matrix."
    )
    num_ctrl_qubits: Optional[pydantic.PositiveInt] = pydantic.Field(
        description="If specified and greater than 0, returns a num_ctrl_qubits controlled unitary gate"
    )
    ctrl_state: Optional[Union[str, pydantic.conint(ge=0)]] = pydantic.Field(
        description="The control state in decimal or as a bit string (e.g. \‘1011’). If not specified, the control state is 2**num_ctrl_qubits - 1"
    )

    # TODO - decide if to include assertion on the unitarity of the matrix. It is already done in Qiskit and could be computationally expensive
    @pydantic.validator("data")
    def data_to_numpy(cls, data):
        data = np.array(data)
        if data.ndim != 2:
            raise ValueError("Data must me two dimensional")
        if data.shape[0] != data.shape[1]:
            raise ValueError("Matrix must be square")
        if not np.mod(np.log2(data.shape[0]), 1) == 0:
            raise ValueError("Matrix dimensions must be an integer exponent of 2")
        return data

    @pydantic.validator("ctrl_state")
    def validate_ctrl_state(cls, ctrl_state, values):
        num_ctrl_qubits = values.get("num_ctrl_qubits")
        if num_ctrl_qubits is None:
            return ctrl_state
        if ctrl_state is None:
            return "1" * num_ctrl_qubits
        ctrl_state_int = (
            int(ctrl_state, 2) if isinstance(ctrl_state, str) else ctrl_state
        )
        if 0 < ctrl_state_int < 2 ** num_ctrl_qubits:
            return ctrl_state
        else:
            raise ValueError(
                "Control state value should be positive and smaller than 2**num_ctrl_qubits"
            )

    def create_io_enums(self):
        if self.num_ctrl_qubits is None:
            self._input_enum = UnitaryGateInputs
            self._output_enum = UnitaryGateOutputs
        else:
            self._input_enum = UnitaryGateControlledInputs
            self._output_enum = UnitaryGateControlledOutputs
