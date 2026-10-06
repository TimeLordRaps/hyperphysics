"""Anomaly cancellation for one Standard Model generation, in exact fractions (standard library only).

Left-handed Weyl fermions of one generation, as (name, colour multiplicity, isospin multiplicity, hypercharge Y):
  Q (3, 2, 1/6), u^c (3, 1, -2/3), d^c (3, 1, 1/3), L (1, 2, -1/2), e^c (1, 1, 1).
Consistency of the gauge theory requires these sums to vanish:
  Y^3 (cubic hypercharge), Y (mixed gravitational), SU(2)^2 Y (sum of Y over isospin doublets, weighted by
  colour), SU(3)^2 Y (sum of Y over colour triplets, weighted by isospin multiplicity).
Check: all four vanish for the standard assignment; with ONE colour instead of three the cubic sum is 1/2.
"""
from fractions import Fraction as F

GENERATION = (("Q", 3, 2, F(1, 6)), ("u^c", 3, 1, F(-2, 3)), ("d^c", 3, 1, F(1, 3)),
              ("L", 1, 2, F(-1, 2)), ("e^c", 1, 1, F(1)))


def anomaly_sums(fields, colours=3):
    def n(c):  # colour multiplicity, with the triplets replaced by `colours`
        return colours if c == 3 else c
    y3 = sum(n(c) * i * y ** 3 for _, c, i, y in fields)
    y1 = sum(n(c) * i * y for _, c, i, y in fields)
    su2_su2_y = sum(n(c) * y for _, c, i, y in fields if i == 2)
    su3_su3_y = sum(i * y for _, c, i, y in fields if c == 3)
    return {"Y^3": y3, "Y": y1, "SU(2)^2 Y": su2_su2_y, "SU(3)^2 Y": su3_su3_y}


if __name__ == "__main__":
    print("standard (3 colours):", {k: str(v) for k, v in anomaly_sums(GENERATION).items()})
    print("one colour:          ", {k: str(v) for k, v in anomaly_sums(GENERATION, colours=1).items()})
    without_e = tuple(f for f in GENERATION if f[0] != "e^c")
    print("without e^c:         ", {k: str(v) for k, v in anomaly_sums(without_e).items()})
