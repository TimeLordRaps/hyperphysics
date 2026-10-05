"""Interior entangled with an exterior: decoherence of the reduced state, and no-signaling.

Joint system = interior (dimension da) x exterior (dimension db), Hamiltonian diagonal in
the product basis with energies E[a][b]; standard library only. Two cases:
  decoupled: E[a][b] = e[a] + f[b]   (no interaction across the sheet)
  coupled:   E[a][b] generic         (an interaction across the sheet)
Checks, with an entangled initial state c[a][b]:
 1. Coherence: the off-diagonal entry of the reduced interior state always rotates in the
    energy basis, so its Cesaro average is ~0 in BOTH cases and cannot tell them apart. The
    magnitude |rho_in[0][1](t)| can: constant when decoupled (the interior evolves unitarily
    by itself), fluctuating when coupled (coherence exchanged with the exterior).
 2. No-signaling: a unitary V applied to the interior at t=0 leaves the exterior's reduced
    state unchanged at every later time when decoupled, and changes it when coupled.
Exact for diagonal H; shows the mechanism, not any physical sheet.
"""
import cmath
import math
import random

rng = random.Random(20261005)
DA = DB = 2


def rand_state():
    c = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(DB)] for _ in range(DA)]
    n = math.sqrt(sum(abs(x) ** 2 for r in c for x in r))
    return [[x / n for x in r] for r in c]


def evolve(c, E, t):
    return [[c[a][b] * cmath.exp(-1j * E[a][b] * t) for b in range(DB)] for a in range(DA)]


def rho_in(c):
    return [[sum(c[a][b] * c[a2][b].conjugate() for b in range(DB)) for a2 in range(DA)] for a in range(DA)]


def rho_out(c):
    return [[sum(c[a][b] * c[a][b2].conjugate() for a in range(DA)) for b2 in range(DB)] for b in range(DB)]


def apply_interior_unitary(c, theta):
    ct, st = math.cos(theta), math.sin(theta)
    v = [[ct, -st], [st, ct]]
    return [[sum(v[a][k] * c[k][b] for k in range(DA)) for b in range(DB)] for a in range(DA)]


def dist(m, n):
    return max(abs(m[i][j] - n[i][j]) for i in range(len(m)) for j in range(len(m)))


def energies(coupled):
    e = [rng.uniform(0, 6) for _ in range(DA)]
    f = [rng.uniform(0, 6) for _ in range(DB)]
    E = [[e[a] + f[b] for b in range(DB)] for a in range(DA)]
    if coupled:
        E = [[E[a][b] + rng.uniform(0, 6) for b in range(DB)] for a in range(DA)]
    return E


if __name__ == "__main__":
    steps = 20000
    for coupled in (False, True):
        E = energies(coupled)
        c = rand_state()
        r0 = rho_in(c)
        avg = [[0j] * DA for _ in range(DA)]
        for t in range(steps):
            r = rho_in(evolve(c, E, t))
            for i in range(DA):
                for j in range(DA):
                    avg[i][j] += r[i][j] / steps
        off0, offavg = abs(r0[0][1]), abs(avg[0][1])
        mags = [abs(rho_in(evolve(c, E, t))[0][1]) for t in range(0, 2000, 3)]
        spread = max(mags) - min(mags)
        c2 = apply_interior_unitary(c, 0.7)
        worst = max(dist(rho_out(evolve(c, E, t)), rho_out(evolve(c2, E, t))) for t in range(0, 400, 7))
        print(f"coupled={coupled!s:5} |rho_in(0)[0][1]|={off0:.4f} |Cesaro avg[0][1]|={offavg:.4f} "
              f"spread of |rho_in[0][1](t)|={spread:.4f} "
              f"max change of exterior state after interior unitary={worst:.4f}")
