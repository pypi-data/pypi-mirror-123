"""This module implements the TaggedGate Class."""
from __future__ import annotations

from typing import Any
from typing import Sequence

import numpy as np

from bqskit.ir.gate import Gate
from bqskit.ir.gates.composedgate import ComposedGate
from bqskit.qis.unitary.differentiable import DifferentiableUnitary
from bqskit.qis.unitary.optimizable import LocallyOptimizableUnitary
from bqskit.qis.unitary.unitarymatrix import UnitaryMatrix


class TaggedGate(
    ComposedGate,
    LocallyOptimizableUnitary,
    DifferentiableUnitary,
):
    """
    The TaggedGate Class.

    Allows a user to place a tag on a gate.
    """

    def __init__(self, gate: Gate, tag: Any) -> None:
        """
        Associate `tag` with `gate`.

        Args:
            gate (Gate): The gate to tag.

            tag (Any): The tag to associate with the gate.
        """

        if not isinstance(gate, Gate):
            raise TypeError('Expected gate object, got %s' % type(gate))

        self.gate = gate
        self.tag = tag
        self._name = 'Tagged(%s:%s)' % (gate.name, str(tag))
        self._num_params = gate.num_params
        self._num_qudits = gate.num_qudits
        self._radixes = gate.radixes

        # If input is a constant gate, we can cache the unitary.
        if self.num_params == 0:
            self.utry = gate.get_unitary()

    def get_unitary(self, params: Sequence[float] = []) -> UnitaryMatrix:
        """Return the unitary for this gate, see :class:`Unitary` for more."""
        if hasattr(self, 'utry'):
            return self.utry

        return self.gate.get_unitary(params)

    def get_grad(self, params: Sequence[float] = []) -> np.ndarray:
        """
        Return the gradient for this gate.

        See :class:`DifferentiableUnitary` for more info.
        """
        if hasattr(self, 'utry'):
            return np.array([])

        return self.gate.get_grad(params)  # type: ignore

    def get_unitary_and_grad(
        self,
        params: Sequence[float] = [],
    ) -> tuple[UnitaryMatrix, np.ndarray]:
        """
        Return the unitary and gradient for this gate.

        See :class:`DifferentiableUnitary` for more info.
        """
        if hasattr(self, 'utry'):
            return self.utry, np.array([])

        return self.gate.get_unitary_and_grad(params)  # type: ignore

    def optimize(self, env_matrix: np.ndarray) -> list[float]:
        """
        Return the optimal parameters with respect to an environment matrix.

        See :class:`LocallyOptimizableUnitary` for more info.
        """
        if hasattr(self, 'utry'):
            return []

        self.check_env_matrix(env_matrix)
        return self.gate.optimize(env_matrix)  # type: ignore
