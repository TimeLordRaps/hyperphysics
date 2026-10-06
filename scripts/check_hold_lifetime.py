"""Can a finite device hold 'indefinitely'? Survival under repeated independent failure chances.

(1) constant per-step failure probability p: survival (1-p)^n -> 0 (certain eventual failure).
(2) summable failure probabilities p_n = 1/n^2 from n=2: survival -> prod (1 - 1/n^2) = 1/2 exactly.
(3) the de Sitter floor temperature T = hbar H / (2 pi k) for H_Lambda ~ 1.8e-18 per second
    (H0 ~ 2.27e-18 per second times sqrt(Omega_Lambda ~ 0.69), rounded), and the Boltzmann factor
    exp(-DeltaE / kT) of a barrier DeltaE at that floor (standard library only).
"""
import math

HBAR, KB = 1.054571817e-34, 1.380649e-23


def survival_constant(p: float, n: int) -> float:
    return (1.0 - p) ** n


def survival_summable(n_max: int) -> float:
    s = 1.0
    for n in range(2, n_max + 1):
        s *= 1.0 - 1.0 / (n * n)
    return s


if __name__ == "__main__":
    for n in (10**3, 10**6, 10**9):
        print(f"constant p=1e-9, n={n:>10d} steps: survival {survival_constant(1e-9, n):.6f}")
    for n in (10, 10**3, 10**6):
        print(f"p_n=1/n^2, n_max={n:>8d}: survival {survival_summable(n):.9f} (limit 0.5)")
    h_lambda = 1.8e-18
    t_floor = HBAR * h_lambda / (2 * math.pi * KB)
    print(f"de Sitter floor temperature ~ {t_floor:.2e} K")
    for de_over_kt in (10, 100, 1000):
        print(f"barrier DeltaE = {de_over_kt} kT_floor: Boltzmann factor {math.exp(-de_over_kt):.3e} per attempt")
