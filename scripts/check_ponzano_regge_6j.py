"""Ponzano-Regge check: exact SU(2) 6j of a regular tetrahedron vs its asymptotic form.

Asymptotic: {6j} ~ cos(S + pi/4) / sqrt(12 pi V), with a = j + 1/2 (dimensionless),
V = a^3 / (6 sqrt 2), S = 6 a theta and theta the EXTERIOR dihedral angle
pi - arccos(1/3). One toy (3D Euclidean, regular tetrahedron); not the 4D EPRL case.
Needs sympy (not a hyperphysics dependency): `python scripts/check_ponzano_regge_6j.py`.
"""
import math

from sympy.physics.wigner import wigner_6j


def asymptotic(j: int) -> float:
    a = j + 0.5
    volume = a**3 / (6 * math.sqrt(2))
    action = 6 * a * (math.pi - math.acos(1 / 3))
    return math.cos(action + math.pi / 4) / math.sqrt(12 * math.pi * volume)


if __name__ == "__main__":
    for j in (5, 20, 40, 80):
        exact = float(wigner_6j(j, j, j, j, j, j))
        approx = asymptotic(j)
        print(f"j={j:3d} exact={exact:+.4e} asymptotic={approx:+.4e} "
              f"relative_error={abs(exact - approx) / abs(exact):.2e}")
