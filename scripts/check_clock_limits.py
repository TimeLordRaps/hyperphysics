"""Numbers behind the time-comb / clock-network limits note (standard library only).

 - Planck time t_P and the Ng-van Dam estimate  dT ~ t_P^(2/3) T^(1/3)  (contested; see the note)
 - fractional gap to the best reported clock systematic uncertainty (5.5e-19, NIST Al+ 2025)
 - statistical improvement N needed at the standard quantum limit (1/sqrt N) and Heisenberg limit (1/N)
 - gravitational redshift per metre of height, and the height resolution a given fractional level needs
 - Margolus-Levitin energy for one operation per Planck time
"""
import math

HBAR, C, G = 1.054571817e-34, 299_792_458.0, 6.67430e-11
T_P = math.sqrt(HBAR * G / C ** 5)
BEST = 5.5e-19  # fractional systematic uncertainty, NIST 27Al+ single-ion clock (reported July 2025)


def ng_van_dam(T: float) -> float:
    return T_P ** (2 / 3) * T ** (1 / 3)


if __name__ == "__main__":
    print(f"Planck time = {T_P:.4e} s")
    for name, T in (("1 s", 1.0), ("1 day", 86400.0), ("1 year", 3.156e7), ("age of universe", 4.35e17)):
        d = ng_van_dam(T)
        frac = d / T
        print(f"T = {name:>15}: Ng-van Dam dT ~ {d:.2e} s, fractional {frac:.2e}; "
              f"gap to best clock = {BEST / frac:.2e}; N at 1/N: {BEST / frac:.2e}; N at 1/sqrt(N): {(BEST / frac) ** 2:.2e}")
    redshift_per_m = G * 5.972e24 / (6.371e6 ** 2) / C ** 2
    print(f"gravitational redshift near Earth's surface: {redshift_per_m:.3e} per metre of height")
    for frac in (BEST, 1e-29):
        print(f"  height resolution for fractional level {frac:.1e}: {frac / redshift_per_m:.2e} m")
    e_ml = math.pi * HBAR / (2 * T_P)
    print(f"Margolus-Levitin energy for one operation per Planck time: {e_ml:.3e} J "
          f"(Planck energy {math.sqrt(HBAR * C ** 5 / G):.3e} J)")
    print(f"optical cycle at 5e14 Hz = {1 / 5e14:.1e} s; ratio to Planck time = {1 / 5e14 / T_P:.2e}")
