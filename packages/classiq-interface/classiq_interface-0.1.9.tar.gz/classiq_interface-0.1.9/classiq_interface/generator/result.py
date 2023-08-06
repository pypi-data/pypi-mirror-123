import base64
import enum
import io
from typing import Union, List, Optional

import pydantic
from PIL import Image
from classiq_interface.generator.generation_metadata import GenerationMetadata


class QuantumFormat(str, enum.Enum):
    QASM = "qasm"
    QSHARP = "qs"
    QIR = "ll"
    IONQ = "ionq"
    CIRQ = "cirq"


class GenerationStatus(str, enum.Enum):
    NONE = "none"
    SUCCESS = "success"
    UNSAT = "unsat"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"
    ERROR = "error"


# TODO: Merge all output formats to single field (dictionary?) to avoid clutter
class GeneratedCircuit(pydantic.BaseModel):
    qasm: Optional[str]
    qsharp: Optional[str]
    qir: Optional[str]
    ionq: Optional[str]
    cirq: Optional[str]
    output_format: List[QuantumFormat]
    image: str
    qviz_html: Optional[str]
    metadata: GenerationMetadata

    def show(self) -> None:
        image = Image.open(io.BytesIO(base64.b64decode(self.image)))
        image.show()


class GenerationResult(pydantic.BaseModel):
    status: GenerationStatus
    details: Union[GeneratedCircuit, str]
