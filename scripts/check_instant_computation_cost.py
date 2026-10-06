"""Where the time goes when a computation is a frozen history state (standard library only).

Reuses the history-state construction of check_history_state_clock.py (run from the scripts/ directory). Checks:
 (1) the spectral gap of the propagation Hamiltonian is 2 - 2 cos(pi/(T+1)) ~ pi^2/(T+1)^2,
     shown by an explicit eigenvector (gauge-transformed cosine) with residual ~ 0;
 (2) reading the answer: the clock is found at the last step with probability 1/(T+1), and
     padding with T idle (identity) steps raises it to (T+1)/(2T+1) ~ 1/2, at twice the clock length.
"""
import math

from check_history_state_clock import T as T_DEFAULT
from check_history_state_clock import apply_h, history, mv, norm, rand_unitary


def gap_eigenvector_residual(T: int) -> tuple:
    gates = [rand_unitary() for _ in range(T)]
    phi = [0.6 + 0j, 0.8j]
    blocks = [phi]
    for u in gates:
        blocks.append(mv(u, blocks[-1]))
    lam = 2 - 2 * math.cos(math.pi / (T + 1))
    v = [math.cos(math.pi * (t + 0.5) / (T + 1)) for t in range(T + 1)]
    psi = [[v[t] * x for x in blocks[t]] for t in range(T + 1)]
    import check_history_state_clock as c
    saved = c.T
    c.T = T
    try:
        hpsi = apply_h(gates, psi)
    finally:
        c.T = saved
    resid = math.sqrt(sum(abs(a - lam * b) ** 2 for hb, pb in zip(hpsi, psi) for a, b in zip(hb, pb)))
    return lam, resid / norm(psi)


if __name__ == "__main__":
    for T in (5, 20, 80):
        lam, res = gap_eigenvector_residual(T)
        print(f"T={T:>3}: gap = {lam:.6f}  pi^2/(T+1)^2 = {math.pi ** 2 / (T + 1) ** 2:.6f}  "
              f"eigenvector residual = {res:.1e}  (1/gap = {1 / lam:.1f} ~ T^2 scale)")
    for T in (5, 20, 80):
        print(f"T={T:>3}: P(clock at last step) = {1 / (T + 1):.4f};  with {T} idle steps appended: "
              f"{(T + 1) / (2 * T + 1):.4f} (clock length {T + 1} -> {2 * T + 1})")
