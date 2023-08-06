import pydantic

from classiq_interface.executor.quantum_program import QuantumProgram
from classiq_interface.chemistry.operator import PauliOperator


class HamiltonianMinimizationProblem(pydantic.BaseModel):
    ansatz: QuantumProgram
    hamiltonian: PauliOperator
