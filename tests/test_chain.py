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
    least_violation_states,
    mat_mul,
    mat_vec,
    minimal_violation_energy,
    mismatch,
    norm,
    selector_branches,
    split_cost,
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
    assert {law.name for law in CHAIN_LAWS} == {"violation-energy", "history-state", "propagation-gap", "least-violation"}
    for law in CHAIN_LAWS:
        assert law.validity and law.fails_when
    with pytest.raises(ValueError):
        ChainLaw("x", "s", "f", "v", ())


def test_least_violation_chain_spreads_the_correction_and_hits_both_ends():
    chain, rng = make_chain(11, dim=3, steps=6)
    target = random_state(rng, 3)                       # not reachable by the forced chain
    states = least_violation_states(chain.ops, chain.state0, target)
    assert max(abs(a - b) for a, b in zip(states[0], chain.state0)) < 1e-12
    assert max(abs(a - b) for a, b in zip(states[-1], target)) < 1e-12
    d = mismatch(chain.ops, chain.state0, target)
    assert sum(abs(x) ** 2 for x in d) > 1e-3
    per_step = chain.violations(states)
    assert max(per_step) - min(per_step) < 1e-12        # evenly spread
    assert abs(sum(per_step) - minimal_violation_energy(chain.ops, chain.state0, target)) < 1e-12
    assert abs(per_step[0] - sum(abs(x) ** 2 for x in d) / chain.steps ** 2) < 1e-12


def test_no_other_chain_with_the_same_ends_has_lower_energy_negative_control():
    chain, rng = make_chain(12, dim=2, steps=5)
    target = random_state(rng, 2)
    best = minimal_violation_energy(chain.ops, chain.state0, target)
    states = least_violation_states(chain.ops, chain.state0, target)
    for _ in range(100):
        perturbed = [states[0]] + [tuple(x + complex(rng.gauss(0, 0.05), rng.gauss(0, 0.05)) for x in b)
                                   for b in states[1:-1]] + [states[-1]]
        assert chain.violation_energy(tuple(perturbed)) > best


def test_a_reachable_target_costs_nothing_and_longer_chains_pay_less():
    chain, rng = make_chain(13, dim=2, steps=4)
    reachable = chain.states()[-1]
    assert minimal_violation_energy(chain.ops, chain.state0, reachable) < 1e-24
    target = random_state(rng, 2)
    short = minimal_violation_energy(chain.ops[:2], chain.state0, target)
    # same mismatch magnitude spread over more steps costs proportionally less
    d = sum(abs(x) ** 2 for x in mismatch(chain.ops[:2], chain.state0, target))
    assert abs(short - d / 2) < 1e-12


def test_convex_cost_spreads_and_concave_cost_concentrates():
    assert split_cost(1.0, 10, 2.0, False) < split_cost(1.0, 10, 2.0, True)        # 0.1 vs 1
    assert split_cost(1.0, 10, 0.5, True) < split_cost(1.0, 10, 0.5, False)        # 1 vs sqrt(10)
    assert abs(split_cost(1.0, 10, 1.0, True) - split_cost(1.0, 10, 1.0, False)) < 1e-12
    with pytest.raises(ValueError):
        split_cost(1.0, 0, 2.0, False)
