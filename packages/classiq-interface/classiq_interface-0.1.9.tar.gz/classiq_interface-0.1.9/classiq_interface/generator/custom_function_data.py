import pydantic
from classiq_interface.generator import custom_register_utilities


class CustomFunctionData(pydantic.BaseModel):
    name: str = pydantic.Field(description="The name of a custom function")

    input_registers_properties: custom_register_utilities.CUSTOM_REGISTERS_PROPERTIES_TYPE = pydantic.Field(
        description="A tuple of input register properties to the custom function"
    )

    output_registers_properties: custom_register_utilities.CUSTOM_REGISTERS_PROPERTIES_TYPE = pydantic.Field(
        description="A tuple of output register properties of the custom function"
    )

    @pydantic.validator("input_registers_properties", "output_registers_properties")
    def validate_io_registers_properties(
        cls,
        io_registers_properties: custom_register_utilities.CUSTOM_REGISTERS_PROPERTIES_TYPE,
    ):
        if io_registers_properties == ():
            raise ValueError(
                "The inputs and outputs of a custom function must be non-empty."
            )

        io_registers_properties = (
            custom_register_utilities.convert_single_register_to_iterable(
                registers=io_registers_properties
            )
        )

        if len(io_registers_properties) != len(
            {
                register_properties.name
                for register_properties in io_registers_properties
            }
        ):
            raise ValueError("The names of IO registers must be distinct.")
        return io_registers_properties
