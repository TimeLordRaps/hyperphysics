# Self-consistency that corrects: least-violation chains, spread corrections and discrete junctions

Owner's statement (USER-STATED, 2026-10-06), recorded verbatim in hyperreality `PROVENANCE.md`: sempiternal meta/hyper laws dictate the self-consistency of base-reality and the possibility-dynamics of preality; possibilities are continuous with discrete junctions that represent unlawful, unobtainable realities; events and matter have possibilities; and if a self-consistency requirement forces it, base-reality self-corrects by creating or erasing matter, even breaking conservation of mass and energy. Tags: `[FORM]` proved or checked, `[FRAME]` holds in a stated model, `[HYPER]` the owner's proposal, `[OPEN]` unresolved.

## A model in which "self-correction" is exact

Take a chain of operations (hyperphysics `chain`): start state `psi_0`, unitary operations `U_1…U_n`. Suppose the boundary conditions are inconsistent with the laws: the end state the world must reach, `target`, is not what the forced chain from `psi_0` produces. Then no chain has zero violation energy. A self-consistency principle that still demands a history picks the chain of **least total violation**, subject to the fixed ends. In the quadratic-cost model:

* `[FORM]` the minimum is `‖Δ‖² / n`, where `Δ = (U_n…U_1)† target − psi_0` is the mismatch pulled back to the start, and the minimizer is `psi_t = U_t…U_1 (psi_0 + (t/n) Δ)`: the correction is **spread evenly**, each step violated by `‖Δ‖/n`, so the total falls as `1/n` (`least_violation_states`, `minimal_violation_energy`, tested: both ends reached, all step violations equal, no perturbation of the intermediate states lowers the energy, a reachable target costs `0`).
* The reading: a requirement that cannot be met lawfully is met by a *tiny* violation at every step instead of one large one. In a long enough chain the violation per step is far below any detectable level, which is how an exact conservation law could hold to every experiment and still be corrected at a level no experiment sees. `[FRAME]`

## Continuous spread and discrete junction are two cost functions

`split_cost` gives the cost of a total correction `D` split over `n` steps: `n (D/n)^p` evenly or `D^p` in one step. For `p = 2` spreading is cheaper (`0.1` against `1` for `D = 1`, `n = 10`); for `p = 1` the two are equal; for `p = 1/2` one concentrated step is cheaper (`1` against `√10`). So the same self-consistency requirement gives a **continuous** correction under a convex cost and a **discrete junction** (all of the violation at one place) under a concave cost. That is a precise way to get "possibilities are continuous with discrete junctions" without adding anything: the junctions are where the least-cost correction sits when the cost of violating is concave. `[FORM]` for the arithmetic, `[HYPER]` that a concave cost is the right one.

## What this does and does not support

* It supports the *form* of the owner's picture: a meta-level requirement (consistency of ends) acting through the cheapest violation of lower-level rules, with the lower-level rules (here, the operations, standing in for conservation) holding almost everywhere.
* It does **not** show that base-reality does this. The standing physical record is that conservation of energy and of charge holds to extreme precision (for instance, searches for electron decay set lifetime limits above `10²⁸` years, *recalled*, not retrieved here), so any such correction must be below those bounds. The `1/n` dilution is compatible with that, and so is the absence of any correction, and nothing here distinguishes them.
* The cost function is an assumption, and a norm constraint on intermediate states (physical states are normalized) raises the minimum: this was checked only for unconstrained intermediate states. `[OPEN]`
* "Self-consistency forces creation or erasure of matter" is the same as asserting the target boundary is forced and the lower laws are soft. A different choice, soft boundary and hard laws, gives the standard answer: no violation, and an inconsistent history is simply not realized. Which one the meta-law is, is the substantive question. `[OPEN]`

## Open

* `[OPEN]` Hard laws with soft boundaries (standard consistency, no violation) or hard boundaries with soft laws (correction); and the cost function.
* `[OPEN]` Whether the discrete junctions are concave-cost minima or something else.
* `[OPEN]` Whether the dilution with chain length gives an experimentally distinguishable signature or is unobservable by construction.
