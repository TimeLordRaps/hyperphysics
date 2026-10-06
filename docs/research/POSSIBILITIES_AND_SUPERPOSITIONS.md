# Possibilities across laws, superpositions inside them

Owner's statements (USER-STATED, 2026-10-06), recorded verbatim in hyperreality `PROVENANCE.md`: preality has an atemporal version, the same laws with nulltime, which "flows both way acausally" like the film *Tenet*, with events on both sheets of possibility and the flow through possibility collapses reversed, so the reason of a possibility may be the reason of a possibility that collapsed "before" it was realized; possibilities are not superpositions (a superposition has possibilities of collapse), but operate like superpositions that are "sempiternally tied" to quantum superpositions (*sempiternal entanglement*), which gives *sempiternal mechanics*, above quantum mechanics and gravity, "formal specifications of the strategies that operations standardize against"; possibilities operate across physical laws, superpositions inside them; and, later, "atemporal preality obviously encompasses preality and can be simulated in an areality". Tags: `[FORM]` checked, `[FRAME]` holds in a stated model, `[HYPER]` the owner's proposal, `[OPEN]` unresolved. Retrieved or checked 2026-10-06; items marked *recalled* are not retrieved.

## 1. Nulltime flowing both ways: a two-boundary description

A standard formalism treats the past and the future boundary symmetrically: pre- and post-selected states, with the Aharonov–Bergmann–Lebowitz rule `P(k) = |<φ|P_k U ψ>|² / Σ_j |<φ|P_j U ψ>|²` for an intermediate outcome (*recalled* as the two-state-vector formalism; the rule itself is checked here). `scripts/check_two_boundary_possibilities.py`, REPRODUCED 2026-10-06, standard library, qubit with a rotation:

* **Time-symmetric.** Swapping the roles of the two boundaries (pre = φ, post = ψ, evolution `U†`) gives identical intermediate probabilities, for three different later boundaries (`0.283951/0.716049`, `0.5/0.5`, `0.979393/0.020607`). `[FORM]`
* **The reason can be later.** The same intermediate outcome has probability `0.28` or `0.98` depending only on which later state is post-selected. So the "reason" for an intermediate possibility can sit at the later boundary, which is the owner's "a reason of a possibility that collapsed before it became realized". `[FRAME]`
* **Encompassing.** The ordinary forward description is the marginal of the two-boundary one over the later outcome: `[0.386399, 0.613601]` both ways. So the two-sheet (atemporal) description *contains* the one-sheet (temporal) description as a marginal, which is a precise reading of "atemporal preality encompasses preality" for this model. `[FORM]` on the toy; the claim for preality itself is the owner's.

This formalism is not retrocausal in the sense of signalling: it re-describes the same statistics, and whether a physical retrocausal mechanism exists is not shown. The earlier objection on retrocausality, stated once (the Leifer–Pusey and replication literature cited in hyperstratum `wiki/hypermath-program.md`), stands. `[OPEN]`

## 2. Possibilities are not superpositions: sectors

A superposition is coherent: it has interference between its branches. A possibility, as the owner uses it, ranges over *laws*, and does not interfere. The precise quantum counterpart is a **superselection sector**: no coherence between sectors, and every observable commutes with the sector label (*recalled*). `[FRAME]`

`scripts/check_two_boundary_possibilities.py`, part B: a law register `L` and a system qubit `S`.

* **cq (sector) state** `(|0><0|⊗|+><+| + |1><1|⊗|−><−|)/2`: the law label has no coherence.
* **Coherent** `(|0>|+> + |1>|−>)/√2`: the law register is in superposition.

Both give the **same reduced state** on `S` (`[[0.5, 0], [0, 0.5]]`), but only the coherent one is entangled: the minimum eigenvalue of the partial transpose is `−0.5` (negative, entangled) against `0.0` (separable, no entanglement). So *possibilities as sectors are correlated with the system, not entangled with it*. `[FORM]`

This is the one place the proposal needs a ruling (the question below): "sempiternal entanglement" cannot be literal entanglement if the possibilities do not interfere; if it is literal, the law register is coherent and the possibilities *are* superpositions of laws, contradicting "a possibility is not a superposition".

## 3. Shape: simplex or Bloch ball

The state space of a set of mutually exclusive possibilities with no interference is a **simplex** of probability vectors (a segment for two laws). A Bloch ball is the state space of a qubit and needs coherence between its two basis states. "The shape of preality like a Bloch sphere of probabilities" therefore either (a) is the geometry of the *within-law* superpositions, a ball for each law (the sectors are a disjoint union of balls, joined by the simplex of their weights), or (b) asserts coherence between laws. Reading (a) matches "possibilities operate across physical laws, superpositions operate inside them". `[FRAME]` for the geometry, `[OPEN]` which reading is meant.

## 4. Sempiternal mechanics: laws as what operations standardize against

"Formal specifications of the strategies that operations standardize against", and how our laws "are formed from all of the possible laws our reality is made of": the nearest established structure is the renormalization-group picture, where a space of possible theories is flowed and universality classes are the standard forms many different microscopic laws converge to (*recalled*). Possibilities across laws are points in theory space; the laws observed in a base-reality are what the flow standardizes. That is a candidate formalization of "mechanics above quantum mechanics and gravity", not a result: nothing here derives our laws, and the hyperphysics order-of-limits work (`limit labels`) is the part of the family that handles which limits in which order. `[HYPER]`

## 5. Where it sits

* Atemporal preality, same kind as preality (a counterpart, `hyperreality.Counterpart`), encompasses preality, and is simulable in an areality because preality is (`SIMULABLE_IN_AREALITY`); hyperreality encodes both (`atemporal_encompasses`, `simulable_in_areality`).
* The two-boundary and sector structures here are finite toys. They show the statements are consistent and what each requires; they do not show that preality is either.

## Open

* `[OPEN]` **Literal entanglement or sectors.** Is "sempiternal entanglement" a coherent law register (possibilities are then superpositions of laws), or a superselected correlation between laws and within-law superpositions (no entanglement)?
* `[OPEN]` Simplex or Bloch ball for the shape of preality (section 3).
* `[OPEN]` Whether "nulltime flows both ways acausally" means this re-description of statistics or an additional physical retrocausal mechanism.
* `[OPEN]` Whether "encompasses" is a property of preality alone or of every atemporal counterpart.
