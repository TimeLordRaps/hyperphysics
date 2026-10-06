"""Gates for the finite models in scripts/ behind docs/research/TIME_BUBBLE_SHEET.md and TIME_COMB_LIMITS.md.

Each script is a toy or an arithmetic check, not a claim about any physical sheet; these tests pin what
each toy establishes, with negative controls, so a regression in the scripts is caught. Standard library only
(the Ponzano-Regge check needs sympy and is skipped without it).
"""
from __future__ import annotations

import importlib
import math
import random
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load(name):
    return importlib.import_module(name)


def test_history_state_is_stationary_and_conditions_to_the_computation():
    m = load("check_history_state_clock")
    m.rng = random.Random(1)
    gates = [m.rand_unitary() for _ in range(m.T)]
    psi0 = [1 + 0j, 0j]
    h = m.history(gates, psi0)
    assert m.norm(m.apply_h(gates, h)) < 1e-12
    ref = psi0
    for t in range(m.T + 1):
        cond = [x * math.sqrt(m.T + 1) for x in h[t]]
        assert max(abs(a - b) for a, b in zip(cond, ref)) < 1e-12
        if t < m.T:
            ref = m.mv(gates[t], ref)


def test_tampering_with_a_gate_breaks_stationarity_negative_control():
    m = load("check_history_state_clock")
    m.rng = random.Random(2)
    gates = [m.rand_unitary() for _ in range(m.T)]
    h = m.history(gates, [1 + 0j, 0j])
    tampered = list(gates)
    tampered[2] = m.rand_unitary()
    assert m.norm(m.apply_h(tampered, h)) > 0.1
    h2 = m.history(tampered, [1 + 0j, 0j])
    assert m.norm(m.apply_h(tampered, h2)) < 1e-12
    overlap = abs(sum(a.conjugate() * b for u, v in zip(h, h2) for a, b in zip(u, v)))
    assert overlap < 0.99


def test_energy_is_total_squared_violation_of_steps():
    m = load("check_derivation_energy")
    m.rng = random.Random(3)
    gates = [m.c.rand_unitary() for _ in range(m.T)]
    for _ in range(100):
        psi = [m.rand_block() for _ in range(m.T + 1)]
        assert abs(m.energy(gates, psi) - m.violations(gates, psi)) < 1e-12
    chain = m.valid_chain(gates, m.rand_block())
    assert abs(m.energy(gates, chain)) < 1e-12
    broken = [list(b) for b in chain]
    broken[3] = m.rand_block()
    assert m.energy(gates, broken) > 1e-3


def test_two_sided_state_is_frozen_only_by_the_opposite_evolution():
    m = load("check_tfd_frozen_time")
    for t in (0.5, 2.0, 10.0, 100.0):
        assert abs(m.overlap(t, -t) - 1.0) < 1e-12
    assert m.overlap(2.0, 2.0) < 0.95  # the same-direction evolution does change it


def test_gap_of_the_propagation_hamiltonian_and_readout_probability():
    m = load("check_instant_computation_cost")
    for T in (5, 20):
        lam, resid = m.gap_eigenvector_residual(T)
        assert resid < 1e-12
        assert abs(lam - (2 - 2 * math.cos(math.pi / (T + 1)))) < 1e-15
        assert abs(lam - math.pi ** 2 / (T + 1) ** 2) / lam < 0.05


def test_entanglement_alone_carries_nothing_and_coupling_does():
    m = load("check_entangled_interior")

    def run(coupled, seed):
        m.rng = random.Random(seed)
        E = m.energies(coupled)
        c = m.rand_state()
        c2 = m.apply_interior_unitary(c, 0.7)
        change = max(m.dist(m.rho_out(m.evolve(c, E, t)), m.rho_out(m.evolve(c2, E, t))) for t in range(0, 400, 7))
        mags = [abs(m.rho_in(m.evolve(c, E, t))[0][1]) for t in range(0, 2000, 3)]
        return change, max(mags) - min(mags)

    change_off, spread_off = run(False, 4)
    change_on, spread_on = run(True, 4)
    assert change_off < 1e-12 and spread_off < 1e-9
    assert change_on > 0.05 and spread_on > 0.01


