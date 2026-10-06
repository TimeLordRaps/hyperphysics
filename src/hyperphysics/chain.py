"""Operation chains: the dynamics and static features of a chain of operations.

hyperphysics is "the mechanics, dynamics, and static features of operations" (FIELD_STACK.md). The
smallest instance is a chain: a start state `psi_0` and operations `U_1 ... U_n`, each a unitary matrix.
Two facts are stated here once, with their validity conditions, so that adjacent fields can cite them.

1. VIOLATION ENERGY. For ANY sequence of states `psi_0 ... psi_n`, the quantity
   `E = sum_t || psi_t - U_t psi_{t-1} ||^2` is the expectation `<psi|H|psi>` of the propagation
   Hamiltonian `H` on the clock-system space (Kitaev's circuit-to-Hamiltonian construction, recalled).
   So `E = 0` exactly when every step is the operation applied to its predecessor, and then the chain is
   fixed by `psi_0` alone: a derivation chain whose dynamics is validity, not evolution in a time.
2. THE FROZEN STATE. The history state `|h> = (n+1)^(-1/2) sum_t |t> (x) U_t...U_1 psi_0` has `H|h> = 0`.
   It does not evolve, yet conditioned on the clock reading `t` it is the t-th step. `H` has spectral gap
   `2 - 2 cos(pi/(n+1))` above its zero modes (a path graph after a gauge change), about `pi^2/(n+1)^2`.

WHAT IS NOT CLAIMED. Nothing here is a model of any physical sheet, wormhole or clock. These are exact
statements about finite chains of unitary matrices, checked numerically to a stated tolerance. The gap is
the gap of the propagation Hamiltonian alone; it says nothing about preparing the state in any physical
process. Pure Python, complex arithmetic, no outside dependency.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

Vector = tuple
Matrix = tuple

TOLERANCE = 1e-9


@dataclass(frozen=True, slots=True)
class ChainLaw:
    """A stated fact about chains, with its validity and failure modes as data."""

    name: str
    statement: str
    form: str
    validity: str
    fails_when: tuple

    def __post_init__(self) -> None:
        for value, label in ((self.name, "name"), (self.statement, "statement"),
                             (self.form, "form"), (self.validity, "validity")):
            if type(value) is not str or not value.strip():
                raise ValueError(f"chain law {label} must be a nonempty string")
        if not self.fails_when:
            raise ValueError("a chain law states at least one failure mode")


def _check_vector(v: Vector, dim: int | None = None) -> int:
    if type(v) is not tuple or not v:
        raise ValueError("a state is a nonempty tuple of complex numbers")
    if dim is not None and len(v) != dim:
        raise ValueError("state dimension does not match the operations")
    return len(v)


def norm(v: Vector) -> float:
    return math.sqrt(sum(abs(x) ** 2 for x in v))


def mat_vec(m: Matrix, v: Vector) -> Vector:
    return tuple(sum(row[k] * v[k] for k in range(len(v))) for row in m)


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)) for i in range(n))


def dagger(m: Matrix) -> Matrix:
    n = len(m)
    return tuple(tuple(m[j][i].conjugate() for j in range(n)) for i in range(n))


def is_unitary(m: Matrix, tol: float = TOLERANCE) -> bool:
    n = len(m)
    if any(len(row) != n for row in m):
        return False
    p = mat_mul(dagger(m), m)
    return all(abs(p[i][j] - (1 if i == j else 0)) < tol for i in range(n) for j in range(n))


@dataclass(frozen=True)
class OperationChain:
    """`ops[t-1]` is `U_t`. All operations are unitary and of the dimension of `state0`."""

    ops: tuple
    state0: Vector

    def __post_init__(self) -> None:
        dim = _check_vector(self.state0)
        if abs(norm(self.state0) - 1.0) > TOLERANCE:
            raise ValueError("the start state must be normalized")
        if type(self.ops) is not tuple or not self.ops:
            raise ValueError("a chain has at least one operation")
        for u in self.ops:
            if len(u) != dim or not is_unitary(u):
                raise ValueError("every operation must be a unitary matrix of the state's dimension")

    @property
    def steps(self) -> int:
        return len(self.ops)

    def states(self) -> tuple:
        """The one valid chain from `state0`: `psi_t = U_t psi_{t-1}`."""
        out = [self.state0]
        for u in self.ops:
            out.append(mat_vec(u, out[-1]))
        return tuple(out)

    def violations(self, states: tuple) -> tuple:
        """Squared violation of each step, for any claimed sequence of `steps + 1` states."""
        self._check_states(states)
        return tuple(
            sum(abs(a - b) ** 2 for a, b in zip(states[t], mat_vec(self.ops[t - 1], states[t - 1])))
            for t in range(1, self.steps + 1)
        )

    def violation_energy(self, states: tuple) -> float:
        return sum(self.violations(states))

    def is_valid(self, states: tuple, tol: float = TOLERANCE) -> bool:
        return self.violation_energy(states) < tol

    def propagate(self, clock_states: tuple) -> tuple:
        """`H psi` for the propagation Hamiltonian, on `psi = (psi_0, ..., psi_n)`."""
        self._check_states(clock_states)
        n = self.steps
        out = []
        for s in range(n + 1):
            diag = (1 if s > 0 else 0) + (1 if s < n else 0)
            v = [diag * x for x in clock_states[s]]
            if s > 0:
                w = mat_vec(self.ops[s - 1], clock_states[s - 1])
                v = [a - b for a, b in zip(v, w)]
            if s < n:
                w = mat_vec(dagger(self.ops[s]), clock_states[s + 1])
                v = [a - b for a, b in zip(v, w)]
            out.append(tuple(v))
        return tuple(out)

    def energy_expectation(self, clock_states: tuple) -> float:
        hpsi = self.propagate(clock_states)
        return sum((a.conjugate() * b).real for pb, hb in zip(clock_states, hpsi) for a, b in zip(pb, hb))

    def history_state(self) -> tuple:
        """The normalized zero mode `(n+1)^(-1/2) (psi_0, ..., psi_n)` of the propagation Hamiltonian."""
        s = 1 / math.sqrt(self.steps + 1)
        return tuple(tuple(x * s for x in block) for block in self.states())

    def conditioned_on(self, history: tuple, t: int) -> Vector:
        """The system state given clock reading `t`, renormalized."""
        if not 0 <= t <= self.steps:
            raise ValueError("clock reading out of range")
        block = history[t]
        n = norm(block)
        return tuple(x / n for x in block)

    def gap(self) -> float:
        """Spectral gap above the zero modes: `2 - 2 cos(pi/(steps+1))`."""
        return 2 - 2 * math.cos(math.pi / (self.steps + 1))

    def readout_probability(self, idle_steps: int = 0) -> float:
        """Probability that measuring the clock of the history state finds the last real step,
        after appending `idle_steps` identity steps."""
        if type(idle_steps) is not int or idle_steps < 0:
            raise ValueError("idle_steps must be a nonnegative integer")
        return (idle_steps + 1) / (self.steps + idle_steps + 1)

    def _check_states(self, states: tuple) -> None:
        if type(states) is not tuple or len(states) != self.steps + 1:
            raise ValueError("a claimed chain has steps + 1 states")
        for block in states:
            _check_vector(block, len(self.state0))


def closing_operation(ops: tuple) -> Matrix:
    """The operation `(U_n ... U_1)^dagger` that closes a chain into a circuit."""
    product = ops[0]
    for u in ops[1:]:
        product = mat_mul(u, product)
    return dagger(product)


def closes(chain: OperationChain, tol: float = TOLERANCE) -> bool:
    """True when the full product of the operations returns the start state."""
    end = chain.states()[-1]
    return norm(tuple(a - b for a, b in zip(end, chain.state0))) < tol


def selector_branches(chains: tuple, amplitudes: tuple) -> tuple:
    """History states of a direct sum `H_A (x) |0><0| + H_B (x) |1><1|`: the selector-weighted
    branches, each stationary on its own. Choosing the selector bit once picks the computation
    without changing `H`. Returns `(amplitude, history_state)` pairs."""
    if len(chains) != len(amplitudes) or not chains:
        raise ValueError("one amplitude per chain")
    if abs(sum(abs(a) ** 2 for a in amplitudes) - 1.0) > TOLERANCE:
        raise ValueError("selector amplitudes must be normalized")
    return tuple((a, c.history_state()) for a, c in zip(amplitudes, chains))


def mismatch(ops: tuple, state0: Vector, target: Vector) -> Vector:
    """`(U_n ... U_1)^dagger target - state0`: how far the forced chain from `state0` ends from `target`,
    pulled back to the start. Zero exactly when the chain already reaches `target`."""
    # (U_n ... U_1)^dagger = U_1^dagger ... U_n^dagger: apply U_n^dagger first
    v = tuple(target)
    for u in reversed(ops):
        v = mat_vec(dagger(u), v)
    return tuple(a - b for a, b in zip(v, state0))


def minimal_violation_energy(ops: tuple, state0: Vector, target: Vector) -> float:
    """Least total squared step violation over all chains from `state0` to `target` (intermediate
    states unconstrained, quadratic cost): `||mismatch||^2 / n`. The correction is spread evenly over
    the `n` steps, so a longer chain pays less in total and each step is violated by `||mismatch||/n`."""
    d = mismatch(ops, state0, target)
    return sum(abs(x) ** 2 for x in d) / len(ops)


def least_violation_states(ops: tuple, state0: Vector, target: Vector) -> tuple:
    """The minimizer of the violation energy between fixed ends: `psi_t = U_t...U_1 (state0 + (t/n) d)`.
    Intermediate states are not constrained to unit norm; with that constraint the minimum is larger."""
    n = len(ops)
    d = mismatch(ops, state0, target)
    out = [tuple(state0)]
    for t in range(1, n + 1):
        phi = tuple(a + (t / n) * b for a, b in zip(state0, d))
        v = phi
        for u in ops[:t]:
            v = mat_vec(u, v)
        out.append(v)
    return tuple(out)


def split_cost(total: float, parts: int, exponent: float, concentrated: bool) -> float:
    """Cost `sum |d_i|^exponent` of splitting a total correction `total` evenly over `parts` steps, or
    putting all of it in one step. Convex cost (exponent > 1) prefers spreading, concave (< 1) prefers
    one discrete junction, and exponent 1 is indifferent."""
    if total < 0 or parts < 1 or exponent <= 0:
        raise ValueError("need total >= 0, parts >= 1, exponent > 0")
    if concentrated:
        return total ** exponent
    return parts * (total / parts) ** exponent


CHAIN_LAWS = (
    ChainLaw(
        name="violation-energy",
        statement="The propagation Hamiltonian's expectation on any clock-system state is the total "
                  "squared violation of the steps; it vanishes exactly on chains whose every step is "
                  "valid, and such a chain is fixed by its start state.",
        form="<psi|H|psi> = sum_t || psi_t - U_t psi_{t-1} ||^2",
        validity="Finite-dimensional unitary operations; states of the clock-system space.",
        fails_when=(
            "an operation is not unitary, so the cross terms no longer match",
            "the clock is not a path (a cyclic clock needs the closing operation, see `closes`)",
        ),
    ),
    ChainLaw(
        name="least-violation",
        statement="Between fixed ends that the operations cannot connect, the chain of least total squared "
                  "step violation spreads the correction evenly, with total ||mismatch||^2 / n; with a concave "
                  "cost the least-cost correction is instead concentrated in one step.",
        form="min E = ||(U_n...U_1)^dagger target - state0||^2 / n",
        validity="Quadratic cost, intermediate states unconstrained; the concave comparison is of cost "
                 "exponents only.",
        fails_when=(
            "intermediate states are required to be normalized (the minimum is larger)",
            "the cost is not a sum over steps",
        ),
    ),
    ChainLaw(
        name="history-state",
        statement="The history state is annihilated by the propagation Hamiltonian, does not evolve, and "
                  "conditioned on clock reading t is the t-th step of the computation.",
        form="H |h> = 0, |h> = (n+1)^(-1/2) sum_t |t> (x) U_t...U_1 psi_0",
        validity="The Hamiltonian is exactly the designed one.",
        fails_when=(
            "one operation in H differs from the operation the state was built with",
            "a perturbation not in the designed algebra is added (the zero mode moves)",
        ),
    ),
    ChainLaw(
        name="propagation-gap",
        statement="Above its zero modes the propagation Hamiltonian has gap 2 - 2 cos(pi/(n+1)), about "
                  "pi^2/(n+1)^2, so adiabatic preparation takes at least of order 1/gap.",
        form="gap = 2 - 2 cos(pi / (n + 1))",
        validity="Path clock, unitary operations, the Hamiltonian alone.",
        fails_when=(
            "a cyclic clock replaces the path",
            "preparation is by a process other than the adiabatic one (no bound is given for it here)",
        ),
    ),
)
