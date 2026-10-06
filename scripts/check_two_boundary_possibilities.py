"""Two-boundary possibilities, and possibilities as sectors versus superpositions (standard library only).

(A) Time-symmetric intermediate probabilities (Aharonov-Bergmann-Lebowitz rule). Pre-select |psi>,
    post-select |phi>, intermediate projective measurement with projectors P_k:
        P(k) = |<phi|P_k|psi>|^2 / sum_j |<phi|P_j|psi>|^2          (after an overall evolution U).
    Reversing the roles (pre = phi, post = psi, evolution U^dagger) gives the same probabilities,
    and the probabilities depend on the LATER boundary: changing |phi> changes them.
(B) A law register L (two laws) correlated with a system S (one qubit, real amplitudes only).
    cq state  = (|0><0| (x) |+><+| + |1><1| (x) |-><-|)/2   (the law label is superselected: no coherence
                between laws);  entangled = (|0>|+> + |1>|->)/sqrt 2  (the law register is coherent).
    Both give the SAME reduced state on S, but only the coherent one has a negative partial-transpose
    eigenvalue (entanglement). So "possibilities that do not interfere" are correlated, not entangled.
"""
import math

R2 = math.sqrt(2.0)


def inner(a, b):
    return sum(x.conjugate() * y for x, y in zip(a, b))


def mv(m, v):
    return [sum(m[i][k] * v[k] for k in range(len(v))) for i in range(len(m))]


def dag(m):
    n = len(m)
    return [[m[j][i].conjugate() for j in range(n)] for i in range(n)]


def abl(U, psi, phi, projectors):
    """Intermediate-outcome probabilities between pre-selection psi and post-selection phi, with the
    intermediate measurement taken after the first half of the evolution (here U is the half step)."""
    amps = [inner(phi, mv(U, mv(p, mv(U, psi)))) for p in projectors]
    weights = [abs(a) ** 2 for a in amps]
    total = sum(weights)
    return [w / total for w in weights] if total > 1e-15 else None


def joint(U, psi, basis, projectors):
    """Joint probability of intermediate outcome k and post-selected outcome m (complete basis)."""
    return [[abs(inner(phi, mv(U, mv(p, mv(U, psi))))) ** 2 for p in projectors] for phi in basis]


def forward_born(U, psi, projectors):
    """Ordinary one-boundary probability of the intermediate outcome: no post-selection."""
    return [sum(abs(x) ** 2 for x in mv(p, mv(U, psi))) for p in projectors]


def jacobi_min_eigenvalue(a, sweeps=60):
    n = len(a)
    a = [row[:] for row in a]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-24:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-18:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1 if theta >= 0 else -1) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
    return min(a[i][i] for i in range(n))


def outer(u, v):
    return [[x * y for y in v] for x in u]


def kron(a, b):
    return [[a[i // 2][j // 2] * b[i % 2][j % 2] for j in range(4)] for i in range(4)]


def partial_transpose_second(m):
    out = [[0.0] * 4 for _ in range(4)]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    out[2 * i + k][2 * j + l] = m[2 * i + l][2 * j + k]
    return out


def reduced_second(m):
    return [[sum(m[2 * a + i][2 * a + j] for a in range(2)) for j in range(2)] for i in range(2)]


def states():
    plus, minus = [1 / R2, 1 / R2], [1 / R2, -1 / R2]
    zero, one = [1.0, 0.0], [0.0, 1.0]
    cq = [[0.5 * (kron(outer(zero, zero), outer(plus, plus))[i][j]
                  + kron(outer(one, one), outer(minus, minus))[i][j]) for j in range(4)] for i in range(4)]
    vec = [(zero[a] * plus[b] + one[a] * minus[b]) / R2 for a in range(2) for b in range(2)]
    ent = outer(vec, vec)
    return cq, ent


if __name__ == "__main__":
    import cmath
    th = 0.9
    U = [[math.cos(th) + 0j, -math.sin(th) + 0j], [math.sin(th) + 0j, math.cos(th) + 0j]]
    P = [[[1 + 0j, 0j], [0j, 0j]], [[0j, 0j], [0j, 1 + 0j]]]
    psi = [1 + 0j, 0j]
    for name, phi in (("phi=|0>", [1 + 0j, 0j]), ("phi=|1>", [0j, 1 + 0j]),
                      ("phi=|+>", [1 / R2 + 0j, 1 / R2 + 0j])):
        fwd = abl(U, psi, phi, P)
        rev = abl(dag(U), phi, psi, P)
        print(f"(A) {name}: forward P = {[round(x, 6) for x in fwd]}  reversed P = {[round(x, 6) for x in rev]}")
    basis = [[1 + 0j, 0j], [0j, 1 + 0j]]
    j = joint(U, psi, basis, P)
    marginal = [sum(j[m][k] for m in range(2)) for k in range(2)]
    print(f"(A2) forward one-boundary P = {[round(x, 6) for x in forward_born(U, psi, P)]}; "
          f"marginal of the two-boundary joint over the later outcome = {[round(x, 6) for x in marginal]}")
    cq, ent = states()
    print("(B) reduced state on S, cq:", [[round(x, 4) for x in r] for r in reduced_second(cq)])
    print("                     entangled:", [[round(x, 4) for x in r] for r in reduced_second(ent)])
    print(f"    min eigenvalue of partial transpose: cq {jacobi_min_eigenvalue(partial_transpose_second(cq)):+.4f}, "
          f"entangled {jacobi_min_eigenvalue(partial_transpose_second(ent)):+.4f}")
