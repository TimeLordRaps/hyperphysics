# The time-bubble sheet: what physics allows, and what the family already holds

Owner's proposal (USER-STATED, 2026-10-05): oreality can be represented by arealities in prealities in infinite-time finite spaces; a time bubble whose boundary is a sheet of infinitesimally thin singularities, like a bubble's film, lets a finite space exist infinitely long inside itself and lets computational information cross the sheet. `[HYPER]` Retrieved 2026-10-05 unless marked *recalled*.

## Four distinct claims inside it

1. **The film is a singularity.** In general relativity a thin shell is not one. The Israel (Darmois–Israel) junction conditions keep the metric continuous across the shell and let the extrinsic curvature jump; the jump equals the shell's surface stress-energy (Lanczos equation) ([overview](https://www.emergentmind.com/topics/darmois-israel-junction-formalism)). Curvature is a delta function, finite surface energy, and geodesics cross it. A genuine singular sheet, with divergent curvature and a degenerate metric, would not carry a signal through at all. So "sheet" should mean a regular thin shell, or a horizon. `[FORM]` for the first; the rest is the proposal.
2. **Finite space, infinite time.** The real instance is the de Sitter static patch: a horizon of finite area, so finitely many states, and unbounded static time (*recalled*; Poincaré recurrence time of order `e^S`). Bounds: Bekenstein `S ≤ 2πER/(ħc)`; covariant (Bousso) bound, entropy on a non-expanding light sheet of a surface is at most a quarter of its area ([entropy bounds](https://arxiv.org/pdf/hep-th/0203101), [Bousso](https://arxiv.org/abs/1404.5635)). Finite states plus infinite time gives recurrence, not new computation: the finite-state verdict of `wiki/hypersphere-and-preality.md`. `[FORM]`
3. **Infinite interior time against finite exterior time.** Redshift cannot supply it. A clock deeper in a potential runs slower than one outside, so a shell with a flat interior has interior time elapsing *less*. The needed asymmetry has to come from causal structure: the exterior's time ends or is cut off (pinch-off, horizon) while the interior goes on. That is a baby universe, a small throat to a large inflating interior (Frolov–Markov–Mukhanov, Farhi–Guth, *recalled*), with no return. `[FRAME]`
4. **"Arrive right after we left."** This needs the interior's infinite history to be readable at one exterior event. Two models, with different strength:
   * Malament–Hogarth (MH) spacetimes: an event whose past contains a worldline of infinite elapsed time, so an observer can receive the outcome of an infinite computation in finite time ([SEP, Supertasks](https://plato.stanford.edu/entries/spacetime-supertasks/)). Etesi and Németi analysed a subclass containing rotating (Kerr) black holes and showed relations beyond Turing computability can be decided ([paper](https://arxiv.org/pdf/gr-qc/0104023)). Whether physically realizable (stability, signal strength) is contested. This is the mechanism for "translating information across the sheet": the receiver crosses at the MH event.
   * Closed timelike curves: polynomial-size CTC computers have exactly the power of PSPACE, classical or quantum ([Aaronson–Watrous](https://arxiv.org/abs/0808.2669)). That is "arrive before you left" but not infinite-time power.

So the infinite-time-computer reading and the "return right after" reading use different resources (MH limit stage versus CTC fixed point). `[FORM]` on each model's stated result; which one the sheet is `[OPEN]`.

## What crosses, and how much

Whatever the mechanism, the bits that cross a sheet of area `A` per use are bounded by the area bound (about `A/4` in Planck units) on any non-expanding light sheet (Bousso, as above). An infinite interior slice (a Coleman–De Luccia bubble's open slices have infinite volume, [Census Taker's Hat](https://arxiv.org/pdf/0710.1129)) is not on such a light sheet, so infinite interior entropy is not excluded by it. That reading is mine, UNVERIFIED. `[HYPER]`

## What the three repositories contribute

* **ordinatics.** The order type of an interior's step count. One sheet interior is `ω`. If each step may consult an agent one sheet deeper, whose whole run counts as one step, depth `k` gives `ω^k`; unbounded depth has supremum `ω^ω`, which is not a rung (`tests/test_nested_sheets.py`, `ω**k` per depth, with sequential rather than nested sheets reaching only `ω·k` as the negative control). The rank order and bands are in `docs/exponent_axis_and_rank_order.md`; the Hardy hierarchy (`fundamental.py`) is a growth measure, not this order type, and the two are not interchangeable (the step-count shadow of depth `k` is polynomial, `H_{ω^k}` is far faster).
* **hyperphysics.** Limit labels: `n` nested stages carry label `ω^n`, the same number, and the word of stages records the order, which is why the limit rule at each sheet must be stated (`docs/research/QUANTUM_GRAVITY_CANDIDATES.md`, ordinatics `docs/complex_rotation_and_limit_rules.md`). The infinite-time-machine limit rule (limsup per cell) is one such rule.
* **hypermath.** Transfinite induction below `ω^k` from `k` nested ordinary inductions (`LadderInduction.lean`) is the proof principle for statements about depth-`k` nestings; `TransfiniteForm.lean` and `ConatTop.lean` hold the least and greatest fixed point readings of a self-containing top (universempiternity). Together they cover every finite depth; the case of a single machine going past `ω^ω` inside one interior is outside them.

## Representing oreality (a proposal, `[HYPER]`)

Oreality as the order-type closure of the nesting: `T(0)` base, `T(k+1)` the interior time of a sheet inside `T(k)`, limit stages at suprema. Prealities hold areality simulations; each is an infinite-time finite space; the transfinite dimension is the order type of the nest. Hypergeometric reality is then what makes the tower exist. `[OPEN]` whether the tower needs ordinals above `ω^ω` (a single interior clocks past them under the machine's limit rule, *recalled*), and what physical quantity the transfinite dimension is.

## Open

* `[OPEN]` MH or CTC or a bounce for the return; stability of MH structure.
* `[OPEN]` Which limit rule an interior uses at its limit stage.
* `[OPEN]` Whether an infinite-volume interior behind a finite-area sheet is consistent with holographic bounds.
