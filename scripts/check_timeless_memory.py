"""Which parts of a finite quantum interior's state survive infinite time (standard library only).

The Cesaro (time-average) limit of a finite-dimensional unitary evolution is the conditional
expectation onto the stationary sector: sum_E P_E rho P_E over the ENERGY EIGENSPACES.
So the information that is "timeless" under the time-average rule is (a) the level populations
and (b) any coherence between states inside a DEGENERATE eigenspace; coherence between
different energies averages away (like 1/steps). Checked for H = diag(0, 0, 1.3, 2.9):
levels 0 and 1 are degenerate.
"""
import cmath
import math

E = [0.0, 0.0, 1.3, 2.9]
C = [complex(0.5, 0.2), complex(0.3, -0.4), complex(0.4, 0.1), complex(0.35, 0.3)]
norm = math.sqrt(sum(abs(x) ** 2 for x in C))
C = [x / norm for x in C]


def averaged_rho(steps: int):
    d = len(C)
    acc = [[0j] * d for _ in range(d)]
    for t in range(steps):
        psi = [C[k] * cmath.exp(-1j * E[k] * t) for k in range(d)]
        for i in range(d):
            for j in range(d):
                acc[i][j] += psi[i] * psi[j].conjugate() / steps
    return acc


if __name__ == "__main__":
    rho0 = [[C[i] * C[j].conjugate() for j in range(4)] for i in range(4)]
    for steps in (100, 1000, 10000):
        avg = averaged_rho(steps)
        pop_err = max(abs(avg[i][i] - rho0[i][i]) for i in range(4))
        degen_err = abs(avg[0][1] - rho0[0][1])
        cross = max(abs(avg[i][j]) for i, j in ((0, 2), (0, 3), (1, 2), (1, 3), (2, 3)))
        print(f"steps={steps:>6d} populations error={pop_err:.1e} "
              f"degenerate-pair coherence error={degen_err:.1e} "
              f"largest cross-energy coherence={cross:.1e}")
    p = [abs(x) ** 2 for x in C]
    print("populations (the timeless classical part):", [round(x, 4) for x in p])
    print("Shannon entropy of populations (nats):", round(-sum(x * math.log(x) for x in p), 4),
          "<= log d =", round(math.log(4), 4))
