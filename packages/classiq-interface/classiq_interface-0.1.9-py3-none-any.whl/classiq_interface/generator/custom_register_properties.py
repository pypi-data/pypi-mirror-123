import pydantic


class CustomRegisterProperties(pydantic.BaseModel):
    """
    The properties of a user-defined custom quantum register.
    """

    name: str = pydantic.Field(
        description="The name of the custom register",
    )

    width: pydantic.PositiveInt = pydantic.Field(
        description="The number of qubits of the custom register",
    )
