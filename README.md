# hyperphysics

Physical law stated once, with its validity conditions and failure modes
attached, so that adjacent fields can **cite** it instead of paraphrasing it.

```python
from hyperphysics import LAWS_BY_NAME, Transport, Warrant, inherited_failure_modes

LAWS_BY_NAME["capacitor"].form          # 'V = Q / C'
LAWS_BY_NAME["capacitor"].fails_when    # ('the dielectric breaks down', ...)
```

## The problem this solves

Adjacent fields borrow the algebraic shape of physical law. `hyperethics`
transports the series-RLC form onto a will tensor. Left to itself, each borrower
restates the law in its own words, the restatements drift, and the phrase *"this
does not transport"* loses its referent — because there is no longer a canonical
statement of what was borrowed.

So the laws live here and borrowers cite them by name. `hyperphysics.transport`
supplies the interface a borrower must satisfy.

## What a borrower must declare

| # | Declaration | Why |
|---|---|---|
| 1 | which law, **by name** | so the claim has a fixed referent |
| 2 | the form it takes in the target field | so both sides are visible at once |
| 3 | what the borrowing transports | the positive claim |
| 4 | what it does **not** transport | concretely: a unit or a mechanism of the cited law |
| 5 | whether the target constrains a parameter the source leaves free | with a reason |

Item 5 is the one usually missed, and it is the interesting one.

```python
Transport(
    law="capacitor",
    target_field="hyperethics.will",
    target_form="past / constant",
    transports="that accumulated past opposes in inverse proportion to the constant holding it",
    does_not_transport="farads, stored field energy, and the circuit's independence of "
                       "capacitance from inductance",
    warrant=Warrant.BORROWED_FORM,
    constrains_parameters=(Quantity.CAPACITANCE,),
    constraint_reason="capacitance is the invariant's constant of charge, so it is not free",
)
```

`validate` rejects a disclaimer that names neither a unit nor a mechanism of the
law it cites. A borrower cannot satisfy the interface with a general assurance;
it must decline something specific.

## What is and is not claimed

Everything in `electrical.py` is textbook classical circuit theory in the
lumped-element approximation. **Nothing here is new physics and nothing is
offered as new physics.** The contribution is that each law carries its validity
conditions and failure modes as *data* rather than as prose a borrower may skip,
which is what makes a citation checkable.

Two limits are stated in the source and enforced in the tests:

- **`validate` is not a soundness check.** It verifies that the required
  declarations were made and are about the law they claim to be about. A
  perfectly declared transport may still be a bad analogy, and no function in
  this package can tell the difference.
- **Units never transport.** SI units attach to the physical quantity and its
  measurement procedure, not to the algebraic form.

## Composition is tracked

`series-rlc` is not a fifth independent law — it is Kirchhoff's voltage law
applied to three constitutive relations. A borrower of the series form therefore
inherits the failure modes of all four:

```python
inherited_failure_modes(transport_of_series_rlc)   # 9 modes, deduplicated
```

## Layering

The file is `electrical.hm`, not `L0_electrical.hm`. **hyperphysics' ground is
not written**, and naming this file L0 would assert that circuit theory is the
ground of physics, which is false and which nothing here argues. It carries no
layer index rather than a wrong one, and gets re-indexed when the ground exists.

```
hypermath            L0 ground / apply         formal universe from one operation
hyperethics          L0 creation / immanence   normative structure from one operation
hyperphysics         (ground not written)      physical law as a citation surface   <- this repo
metamathethicology   operation spaces          metamath + metaphysics + metaethics + metalogic
```

## Install and check

```bash
pip install -e ".[dev]"
python -m pytest tests
python -m ruff check src tests
```

Zero runtime dependencies; the package imports only the standard library.

See [`electrical.hm`](electrical.hm) for the layer specification and its
graduation criterion, and [`VALIDATION.md`](VALIDATION.md) for what the checks do
and do not establish.

## Open

The two that matter most are open, and they are named in `electrical.hm`:

- **GC-4** — a criterion for when a transport is *sound* rather than merely
  declared. This is the real open problem of the package.
- **GC-5** — hyperphysics' own ground, of which circuit theory would be a
  consequence rather than a starting point.
