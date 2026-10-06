"""A computation with no time of its own: Kitaev history state / Page-Wootters clock (standard library).

A one-qubit system S is entangled with a clock register C with levels t = 0..T. The propagation
Hamiltonian H = sum_{t=1..T} ( |t><t| + |t-1><t-1| ) (x) 1 - |t><t-1| (x) U_t - |t-1><t| (x) U_t^dagger
has the history state |h> = (T+1)^(-1/2) sum_t |t> (x) U_t...U_1 |psi0> as a zero-energy state, so |h> is
stationary (no global time evolution), yet the system state conditioned on clock reading t is the t-th
step of the computation. Checks: (1) H h = 0; (2) conditioning on t gives U_t...U_1 psi0; (3) tampering
with one gate in H (negative control) makes H h != 0; (4) a reconfiguration of one gate yields a different
history state, and the overlap with the old one is reported.
"""
import cmath
import math
import random

rng = random.Random(20261006)
T = 5


def rand_unitary():
    a, b, c = (rng.uniform(0, 2 * math.pi) for _ in range(3))
    return [[math.cos(a) * cmath.exp(1j * b), -math.sin(a) * cmath.exp(1j * c)],
            [math.sin(a) * cmath.exp(-1j * c), math.cos(a) * cmath.exp(-1j * b)]]


def mv(m, v):
    return [m[0][0] * v[0] + m[0][1] * v[1], m[1][0] * v[0] + m[1][1] * v[1]]


def dag(m):
    return [[m[0][0].conjugate(), m[1][0].conjugate()], [m[0][1].conjugate(), m[1][1].conjugate()]]


def history(gates, psi0):
    blocks = [psi0]
    for u in gates:
        blocks.append(mv(u, blocks[-1]))
    s = 1 / math.sqrt(len(blocks))
    return [[x * s for x in b] for b in blocks]


def apply_h(gates, psi):
    out = []
    for s in range(T + 1):
        diag = (1 if s > 0 else 0) + (1 if s < T else 0)
        v = [diag * x for x in psi[s]]
        if s > 0:
            w = mv(gates[s - 1], psi[s - 1])
            v = [a - b for a, b in zip(v, w)]
        if s < T:
            w = mv(dag(gates[s]), psi[s + 1])
            v = [a - b for a, b in zip(v, w)]
        out.append(v)
    return out


def norm(psi):
    return math.sqrt(sum(abs(x) ** 2 for b in psi for x in b))


if __name__ == "__main__":
    gates = [rand_unitary() for _ in range(T)]
    psi0 = [1 + 0j, 0j]
    h = history(gates, psi0)
    print(f"(1) norm of H h = {norm(apply_h(gates, h)):.2e}   (norm of h = {norm(h):.6f})")
    ref = psi0
    worst = 0.0
    for t in range(T + 1):
        cond = [x * math.sqrt(T + 1) for x in h[t]]
        worst = max(worst, max(abs(a - b) for a, b in zip(cond, ref)))
        if t < T:
            ref = mv(gates[t], ref)
    print(f"(2) conditional state at each clock reading vs U_t..U_1 psi0: max difference {worst:.2e}")
    tampered = list(gates)
    tampered[2] = rand_unitary()
    print(f"(3) negative control, one gate in H replaced: norm of H' h = {norm(apply_h(tampered, h)):.3f}")
    h2 = history(tampered, psi0)
    print(f"(4) reconfigured computation: norm of H' h' = {norm(apply_h(tampered, h2)):.2e}; "
          f"overlap |<h|h'>| = {abs(sum(a.conjugate() * b for u, v in zip(h, h2) for a, b in zip(u, v))):.4f}")
