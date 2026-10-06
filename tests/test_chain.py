"""Tests for operation chains: violation energy, the history state, the gap, closure, branches."""

from __future__ import annotations

import math
import random

import pytest

from hyperphysics.chain import (
    CHAIN_LAWS,
    ChainLaw,
    OperationChain,
    closes,
    closing_operation,
    dagger,
    is_unitary,
    mat_mul,
    mat_vec,
    norm,
    selector_branches,
)


def random_unitary(rng, dim):
    cols = []
    for _ in range(dim):
        v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(dim)]
        for c in cols:  # Gram-Schmidt
            ip = sum(a.conjugate() * b for a, b in zip(c, v))
            v = [b - ip * a for a, b in zip(c, v)]
        n = math.sqrt(sum(abs(x) ** 2 for x in v))
        cols.append([x / n for x in v])
    return tuple(tuple(cols[j][i] for j in range(dim)) for i in range(dim))


def random_state(rng, dim):
    v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(dim)]
    n = math.sqrt(sum(abs(x) ** 2 for x in v))
    return tuple(x / n for x in v)


def make_chain(seed, dim=3, steps=4):
    rng = random.Random(seed)
    return OperationChain(tuple(random_unitary(rng, dim) for _ in range(steps)), random_state(rng, dim)), rng


@pytest.mark.parametrize("dim", [2, 3, 4])
def test_energy_is_total_squared_violation_on_arbitrary_states(dim):
    chain, rng = make_chain(dim, dim)
    for _ in range(50):
        psi = tuple(random_state(rng, dim) for _ in range(chain.steps + 1))
        assert abs(chain.energy_expectation(psi) - chain.violation_energy(psi)) < 1e-12


def test_valid_chain_has_zero_energy_and_a_broken_one_does_not():
    chain, rng = make_chain(1)
    states = chain.states()
    assert chain.violation_energy(states) < 1e-14 and chain.is_valid(states)
    broken = list(states)
    broken[2] = random_state(rng, 3)
    assert not chain.is_valid(tuple(broken))
    assert chain.violations(tuple(broken))[1] > 1e-3 or chain.violations(tuple(broken))[2] > 1e-3


def test_history_state_is_a_normalized_zero_mode_and_conditions_to_each_step():
    chain, _ = make_chain(2, dim=3, steps=5)
    h = chain.history_state()
    assert abs(math.sqrt(sum(abs(x) ** 2 for b in h for x in b)) - 1.0) < 1e-12
    assert max(abs(x) for b in chain.propagate(h) for x in b) < 1e-12
    for t, state in enumerate(chain.states()):
        assert max(abs(a - b) for a, b in zip(chain.conditioned_on(h, t), state)) < 1e-12


def test_a_different_hamiltonian_does_not_annihilate_the_state_negative_control():
    chain, rng = make_chain(3)
    other_ops = list(chain.ops)
    other_ops[1] = random_unitary(rng, 3)
    other = OperationChain(tuple(other_ops), chain.state0)
    assert max(abs(x) for b in other.propagate(chain.history_state()) for x in b) > 0.05


@pytest.mark.parametrize("steps", [3, 8, 30])
def test_gap_is_the_cosine_mode_of_the_gauge_transformed_path(steps):
    chain, rng = make_chain(steps, dim=2, steps=steps)
    lam = chain.gap()
    assert abs(lam - (2 - 2 * math.cos(math.pi / (steps + 1)))) < 1e-15
    assert abs(lam - math.pi ** 2 / (steps + 1) ** 2) / lam < 0.1
    blocks = chain.states()
    v = [math.cos(math.pi * (t + 0.5) / (steps + 1)) for t in range(steps + 1)]
    psi = tuple(tuple(v[t] * x for x in blocks[t]) for t in range(steps + 1))
    hpsi = chain.propagate(psi)
    resid = math.sqrt(sum(abs(a - lam * b) ** 2 for hb, pb in zip(hpsi, psi) for a, b in zip(hb, pb)))
    assert resid / math.sqrt(sum(abs(x) ** 2 for b in psi for x in b)) < 1e-12


def test_readout_probability_and_idle_padding():
    chain, _ = make_chain(4, dim=2, steps=5)
    assert abs(chain.readout_probability() - 1 / 6) < 1e-15
    assert abs(chain.readout_probability(5) - 6 / 11) < 1e-15
    assert chain.readout_probability(50) > chain.readout_probability(5) > chain.readout_probability()
    with pytest.raises(ValueError):
        chain.readout_probability(-1)


def test_a_closing_operation_makes_the_circuit_close_and_otherwise_it_does_not():
    chain, rng = make_chain(5, dim=3, steps=2)
    assert not closes(chain)
    closed = OperationChain(chain.ops + (closing_operation(chain.ops),), chain.state0)
    assert closes(closed)
    open_ = OperationChain(chain.ops + (random_unitary(rng, 3),), chain.state0)
    assert not closes(open_)


def test_selector_branches_are_each_stationary_and_differ():
    a, _ = make_chain(6, dim=2, steps=3)
    b, _ = make_chain(7, dim=2, steps=3)
    branches = selector_branches((a, b), (1 / math.sqrt(2), 1 / math.sqrt(2)))
    for chain, (amp, h) in zip((a, b), branches):
        assert max(abs(x) for blk in chain.propagate(h) for x in blk) < 1e-12
    ha, hb = branches[0][1], branches[1][1]
    assert abs(sum(x.conjugate() * y for u, v in zip(ha, hb) for x, y in zip(u, v))) < 0.999
    with pytest.raises(ValueError):
        selector_branches((a, b), (1.0, 1.0))


def test_validity_conditions_are_enforced():
    rng = random.Random(8)
    u = random_unitary(rng, 2)
    s = random_state(rng, 2)
    with pytest.raises(ValueError):
        OperationChain((((2 + 0j, 0j), (0j, 1 + 0j)),), s)              # not unitary
    with pytest.raises(ValueError):
        OperationChain((random_unitary(rng, 3),), s)                    # wrong dimension
    with pytest.raises(ValueError):
        OperationChain((u,), (2 + 0j, 0j))                              # not normalized
    with pytest.raises(ValueError):
        OperationChain((), s)
    chain = OperationChain((u,), s)
    with pytest.raises(ValueError):
        chain.violation_energy((s,))                                    # wrong number of states


def test_unitary_helpers_agree():
    rng = random.Random(9)
    u = random_unitary(rng, 3)
    assert is_unitary(u) and is_unitary(dagger(u))
    v = random_state(rng, 3)
    assert abs(norm(mat_vec(u, v)) - 1) < 1e-12
    p = mat_mul(dagger(u), u)
    assert all(abs(p[i][j] - (i == j)) < 1e-12 for i in range(3) for j in range(3))


def test_every_law_states_validity_and_failure_modes():
    assert {law.name for law in CHAIN_LAWS} == {"violation-energy", "history-state", "propagation-gap"}
    for law in CHAIN_LAWS:
        assert law.validity and law.fails_when
    with pytest.raises(ValueError):
        ChainLaw("x", "s", "f", "v", ())
