"""Custom function library module, implementing facilities for adding user defined functions to the Classiq platform."""

from typing import Tuple, Dict, Union, Optional

from classiq_interface.generator import custom_register_utilities
from classiq_interface.generator.custom_function import (
    CustomFunction,
    DEFAULT_CUSTOM_FUNCTION_INPUT,
    DEFAULT_CUSTOM_FUNCTION_OUTPUT,
)
from classiq_interface.generator.custom_function_data import CustomFunctionData
from classiq_interface.generator.custom_function_implementation import (
    CustomFunctionImplementation,
)
from classiq_interface.generator.custom_register import CustomRegister
from classiq_interface.generator.custom_register_properties import (
    CustomRegisterProperties,
)


class CustomFunctionLibrary:
    """Facility to manage user-defined custom functions."""

    def __init__(self, name: str = None):
        self._custom_functions_dict: Dict[str, CustomFunction] = dict()
        self._name: Optional[str] = name

    def get_custom_function(self, function_name: str) -> CustomFunction:
        """Gets a function from the function library.

        Args:
            function_name (str): The name of the custom function.

        Returns:
            The custom function parameters.
        """
        return self._custom_functions_dict[function_name]

    @staticmethod
    def new_register(
        register_name: str = None, qubits: Tuple[int, ...] = None, width: int = None
    ) -> Union[CustomRegister, CustomRegisterProperties]:
        """Create either a new custom register or a custom register properties object.

        Args:
            register_name (:obj:`str`, optional): The name of the custom register.
            qubits (:obj:`tuple`, optional): A tuple of integers indexing the qubits of the register.
            width (:obj:`int`, optional): The number of qubits of the custom register.

        Returns:
            Either a CustomRegister or a CustomRegisterProperties object.
        """
        if qubits is None:
            return CustomRegisterProperties(name=register_name, width=width)
        if width is not None and len(qubits) != width:
            raise ValueError(
                f"the width and qubits of the new custom register are incompatible."
            )
        return CustomRegister(name=register_name, qubits=qubits)

    def add_function(
        self,
        function_name: str,
        input_registers_properties: custom_register_utilities.CUSTOM_REGISTERS_PROPERTIES_TYPE = None,
        output_registers_properties: custom_register_utilities.CUSTOM_REGISTERS_PROPERTIES_TYPE = None,
        serialized_circuit: str = None,
        implementation_name: str = None,
        input_registers: custom_register_utilities.CUSTOM_REGISTERS_TYPE = None,
        output_registers: custom_register_utilities.CUSTOM_REGISTERS_TYPE = None,
        zero_input_registers: custom_register_utilities.CUSTOM_REGISTERS_TYPE = None,
        auxiliary_registers: custom_register_utilities.CUSTOM_REGISTERS_TYPE = None,
        override_existing_custom_functions: bool = False,
        allow_synthesis_with_stub: bool = False,
    ) -> CustomFunction:
        """Adds a function to the function library.

        Args:
            function_name (str): The name of the custom function.
            input_registers_properties (:obj:`tuple`, optional): The inputs of the custom function as either a register or a tuple of registers.
            output_registers_properties (:obj:`tuple`, optional): The outputs of the custom function as either a register or a tuple of registers.
            serialized_circuit (:obj:`str`, optional): A QASM code of the custom implementation.
            implementation_name (:obj:`str`, optional): The name of the custom implementation.
            input_registers (:obj:`tuple`, optional): The inputs of the custom implemenation as either a register or a tuple of registers.
            output_registers (:obj:`tuple`, optional): The outputs of the custom implemenation as either a register or a tuple of registers.
            zero_input_registers (:obj:`tuple`, optional): The zero inputs of the custom implemenation as either a register or a tuple of registers.
            auxiliary_registers (:obj:`tuple`, optional): The auxiliary qubits of the custom implemenation as either a register or a tuple of registers.
            override_existing_custom_functions (:obj:`bool`, optional): Defaults to False.
            allow_synthesis_with_stub (:obj:`bool`, optional): Defaults to False.

        Returns:
            The custom function parameters.
        """
        if (
            not override_existing_custom_functions
            and function_name in self._custom_functions_dict
        ):
            raise ValueError("Cannot override existing custom functions.")

        if (
            serialized_circuit is not None
            and input_registers is None
            and output_registers is None
            and input_registers_properties is None
            and output_registers_properties is None
        ):
            num_io_qubits = CustomFunctionImplementation.get_num_qubits_in_qasm(
                qasm_string=serialized_circuit
            )
            io_qubits = tuple(range(num_io_qubits))
            input_registers = (
                CustomRegister(name=DEFAULT_CUSTOM_FUNCTION_INPUT, qubits=io_qubits),
            )
            output_registers = (
                CustomRegister(name=DEFAULT_CUSTOM_FUNCTION_OUTPUT, qubits=io_qubits),
            )
        if input_registers_properties is None:
            input_registers_properties = input_registers
        if output_registers_properties is None:
            output_registers_properties = output_registers

        custom_function = CustomFunction(
            data=CustomFunctionData(
                name=function_name,
                input_registers_properties=input_registers_properties,
                output_registers_properties=output_registers_properties,
            ),
            allow_synthesis_with_stub=allow_synthesis_with_stub,
        )
        if serialized_circuit is not None:
            custom_function.add_implementation(
                serialized_circuit=serialized_circuit,
                implementation_name=implementation_name,
                input_registers=input_registers,
                output_registers=output_registers,
                zero_input_registers=zero_input_registers,
                auxiliary_registers=auxiliary_registers,
            )
        elif (
            implementation_name is not None
            or zero_input_registers is not None
            or auxiliary_registers is not None
        ):
            raise ValueError(
                "Explicit implementation details require an explicit QASM string."
            )

        self._custom_functions_dict[custom_function.name] = custom_function
        return custom_function

    def remove_function(self, function_name: str) -> CustomFunction:
        """Removes a function from the function library.

        Args:
            function_name (str): The name of the custom function.

        Returns:
            The removed custom function parameters.
        """
        return self._custom_functions_dict.pop(function_name)

    @property
    def name(self) -> str:
        """Get the library name.

        Returns:
            The library name.
        """
        return self._name

    @property
    def function_names(self) -> Tuple[str, ...]:
        """Get a tuple of the names of the custom functions in the library.

        Returns:
            The names of the custom functions in the library.
        """
        return tuple(self._custom_functions_dict.keys())
