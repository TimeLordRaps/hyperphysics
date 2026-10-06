"""A frozen computation as a derivation chain: energy = total violation of derivation steps.

For the propagation Hamiltonian H of check_history_state_clock.py and ANY clock-system state
psi = (psi_0, ..., psi_T):   <psi|H|psi> = sum_t || psi_t - U_t psi_{t-1} ||^2.
So H is a sum of squares of local step violations: it vanishes exactly on chains in which every step is
valid (each psi_t is what rule U_t derives from psi_{t-1}), and such a chain is fixed by psi_0 alone
(derivation is directional). Checks on random chains, standard library only:
 (1) the identity <psi|H|psi> = sum of squared step violations (random, non-valid chains);
 (2) a valid chain has energy 0; breaking exactly one step gives energy = that step's violation;
 (3) different psi_0 give different valid chains (that a valid chain is fixed by psi_0 is the proof,
     not this run: w_t = 0 for all t forces psi_t = U_t psi_{t-1}).
"""
import math
import random

import check_history_state_clock as c

rng = random.Random(20261006)
T = c.T


def rand_block():
    v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(2)]
    n = math.sqrt(sum(abs(x) ** 2 for x in v))
    return [x / n for x in v]


def energy(gates, psi):
    hpsi = c.apply_h(gates, psi)
    return sum((a.conjugate() * b).real for pb, hb in zip(psi, hpsi) for a, b in zip(pb, hb))


def violations(gates, psi):
    return sum(sum(abs(psi[t][k] - c.mv(gates[t - 1], psi[t - 1])[k]) ** 2 for k in range(2))
               for t in range(1, T + 1))


def valid_chain(gates, psi0):
    blocks = [psi0]
    for u in gates:
        blocks.append(c.mv(u, blocks[-1]))
    return blocks


if __name__ == "__main__":
    gates = [c.rand_unitary() for _ in range(T)]
    worst = 0.0
    for _ in range(200):
        psi = [rand_block() for _ in range(T + 1)]
        worst = max(worst, abs(energy(gates, psi) - violations(gates, psi)))
    print(f"(1) random chains: max |<H> - sum of squared step violations| = {worst:.2e}")
    chain = valid_chain(gates, rand_block())
    print(f"(2) valid chain: energy {energy(gates, chain):.2e}")
    broken = [list(b) for b in chain]
    broken[3] = rand_block()   # breaks step 3 (into psi_3) and step 4 (out of psi_3)
    print(f"    chain with psi_3 replaced: energy {energy(gates, broken):.4f} "
          f"= violations {violations(gates, broken):.4f}")
    a = valid_chain(gates, [1 + 0j, 0j])
    d = max(abs(x - y) for p, q in zip(a, valid_chain(gates, [0j, 1 + 0j])) for x, y in zip(p, q))
    print(f"(3) valid chains from different psi_0 differ by up to {d:.3f}")
