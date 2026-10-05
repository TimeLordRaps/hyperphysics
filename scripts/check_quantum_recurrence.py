"""Finite-dimensional unitary evolution: Cesaro limit and eps-recurrence (standard library only).

For a random non-degenerate spectrum:
 1. the time average of rho(t) tends to the diagonal ensemble sum_E P_E rho P_E; the
    off-diagonal entries of the average fall like 1/steps (mean ergodic theorem for a
    unitary on a finite-dimensional space; this is the limit-stage value of an interior
    run for omega steps under a Cesaro rule);
 2. the first eps-return step of |<psi|psi(t)>| > 1 - eps grows with dimension d
    (empirical scaling on random spectra, heuristic eps^-(d-1); not a theorem for every
    Hamiltonian).
"""
import cmath
import math
import random

rng = random.Random(20261005)


def random_state(d):
    v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d)]
    n = math.sqrt(sum(abs(x) ** 2 for x in v))
    return [x / n for x in v]


def offdiag_of_average(d: int, steps: int) -> float:
    energies = [rng.uniform(0, 2 * math.pi) for _ in range(d)]
    psi = random_state(d)
    worst = 0.0
    for i in range(d):
        for j in range(i + 1, d):
            w = energies[i] - energies[j]
            acc = sum(cmath.exp(-1j * w * t) for t in range(steps)) / steps
            worst = max(worst, abs(psi[i] * psi[j].conjugate() * acc))
    return worst


def first_return(d: int, eps: float, limit: int = 600_000) -> int:
    energies = [rng.uniform(0, 2 * math.pi) for _ in range(d)]
    p = [abs(x) ** 2 for x in random_state(d)]
    for t in range(1, limit):
        if abs(sum(pk * cmath.exp(-1j * e * t) for pk, e in zip(p, energies))) > 1 - eps:
            return t
    return -1


if __name__ == "__main__":
    for steps in (10**2, 10**3, 10**4):
        print(f"d=4 steps={steps:>6d} max off-diagonal of Cesaro average = {offdiag_of_average(4, steps):.3e}")
    for d in (2, 3, 4, 5):
        times = sorted(first_return(d, 0.1) for _ in range(7))
        print(f"d={d} eps=0.1 first-return step, 7 draws sorted (-1 = none within 600000): {times}")
