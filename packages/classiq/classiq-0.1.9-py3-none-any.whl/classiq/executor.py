"""Executor module, implementing facilities for executing quantum programs using Classiq platform."""
from typing import Union

import classiq_interface.executor.execution_preferences
from classiq import api_wrapper
from classiq_interface.executor import (
    result as exc_result,
    execution_request,
    hamiltonian_minimization_problem,
)
from classiq_interface.executor.result import (
    FinanceSimulationResults,
    GroverSimulationResults,
    ExecutionDetails,
)
from classiq_interface.generator import result as generation_result
from classiq_interface.hybrid.result import VQESolverResult


class Executor:
    """Executor is the entry point for executing quantum programs on multiple quantum hardware vendors."""

    def __init__(
        self,
        preferences: classiq_interface.executor.execution_preferences.ExecutionPreferences,
    ) -> None:
        """Init self.

        Args:
            preferences (): Execution preferences, such as number of shots.
        """
        self._preferences = preferences
        self._api_wrapper = api_wrapper.ApiWrapper()

    async def execute_quantum_program(
        self, quantum_program: classiq_interface.executor.quantum_program.QuantumProgram
    ) -> ExecutionDetails:
        request = execution_request.ExecutionRequest(
            quantum_program=quantum_program, preferences=self._preferences
        )
        execution_result = await self._api_wrapper.call_execute_quantum_program_task(
            request=request
        )

        if execution_result.status != exc_result.ExecutionStatus.SUCCESS:
            raise Exception(f"Execution failed: {execution_result.details}")

        return execution_result.details

    async def execute_generated_circuit(
        self, generation_result: generation_result.GeneratedCircuit
    ) -> Union[FinanceSimulationResults, GroverSimulationResults]:
        request = execution_request.ExecutionRequest(
            generation_data=generation_result.metadata, preferences=self._preferences
        )
        execution_result = await self._api_wrapper.call_execute_generated_circuit_task(
            request=request
        )

        if execution_result.status != exc_result.ExecutionStatus.SUCCESS:
            raise Exception(f"Execution failed: {execution_result.details}")

        return execution_result.details

    async def execute_hamiltonian_minimization(
        self,
        hamiltonian_minimization_problem: hamiltonian_minimization_problem.HamiltonianMinimizationProblem,
    ) -> VQESolverResult:
        request = execution_request.ExecutionRequest(
            hamiltonian_minimization_problem=hamiltonian_minimization_problem,
            preferences=self._preferences,
        )
        execution_result = (
            await self._api_wrapper.call_execute_hamiltonian_minimization(
                request=request
            )
        )

        if execution_result.status != exc_result.ExecutionStatus.SUCCESS:
            raise Exception(f"Execution failed: {execution_result.details}")

        return execution_result.details
