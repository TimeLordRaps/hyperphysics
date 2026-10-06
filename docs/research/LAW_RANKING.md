# Where conservation sits among the laws, and what stands above them

Owner's statements (USER-STATED, 2026-10-06), recorded in hyperreality `PROVENANCE.md`: conservation is a law, but where does it go on a ranking of laws; we assume all laws are absolute but some take priority in resolution, one dominant model over another; and all laws have whole-forms above them that represent them all in order. Tags: `[FORM]` checked or standard, `[FRAME]` holds in a stated model, `[HYPER]` the owner's proposal, `[OPEN]` unresolved. Items marked *recalled* are not retrieved.

## A ranking by dependence (what is derived from what)

| Tier | Kind of law | Examples | Depends on |
|---|---|---|---|
| 0 | Consistency requirements | unitarity, causality (no signalling), cancellation of gauge anomalies | nothing physical: a theory that fails them is not a theory |
| 1 | Symmetry principles | Poincaré invariance (time translation, space translation, rotation, boosts), gauge invariance | Tier 0 |
| 2 | Conservation laws | energy, momentum, angular momentum (from spacetime symmetry); charge (from gauge invariance) | Tier 1 (Noether) |
| 3 | Dynamical laws | equations of motion, field equations | Tiers 0–1 |
| 4 | Statistical and effective laws | the second law, Ohm's law, hydrodynamics | Tier 3 plus coarse-graining |

So conservation sits **between symmetry and dynamics**: it is a consequence of a symmetry, not a free-standing law. Noether's theorem states that each continuous symmetry of the laws gives a conserved quantity (time translation gives energy, space translation momentum, rotation angular momentum) ([overview](https://profoundphysics.com/noethers-theorem-a-complete-guide/)). `[FORM]` standard.

## Priority in resolution: precedents where a lower law yields

* **Conservation yields to a higher structure.** Baryon and lepton number are conserved in the classical Standard Model, but quantum anomalies violate their combination B+L, through sphalerons, while B−L stays conserved; the process is suppressed by about `10⁻¹⁶¹` at zero temperature and unsuppressed at high temperature ([review](https://arxiv.org/pdf/0808.2236), [sphaleron analysis](https://arxiv.org/pdf/2505.05607)). So a "conservation law" is not equally absolute in every case: some are accidental symmetries and give way to a deeper consistency structure. `[FRAME]`
* **Energy conservation is global only given the symmetry.** In an expanding universe time-translation symmetry is absent, and total energy is not defined as a conserved quantity (*recalled*). That is the Noether lever from `END_OF_BASE_REALITY.md`.
* **The second law is statistical,** violated by fluctuations over short times (fluctuation theorems, *recalled*), so it ranks below the exact conservation laws on this scale, despite its reputation.

## A case where consistency fixes the matter

Tier 0 constrains what exists. For one Standard Model generation the left-handed fermions are `Q (3,2,1/6)`, `u^c (3,1,−2/3)`, `d^c (3,1,1/3)`, `L (1,2,−1/2)`, `e^c (1,1,1)` (colour, isospin, hypercharge). `scripts/check_anomaly_cancellation.py`, exact fractions, REPRODUCED 2026-10-06:

* all four anomaly sums (`Y³`, `Y`, `SU(2)²Y`, `SU(3)²Y`) are **zero**;
* with one colour instead of three, the cubic sum is `1/2` and the `SU(2)²Y` sum is `−1/3`;
* removing the `e^c` field gives `Y³ = −1`, `Y = −1`.

Gauge anomalies impose consistency conditions that translate into relations among the hypercharges ([lectures](https://www.repository.cam.ac.uk/handle/1810/313091), [hypercharge quantisation](https://arxiv.org/pdf/1907.00514)). So here a consistency requirement fixes which matter is present, which is a real instance of the owner's "self-consistency dictates matter", though in the opposite direction from "creating or erasing it on demand": the content is fixed in advance, not corrected afterwards. `[FRAME]`

## The whole-form above the laws

The owner's "whole-forms above them that represent them all orderly" has a literal reading here: the **symmetry group** (Poincaré times the gauge group) organizes the conserved quantities, whose charges form a representation of its Lie algebra (energy, momentum, angular momentum, boost generators close into the Poincaré algebra; recalled). That is a single structure above the individual conservation laws that holds them in order. Whether the family's "form" in the hyperstratum sense (a reachable closed derivation chain) can be matched to such a group structure is not shown. `[HYPER]`, `[OPEN]`

## Open

* `[OPEN]` Whether the meta-law the owner posits is Tier 0 (a consistency requirement, as in anomaly cancellation) or a rule above all tiers.
* `[OPEN]` Whether "priority in resolution" is dependence order (this table) or a different ordering.
* `[OPEN]` Whether the whole-form is the symmetry group or something the table does not contain.
