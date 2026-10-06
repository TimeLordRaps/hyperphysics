"""Thermofield-double toy: which time evolutions freeze the two-sided state (standard library only).

|TFD> = sum_E a_E |E>_L |E>_R with a_E proportional to exp(-beta E / 2). Evolving the left side for
t_L and the right for t_R multiplies each term by exp(-i E (t_L + t_R)), so only t_L + t_R matters.
t_R = -t_L (the boost, H_R - H_L) leaves the state exactly unchanged: a frozen time component.
t_R = +t_L (the evolution that grows the bridge in the holographic picture) changes it; the overlap
with the start is a spectral form factor and returns only at the recurrence time.
Also prints the scale M ~ b c^2 / G for a throat of radius b (Morris-Thorne order of magnitude).
"""
import cmath
import math
import random

rng = random.Random(20261006)
D, BETA = 6, 1.0
ENERGIES = [rng.uniform(0.0, 3.0) for _ in range(D)]
W = [math.exp(-BETA * e / 2) for e in ENERGIES]
NORM = math.sqrt(sum(w * w for w in W))
A = [w / NORM for w in W]


def overlap(t_l: float, t_r: float) -> float:
    return abs(sum(a * a * cmath.exp(-1j * e * (t_l + t_r)) for a, e in zip(A, ENERGIES)))


if __name__ == "__main__":
    for t in (0.5, 2.0, 10.0, 100.0):
        print(f"t={t:>6}: overlap(t_L=t, t_R=-t) = {overlap(t, -t):.12f}   "
              f"overlap(t_L=t, t_R=+t) = {overlap(t, t):.4f}")
    c, g = 299_792_458.0, 6.67430e-11
    for name, b in (("Planck length", 1.616e-35), ("proton radius", 8.4e-16),
                    ("1 micrometre", 1e-6), ("1 metre", 1.0)):
        print(f"throat radius b = {name:>14} ({b:.3g} m): M ~ b c^2/G = {b * c * c / g:.3e} kg")