def test_timeless_part_is_populations_and_degenerate_coherence():
    m = load("check_timeless_memory")
    rho0 = [[m.C[i] * m.C[j].conjugate() for j in range(4)] for i in range(4)]
    avg = m.averaged_rho(4000)
    assert max(abs(avg[i][i] - rho0[i][i]) for i in range(4)) < 1e-11
    assert abs(avg[0][1] - rho0[0][1]) < 1e-11            # degenerate pair keeps its coherence
    assert max(abs(avg[i][j]) for i, j in ((0, 2), (0, 3), (1, 2), (1, 3), (2, 3))) < 5e-3


def test_cesaro_off_diagonals_shrink_with_steps():
    m = load("check_quantum_recurrence")
    m.rng = random.Random(5)
    small, large = m.offdiag_of_average(4, 100), m.offdiag_of_average(4, 10000)
    assert large < small


def test_hold_lifetime_arithmetic():
    m = load("check_hold_lifetime")
    assert abs(m.survival_constant(1e-9, 10 ** 9) - math.exp(-1)) < 1e-6
    assert abs(m.survival_summable(10 ** 6) - 0.5) < 1e-5
    assert m.survival_constant(1e-9, 10 ** 3) > m.survival_constant(1e-9, 10 ** 9)


def test_clock_limit_numbers():
    m = load("check_clock_limits")
    assert abs(m.T_P - 5.391e-44) / 5.391e-44 < 1e-3
    assert abs(m.ng_van_dam(1.0) - 1.43e-29) / 1.43e-29 < 0.02
    assert m.ng_van_dam(1.0) > m.T_P
    assert m.ng_van_dam(10 ** 3) / 10 ** 3 < m.ng_van_dam(1.0) / 1.0  # fractional bound improves with T


def test_ponzano_regge_asymptotics_match_when_sympy_is_available():
    pytest.importorskip("sympy")
    m = load("check_ponzano_regge_6j")
    from sympy.physics.wigner import wigner_6j
    for j in (20, 40):
        exact = float(wigner_6j(j, j, j, j, j, j))
        assert abs(exact - m.asymptotic(j)) / abs(exact) < 2e-3


def _setup_two_boundary():
    m = load("check_two_boundary_possibilities")
    th = 0.9
    U = [[math.cos(th) + 0j, -math.sin(th) + 0j], [math.sin(th) + 0j, math.cos(th) + 0j]]
    P = [[[1 + 0j, 0j], [0j, 0j]], [[0j, 0j], [0j, 1 + 0j]]]
    return m, U, P, [1 + 0j, 0j]


def test_two_boundary_probabilities_are_time_symmetric_and_depend_on_the_later_boundary():
    m, U, P, psi = _setup_two_boundary()
    outcomes = []
    for phi in ([1 + 0j, 0j], [0j, 1 + 0j], [1 / m.R2 + 0j, 1 / m.R2 + 0j]):
        fwd, rev = m.abl(U, psi, phi, P), m.abl(m.dag(U), phi, psi, P)
        assert max(abs(a - b) for a, b in zip(fwd, rev)) < 1e-12
        outcomes.append(fwd)
    assert max(abs(outcomes[0][0] - outcomes[2][0]), abs(outcomes[0][0] - outcomes[1][0])) > 0.2


def test_the_forward_description_is_the_marginal_of_the_two_boundary_one():
    m, U, P, psi = _setup_two_boundary()
    basis = [[1 + 0j, 0j], [0j, 1 + 0j]]
    j = m.joint(U, psi, basis, P)
    marginal = [sum(j[b][k] for b in range(2)) for k in range(2)]
    assert max(abs(a - b) for a, b in zip(marginal, m.forward_born(U, psi, P))) < 1e-12
    assert abs(sum(sum(r) for r in j) - 1.0) < 1e-12


def test_superselected_possibilities_are_correlated_but_not_entangled():
    m = load("check_two_boundary_possibilities")
    cq, ent = m.states()
    red_cq, red_ent = m.reduced_second(cq), m.reduced_second(ent)
    assert max(abs(red_cq[i][j] - red_ent[i][j]) for i in range(2) for j in range(2)) < 1e-12
    assert m.jacobi_min_eigenvalue(m.partial_transpose_second(cq)) > -1e-9      # separable
    assert m.jacobi_min_eigenvalue(m.partial_transpose_second(ent)) < -0.4      # entangled
